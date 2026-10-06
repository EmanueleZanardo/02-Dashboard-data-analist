"""Test tab187 (stile pytest): matching orario PPA (24/7 hourly matching).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_matching_ppa_orario")
calcola_matching_ppa_orario = _F["calcola_matching_ppa_orario"]

TZ = "Europe/Zurich"

KW = dict(gen_mw=10.0, mix_solare_pct=50.0, cf_solare=0.18, cf_eolico=0.40,
          carico_mw=8.0, profilo_carico="Piatto", prezzo_ppa=70.0)


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


def ora_singola(dt, prezzo=100.0):
    idx = pd.DatetimeIndex([pd.Timestamp(dt, tz=TZ)])
    return pd.Series([prezzo], index=idx, name="p")


def ore_pulite(giorni, start="2026-09-28"):
    """Ore dopo la pulizia della tab (duplicati keep-first: l'ora ambigua
    del cambio ora legale 2026-10-25 viene scartata una volta)."""
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    idx = idx.tz_localize(None)
    return int((~idx.duplicated(keep="first")).sum())


class TestInvarianze:
    def test_bilanci_energetici_60gg(self):
        n = ore_pulite(60)
        r = calcola_matching_ppa_orario(piatta(60), **KW)
        assert r["valido"]
        assert r["mwh_abbinati"] + r["mwh_deficit"] == pytest.approx(r["mwh_carico"], rel=1e-9)
        assert r["mwh_abbinati"] + r["mwh_surplus"] == pytest.approx(r["mwh_gen"], rel=1e-9)
        assert r["mwh_carico"] == pytest.approx(8.0 * n, rel=1e-12)
        assert r["n_ore"] == n and r["n_giorni"] == 60

    def test_bilanci_economici_60gg(self):
        r = calcola_matching_ppa_orario(piatta(60), **KW)
        assert r["costo_totale_eur"] == pytest.approx(
            r["costo_ppa_eur"] + r["costo_deficit_eur"] - r["ricavo_surplus_eur"], rel=1e-9)
        assert r["delta_eur"] == pytest.approx(
            r["costo_spot_puro_eur"] - r["costo_totale_eur"], rel=1e-9)
        assert r["prezzo_effettivo_eur_mwh"] == pytest.approx(
            r["costo_totale_eur"] / r["mwh_carico"], rel=1e-9)
        assert r["delta_pct"] == pytest.approx(
            r["delta_eur"] / r["costo_spot_puro_eur"] * 100.0, rel=1e-9)
        assert r["costo_ppa_eur"] == pytest.approx(r["mwh_gen"] * 70.0, rel=1e-9)

    def test_normalizzazione_cf_esatta(self):
        # mix 100% solare -> media sul periodo esattamente cf_solare
        n = ore_pulite(60)
        r = calcola_matching_ppa_orario(piatta(60), **{**KW, "mix_solare_pct": 100.0})
        assert r["mwh_gen"] == pytest.approx(10.0 * 0.18 * n, rel=1e-9)
        r = calcola_matching_ppa_orario(piatta(60), **{**KW, "mix_solare_pct": 0.0})
        assert r["mwh_gen"] == pytest.approx(10.0 * 0.40 * n, rel=1e-9)

    def test_df_giornaliera_coerente(self):
        r = calcola_matching_ppa_orario(piatta(60), **KW)
        df = r["df_giornaliera"]
        assert len(df) == 60
        assert df["MWh abbinati"].sum() == pytest.approx(r["mwh_abbinati"], abs=5.0)
        assert df["MWh deficit"].sum() == pytest.approx(r["mwh_deficit"], abs=5.0)
        assert df["MWh surplus"].sum() == pytest.approx(r["mwh_surplus"], abs=5.0)
        assert df["Costo totale (EUR)"].sum() == pytest.approx(r["costo_totale_eur"], abs=60.0)
        assert set(df.columns) == {"Giorno", "MWh abbinati", "MWh surplus",
                                   "MWh deficit", "MWh carico", "Copertura %",
                                   "Costo totale (EUR)"}

    def test_df_mensile_coerente(self):
        r = calcola_matching_ppa_orario(piatta(60), **KW)
        df = r["df_mensile"]
        assert list(df["Mese"]) == ["2026-09", "2026-10", "2026-11"]
        assert df["MWh abbinati"].sum() == pytest.approx(r["mwh_abbinati"], abs=5.0)
        assert df["Delta vs spot (EUR)"].sum() == pytest.approx(r["delta_eur"], abs=60.0)
        assert df["Costo totale (EUR)"].sum() == pytest.approx(r["costo_totale_eur"], abs=60.0)

    def test_profili_carico_differiscono(self):
        base = dict(KW)
        cop = {}
        for prof in ("Piatto", "Uffici (8-18, lun-ven)", "Industriale 3 turni", "Residenziale"):
            r = calcola_matching_ppa_orario(piatta(30), **{**base, "profilo_carico": prof})
            assert r["valido"]
            cop[prof] = r["copertura_media_pct"]
        assert len(set(round(v, 6) for v in cop.values())) == 4


class TestNumeriAMano:
    def test_ora_solare_mezzogiorno_solstizio(self):
        # 2026-06-21 12:00 (doy 172): sole al picco -> gen = 10 * 0.18 = 1.8 MW
        r = calcola_matching_ppa_orario(ora_singola("2026-06-21 12:00"),
                                        **{**KW, "mix_solare_pct": 100.0})
        assert r["valido"]
        assert r["mwh_gen"] == pytest.approx(1.8, rel=1e-9)
        assert r["mwh_carico"] == pytest.approx(8.0, rel=1e-9)
        assert r["mwh_abbinati"] == pytest.approx(1.8, rel=1e-9)
        assert r["mwh_surplus"] == pytest.approx(0.0, abs=1e-12)
        assert r["mwh_deficit"] == pytest.approx(6.2, rel=1e-9)
        assert r["costo_ppa_eur"] == pytest.approx(126.0, rel=1e-9)
        assert r["costo_deficit_eur"] == pytest.approx(620.0, rel=1e-9)
        assert r["ricavo_surplus_eur"] == pytest.approx(0.0, abs=1e-12)
        assert r["costo_totale_eur"] == pytest.approx(746.0, rel=1e-9)
        assert r["costo_spot_puro_eur"] == pytest.approx(800.0, rel=1e-9)
        assert r["delta_eur"] == pytest.approx(54.0, rel=1e-9)
        assert r["delta_pct"] == pytest.approx(6.75, rel=1e-9)
        assert r["prezzo_effettivo_eur_mwh"] == pytest.approx(93.25, rel=1e-9)
        assert r["copertura_media_pct"] == pytest.approx(22.5, rel=1e-9)
        assert r["ore_100_pct"] == pytest.approx(0.0, abs=1e-12)
        assert r["giudizio"] == "MATCHING DEBOLE"
        assert r["df_giornaliera"]["Giorno"].iloc[0] == "2026-06-21"

    def test_ora_mezzanotte_solare_zero(self):
        r = calcola_matching_ppa_orario(ora_singola("2026-06-21 00:00"),
                                        **{**KW, "mix_solare_pct": 100.0})
        assert r["valido"]
        assert r["mwh_gen"] == pytest.approx(0.0, abs=1e-12)
        assert r["mwh_deficit"] == pytest.approx(8.0, rel=1e-9)
        assert r["costo_totale_eur"] == pytest.approx(800.0, rel=1e-9)
        assert r["delta_eur"] == pytest.approx(0.0, abs=1e-9)
        assert r["copertura_media_pct"] == pytest.approx(0.0, abs=1e-12)
        assert r["giudizio"] == "MATCHING DEBOLE"

    def test_eolico_ora_singola_normalizzato(self):
        # su una sola ora la normalizzazione forza cf = cf_eolico esatto
        r = calcola_matching_ppa_orario(ora_singola("2026-11-15 03:00"),
                                        **{**KW, "mix_solare_pct": 0.0})
        assert r["mwh_gen"] == pytest.approx(10.0 * 0.40, rel=1e-9)
        assert r["mwh_abbinati"] == pytest.approx(4.0, rel=1e-9)

    def test_copertura_piena_eccellente(self):
        r = calcola_matching_ppa_orario(piatta(3), **{**KW, "gen_mw": 1000.0})
        assert r["valido"]
        assert r["mwh_deficit"] == pytest.approx(0.0, abs=1e-9)
        assert r["mwh_abbinati"] == pytest.approx(r["mwh_carico"], rel=1e-9)
        assert r["copertura_media_pct"] == pytest.approx(100.0, rel=1e-9)
        assert r["ore_100_pct"] == pytest.approx(100.0, rel=1e-9)
        assert r["giudizio"] == "MATCHING ECCELLENTE"

    def test_giudizi_soglie_parziale_buono(self):
        kw100 = {**KW, "mix_solare_pct": 100.0}
        r = calcola_matching_ppa_orario(ora_singola("2026-06-21 12:00"),
                                        **{**kw100, "gen_mw": 20.0})
        assert r["copertura_media_pct"] == pytest.approx(45.0, rel=1e-9)
        assert r["giudizio"] == "MATCHING PARZIALE"
        r = calcola_matching_ppa_orario(ora_singola("2026-06-21 12:00"),
                                        **{**kw100, "gen_mw": 35.0})
        assert r["copertura_media_pct"] == pytest.approx(78.75, rel=1e-9)
        assert r["giudizio"] == "MATCHING BUONO"


class TestErrori:
    @pytest.mark.parametrize("k,v", [
        ("gen_mw", 0.0), ("gen_mw", -1.0), ("gen_mw", "x"), ("gen_mw", True),
        ("mix_solare_pct", -1.0), ("mix_solare_pct", 101.0),
        ("cf_solare", 0.0), ("cf_solare", 0.95), ("cf_solare", -0.1),
        ("cf_eolico", 0.0), ("cf_eolico", 0.95),
        ("carico_mw", 0.0), ("carico_mw", -5.0),
        ("profilo_carico", "X"), ("profilo_carico", ""),
        ("prezzo_ppa", -1.0), ("prezzo_ppa", float("nan")),
    ])
    def test_parametri_non_validi(self, k, v):
        r = calcola_matching_ppa_orario(piatta(2), **{**KW, k: v})
        assert not r["valido"] and r["errore"]

    def test_ppa_zero_valido(self):
        r = calcola_matching_ppa_orario(piatta(2), **{**KW, "prezzo_ppa": 0.0})
        assert r["valido"] and r["costo_ppa_eur"] == 0.0

    def test_serie_vuota(self):
        s = pd.Series([], dtype=float, index=pd.DatetimeIndex([]))
        r = calcola_matching_ppa_orario(s, **KW)
        assert not r["valido"]

    def test_non_series(self):
        r = calcola_matching_ppa_orario([100.0, 100.0], **KW)
        assert not r["valido"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0, 100.0], index=["a", "b"])
        r = calcola_matching_ppa_orario(s, **KW)
        assert not r["valido"]

    def test_nan_tz_duplicati(self):
        idx = pd.date_range("2026-09-28", periods=48, freq="h", tz=TZ)
        idx51 = idx.append(idx[:3])  # 3 duplicati
        vals = np.full(51, 100.0)
        vals[5] = np.nan
        s = pd.Series(vals, index=idx51, name="p")
        r = calcola_matching_ppa_orario(s, **KW)
        assert r["valido"]
        assert r["n_ore"] == 47  # 51 - 1 NaN - 3 duplicati

    def test_determinismo(self):
        r1 = calcola_matching_ppa_orario(piatta(30), **KW)
        r2 = calcola_matching_ppa_orario(piatta(30), **KW)
        for k in ("mwh_gen", "mwh_carico", "mwh_abbinati", "mwh_surplus",
                  "mwh_deficit", "costo_totale_eur", "delta_eur",
                  "copertura_media_pct"):
            assert r1[k] == r2[k]
        pd.testing.assert_frame_equal(r1["df_giornaliera"], r2["df_giornaliera"])
        pd.testing.assert_frame_equal(r1["df_mensile"], r2["df_mensile"])


class TestRegistryTab187:
    def test_tab187_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab187" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab187" in withs
        assert len(withs) == len(dvars) == 271
        assert '"🕐 Matching orario PPA"' in src
        assert "calcola_matching_ppa_orario" in src
        keys = re.findall(r'key="(mpo187_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 8
