"""Test tab188 (stile pytest): comunita' energetica / autoconsumo collettivo.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_comunita_energetica")
calcola_comunita_energetica = _F["calcola_comunita_energetica"]

TZ = "Europe/Zurich"

KW = dict(potenza_fv_kwp=100.0, cf_fv=0.13, n_utenze=20, picco_kw=4.0,
          profilo_utenze="Mix automatico",
          maggiorazione_retail=45.0, premio_cer=0.0)


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


def ore_pulite(giorni, start="2026-09-28"):
    """Ore dopo la pulizia della tab (duplicati keep-first: l'ora ambigua
    del cambio ora legale 2026-10-25 viene scartata una volta)."""
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    idx = idx.tz_localize(None)
    return int((~idx.duplicated(keep="first")).sum())


class TestInvarianze:
    def test_bilanci_energetici_60gg(self):
        n = ore_pulite(60)
        r = calcola_comunita_energetica(piatta(60), **KW)
        assert r["valido"]
        assert r["mwh_condivisi"] + r["mwh_deficit"] == pytest.approx(
            r["mwh_carico"], rel=1e-9)
        assert r["mwh_condivisi"] + r["mwh_surplus"] == pytest.approx(
            r["mwh_gen"], rel=1e-9)
        assert r["n_ore"] == n and r["n_giorni"] == 60
        assert r["n_utenze"] == 20

    def test_bilanci_economici_60gg(self):
        # beneficio = (baseline - comunita') + condivisi * premio
        r = calcola_comunita_energetica(piatta(60), **KW)
        atteso = (r["costo_baseline_eur"] - r["costo_comunita_eur"]
                  + r["mwh_condivisi"] * KW["premio_cer"])
        assert r["beneficio_eur"] == pytest.approx(atteso, rel=1e-9)

    def test_premio_zero_beneficio_uguale_diff_costi(self):
        r = calcola_comunita_energetica(piatta(30), **KW)
        assert r["beneficio_eur"] == pytest.approx(
            r["costo_baseline_eur"] - r["costo_comunita_eur"], rel=1e-9)

    def test_premio_positivo_aumenta_beneficio(self):
        kw0 = dict(KW, premio_cer=0.0)
        kw1 = dict(KW, premio_cer=110.0)
        r0 = calcola_comunita_energetica(piatta(30), **kw0)
        r1 = calcola_comunita_energetica(piatta(30), **kw1)
        assert r1["beneficio_eur"] == pytest.approx(
            r0["beneficio_eur"] + r1["mwh_condivisi"] * 110.0, rel=1e-9)

    def test_quote_in_range(self):
        r = calcola_comunita_energetica(piatta(30), **KW)
        assert 0.0 <= r["quota_condivisa_pct"] <= 100.0
        assert 0.0 <= r["autoconsumo_collettivo_pct"] <= 100.0
        assert r["beneficio_per_utenza_eur"] == pytest.approx(
            r["beneficio_eur"] / 20, rel=1e-12)

    def test_tutti_i_profili_validi(self):
        for prof in ("Piatto", "Uffici (8-18, lun-ven)", "Industriale 3 turni",
                     "Residenziale", "Mix automatico"):
            r = calcola_comunita_energetica(piatta(10),
                                            **dict(KW, profilo_utenze=prof))
            assert r["valido"], prof
            assert r["mwh_carico"] > 0

    def test_fv_sovradimensionato_quota_sale(self):
        r_pic = calcola_comunita_energetica(piatta(30),
                                            **dict(KW, potenza_fv_kwp=50.0))
        r_gra = calcola_comunita_energetica(piatta(30),
                                            **dict(KW, potenza_fv_kwp=400.0))
        assert r_gra["mwh_gen"] > r_pic["mwh_gen"]
        assert r_gra["mwh_condivisi"] >= r_pic["mwh_condivisi"]
        # piu' FV -> piu' surplus, autoconsumo collettivo cala
        assert r_gra["autoconsumo_collettivo_pct"] <= r_pic["autoconsumo_collettivo_pct"]


class TestProfiloPiattoEsatto:
    def test_mwh_carico_da_seed_188(self):
        # profilo Piatto: shape sempre 1.0; picchi = 4*(0.6+0.8*rand) seed 188
        rng = np.random.RandomState(188)
        picchi = 4.0 * (0.6 + 0.8 * rng.rand(5))
        n = ore_pulite(3)
        r = calcola_comunita_energetica(
            piatta(3), potenza_fv_kwp=100.0, cf_fv=0.13, n_utenze=5,
            picco_kw=4.0, profilo_utenze="Piatto",
            maggiorazione_retail=45.0, premio_cer=0.0)
        assert r["valido"]
        assert r["mwh_carico"] == pytest.approx(picchi.sum() * n / 1000.0,
                                                rel=1e-9)

    def test_beneficio_piatto_markup(self):
        r = calcola_comunita_energetica(
            piatta(3), potenza_fv_kwp=100.0, cf_fv=0.13, n_utenze=5,
            picco_kw=4.0, profilo_utenze="Piatto",
            maggiorazione_retail=45.0, premio_cer=10.0)
        assert r["beneficio_eur"] == pytest.approx(r["mwh_condivisi"] * 55.0,
                                                   rel=1e-9)


class TestErrori:
    def test_serie_vuota(self):
        s = pd.Series([], dtype=float,
                      index=pd.DatetimeIndex([], tz=TZ), name="p")
        r = calcola_comunita_energetica(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_non_series(self):
        r = calcola_comunita_energetica([1.0, 2.0, 3.0], **KW)
        assert not r["valido"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0] * 48, index=["ora-%d" % i for i in range(48)])
        r = calcola_comunita_energetica(s, **KW)
        assert not r["valido"]

    def test_una_sola_utenza(self):
        r = calcola_comunita_energetica(piatta(5), **dict(KW, n_utenze=1))
        assert not r["valido"]

    def test_cf_zero(self):
        r = calcola_comunita_energetica(piatta(5), **dict(KW, cf_fv=0.0))
        assert not r["valido"]

    def test_fv_zero(self):
        r = calcola_comunita_energetica(
            piatta(5), **dict(KW, potenza_fv_kwp=0.0))
        assert not r["valido"]

    def test_profilo_sconosciuto(self):
        r = calcola_comunita_energetica(
            piatta(5), **dict(KW, profilo_utenze="Boh"))
        assert not r["valido"]

    def test_markup_negativo(self):
        r = calcola_comunita_energetica(
            piatta(5), **dict(KW, maggiorazione_retail=-1.0))
        assert not r["valido"]


class TestDeterminismo:
    def test_due_chiamate_uguali(self):
        r1 = calcola_comunita_energetica(piatta(14), **KW)
        r2 = calcola_comunita_energetica(piatta(14), **KW)
        for k in ("mwh_gen", "mwh_carico", "mwh_condivisi", "mwh_surplus",
                  "mwh_deficit", "beneficio_eur", "costo_baseline_eur",
                  "costo_comunita_eur", "quota_condivisa_pct",
                  "autoconsumo_collettivo_pct", "giudizio"):
            assert r1[k] == r2[k]
        pd.testing.assert_frame_equal(r1["df_giornaliera"],
                                      r2["df_giornaliera"])
        pd.testing.assert_frame_equal(r1["df_mensile"], r2["df_mensile"])


class TestTabelle:
    def test_df_giornaliera_colonne(self):
        r = calcola_comunita_energetica(piatta(9), **KW)
        df = r["df_giornaliera"]
        assert list(df.columns) == ["Giorno", "MWh generati", "MWh carico",
                                    "MWh condivisi", "MWh surplus",
                                    "MWh deficit", "Quota condivisa %",
                                    "Beneficio (EUR)"]
        assert len(df) == 9
        assert df["MWh condivisi"].sum() == pytest.approx(
            r["mwh_condivisi"], abs=0.05)
        # beneficio giornaliero arrotondato a 0 decimali: tolleranza 0.5/giorno
        assert df["Beneficio (EUR)"].sum() == pytest.approx(
            r["beneficio_eur"], abs=len(df) * 0.5 + 1e-9)

    def test_df_mensile_cumulato_monotono(self):
        r = calcola_comunita_energetica(piatta(75), **KW)
        df = r["df_mensile"]
        assert "Beneficio cumulato (EUR)" in df.columns
        cum = df["Beneficio cumulato (EUR)"].to_numpy()
        assert (np.diff(cum) >= -1e-9).all()
        # cumulato = round(cumsum(non arrotondati)): tolleranza 0.5/mese
        assert cum[-1] == pytest.approx(r["beneficio_eur"],
                                       abs=len(df) * 0.5 + 1e-9)


class TestRegistryTab188:
    def test_tab188_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab188" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab188" in withs
        assert len(withs) == len(dvars) == 211
        assert '"🤝 Comunità energetica"' in src
        assert "calcola_comunita_energetica" in src
        keys = re.findall(r'key="(cer188_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 8
