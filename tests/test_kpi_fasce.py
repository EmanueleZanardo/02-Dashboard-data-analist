"""Test KPI fasce orarie F1/F2/F3 (stile pytest).

Copre: fascia_oraria (confini AEEGSI), calcola_concentrazione_fasce,
calcola_costo_fornitura, sposta_carico_f1_f3, calcola_base_peak_mensile —
inclusi casi limite (serie vuote, NaN, MW a zero, prezzi negativi).
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("fascia_oraria", "calcola_concentrazione_fasce",
          "calcola_costo_fornitura", "sposta_carico_f1_f3",
          "calcola_base_peak_mensile")
fascia_oraria = _F["fascia_oraria"]
calcola_concentrazione_fasce = _F["calcola_concentrazione_fasce"]
calcola_costo_fornitura = _F["calcola_costo_fornitura"]
sposta_carico_f1_f3 = _F["sposta_carico_f1_f3"]
calcola_base_peak_mensile = _F["calcola_base_peak_mensile"]

TZ = "Europe/Zurich"
# lunedi' 2026-09-28: 14 giorni = 2 settimane intere (niente DST nel range)
START = "2026-09-28"


def serie_piatta(ore, prezzo=100.0, start=START):
    idx = pd.date_range(start, periods=ore, freq="h", tz=TZ)
    return pd.Series(np.full(ore, prezzo), index=idx, name="p")


def ts(giorno, ora):
    # giorno: 'YYYY-MM-DD'
    return pd.Timestamp(f"{giorno} {ora:02d}:00")


# ---------------------------------------------------------------- fascia_oraria
class TestFasciaOraria:
    def test_feriale_f1(self):
        assert fascia_oraria(ts("2026-09-28", 8)) == "F1"   # lun 08:00
        assert fascia_oraria(ts("2026-09-28", 12)) == "F1"
        assert fascia_oraria(ts("2026-09-28", 18)) == "F1"  # ultimo minuto F1

    def test_feriale_f2(self):
        assert fascia_oraria(ts("2026-09-28", 7)) == "F2"   # 07:00-08:00
        assert fascia_oraria(ts("2026-09-28", 19)) == "F2"  # 19:00-23:00
        assert fascia_oraria(ts("2026-09-28", 22)) == "F2"

    def test_feriale_f3(self):
        assert fascia_oraria(ts("2026-09-28", 0)) == "F3"
        assert fascia_oraria(ts("2026-09-28", 6)) == "F3"
        assert fascia_oraria(ts("2026-09-28", 23)) == "F3"  # dalle 23:00

    def test_sabato(self):
        assert fascia_oraria(ts("2026-10-03", 12)) == "F2"  # sab 07-23
        assert fascia_oraria(ts("2026-10-03", 7)) == "F2"
        assert fascia_oraria(ts("2026-10-03", 22)) == "F2"
        assert fascia_oraria(ts("2026-10-03", 23)) == "F3"
        assert fascia_oraria(ts("2026-10-03", 6)) == "F3"

    def test_domenica_sempre_f3(self):
        for h in (0, 6, 12, 18, 23):
            assert fascia_oraria(ts("2026-10-04", h)) == "F3"

    def test_tz_aware(self):
        t = pd.Timestamp("2026-09-28 10:00", tz=TZ)
        assert fascia_oraria(t) == "F1"


# ------------------------------------------------- calcola_concentrazione_fasce
class TestConcentrazioneFasce:
    def test_piatta_quota_top10_circa_10(self):
        r = calcola_concentrazione_fasce(serie_piatta(336), 1.0, 1.0, 1.0)
        assert r["errore"] is None
        f1 = r["fasce"]["F1"]
        assert f1["ore"] == 110          # 10 feriali x 11h
        assert f1["energia_mwh"] == pytest.approx(110.0)
        assert f1["costo_eur"] == pytest.approx(11000.0)
        assert f1["p10"] == f1["p50"] == f1["p90"] == pytest.approx(100.0)
        assert f1["skew"] == pytest.approx(0.0)
        # serie piatta: la quota del 10% piu' caro e' ~10% (discretizzazione)
        for fx in ("F1", "F2", "F3"):
            q = r["fasce"][fx]["quota_top10_pct"]
            assert q == pytest.approx(10.0, abs=1.5), (fx, q)
        # ore per coprire il 50% del costo: ceil(n/2)
        assert r["fasce"]["F1"]["ore_50pct"] == 55
        assert r["fasce"]["F2"]["ore_50pct"] == 41   # n=82
        assert r["fasce"]["F3"]["ore_50pct"] == 72   # n=144

    def test_curva_lorenz_finisice_a_100(self):
        r = calcola_concentrazione_fasce(serie_piatta(336), 1.0, 1.0, 1.0)
        df = r["df_curva"]
        assert len(df) == 60  # 20 punti x 3 fasce
        for fx in ("F1", "F2", "F3"):
            ultimo = df[df["Fascia"] == fx].iloc[-1]
            assert ultimo["Quota ore (%)"] == pytest.approx(100.0)
            assert ultimo["Quota costo cumulata (%)"] == pytest.approx(100.0)

    def test_spike_concentra_f1(self):
        s = serie_piatta(336)
        s.iloc[8] = 10000.0  # lunedi' 08:00 -> fascia F1
        r = calcola_concentrazione_fasce(s, 1.0, 1.0, 1.0)
        q = r["fasce"]["F1"]["quota_top10_pct"]
        assert 52.0 < q < 54.0, q          # (10000+10*100)/20900
        assert r["fasce"]["F1"]["ore_50pct"] == 6
        assert r["fascia_piu_concentrata"] == "F1"
        # F2/F3 restano piatte
        assert r["fasce"]["F2"]["quota_top10_pct"] == pytest.approx(10.0, abs=1.5)

    def test_serie_vuota(self):
        vuota = pd.Series([], dtype=float,
                          index=pd.DatetimeIndex([], tz=TZ))
        r = calcola_concentrazione_fasce(vuota, 1.0, 1.0, 1.0)
        assert r["errore"] is None
        for fx in ("F1", "F2", "F3"):
            assert r["fasce"][fx]["ore"] == 0
            assert r["fasce"][fx]["quota_top10_pct"] is None
        assert r["fascia_piu_concentrata"] is None
        assert len(r["df_curva"]) == 0

    def test_tutti_nan(self):
        s = serie_piatta(24)
        s[:] = np.nan
        r = calcola_concentrazione_fasce(s, 1.0, 1.0, 1.0)
        assert r["errore"] is None
        assert r["fasce"]["F1"]["ore"] == 0
        assert r["fascia_piu_concentrata"] is None

    def test_indice_non_datetime(self):
        r = calcola_concentrazione_fasce(pd.Series([100.0, 120.0]), 1.0, 1.0, 1.0)
        assert r["errore"] is None
        assert all(r["fasce"][fx]["ore"] == 0 for fx in ("F1", "F2", "F3"))

    def test_mw_zero(self):
        r = calcola_concentrazione_fasce(serie_piatta(336), 0.0, 0.0, 0.0)
        assert r["errore"] is None
        assert all(r["fasce"][fx]["ore"] == 0 for fx in ("F1", "F2", "F3"))
        assert r["fascia_piu_concentrata"] is None

    def test_prezzi_negativi_niente_concentrazione(self):
        r = calcola_concentrazione_fasce(serie_piatta(336, prezzo=-10.0),
                                        1.0, 1.0, 1.0)
        assert r["errore"] is None
        assert r["fasce"]["F1"]["ore"] == 110
        assert r["fasce"]["F1"]["costo_eur"] < 0
        # costo totale <= 0 -> niente quote di concentrazione
        assert r["fasce"]["F1"]["quota_top10_pct"] is None
        assert r["fasce"]["F1"]["ore_50pct"] is None


# ------------------------------------------------------- calcola_costo_fornitura
class TestCostoFornitura:
    def test_piatta(self):
        r = calcola_costo_fornitura(serie_piatta(336), 1.0, 1.0, 1.0)
        assert r["totale"] == pytest.approx(33600.0)
        assert r["mwh"] == pytest.approx(336.0)
        assert r["ponderato"] == pytest.approx(100.0)
        pf = r["per_fascia"]
        assert pf.loc["F1", "ore"] == 110
        assert pf.loc["F1", "mwh"] == pytest.approx(110.0)
        assert pf.loc["F1", "costo"] == pytest.approx(11000.0)
        assert pf.loc["F1", "prezzo_medio"] == pytest.approx(100.0)
        assert pf.loc["F2", "ore"] == 82
        assert pf.loc["F3", "ore"] == 144

    def test_mw_zero_ponderato_nan(self):
        r = calcola_costo_fornitura(serie_piatta(24), 0.0, 0.0, 0.0)
        assert r["mwh"] == 0.0
        assert np.isnan(r["ponderato"])

    def test_spike_f1_alza_ponderato(self):
        s = serie_piatta(336)
        s.iloc[8] = 10000.0
        r = calcola_costo_fornitura(s, 1.0, 1.0, 1.0)
        assert r["ponderato"] > 100.0
        assert r["totale"] == pytest.approx(33600.0 + 9900.0)


# ---------------------------------------------------------- sposta_carico_f1_f3
class TestSpostaCarico:
    def test_energia_conservata(self):
        s = serie_piatta(336)
        f1n, f3n = sposta_carico_f1_f3(s, 2.0, 1.0, 50.0)
        assert f1n == pytest.approx(1.0)
        assert f3n == pytest.approx(1.0 + 110.0 / 144.0)
        prima = 2.0 * 110 + 1.0 * 144
        dopo = f1n * 110 + f3n * 144
        assert dopo == pytest.approx(prima)

    def test_quota_zero_inviarato(self):
        s = serie_piatta(336)
        assert sposta_carico_f1_f3(s, 2.0, 1.0, 0.0) == (2.0, 1.0)

    def test_quota_100_azzera_f1(self):
        s = serie_piatta(336)
        f1n, f3n = sposta_carico_f1_f3(s, 2.0, 1.0, 100.0)
        assert f1n == pytest.approx(0.0)
        assert f3n == pytest.approx(1.0 + 220.0 / 144.0)

    def test_quota_clampata(self):
        s = serie_piatta(336)
        assert sposta_carico_f1_f3(s, 2.0, 1.0, 150.0) == \
            pytest.approx(sposta_carico_f1_f3(s, 2.0, 1.0, 100.0))
        assert sposta_carico_f1_f3(s, 2.0, 1.0, -20.0) == (2.0, 1.0)

    def test_senza_ore_f1_inviarato(self):
        # solo domenica: niente ore F1
        idx = pd.date_range("2026-10-04", periods=24, freq="h", tz=TZ)
        s = pd.Series(np.full(24, 100.0), index=idx)
        assert sposta_carico_f1_f3(s, 2.0, 1.0, 50.0) == (2.0, 1.0)


# ----------------------------------------------------- calcola_base_peak_mensile
class TestBasePeakMensile:
    def test_piatta_spread_zero(self):
        idx = pd.date_range("2026-01-01", periods=31 * 24, freq="h", tz=TZ)
        s = pd.Series(np.full(len(idx), 100.0), index=idx)
        df = calcola_base_peak_mensile(s)
        assert len(df) == 1
        r = df.iloc[0]
        assert r["Mese"] == "2026-01"
        assert r["Base (€/MWh)"] == pytest.approx(100.0)
        assert r["Peak (€/MWh)"] == pytest.approx(100.0)
        assert r["Offpeak (€/MWh)"] == pytest.approx(100.0)
        assert r["Spread P-O (€/MWh)"] == pytest.approx(0.0)
        assert r["Spread %"] == pytest.approx(0.0)
        attese = int((((idx.weekday < 5) & (idx.hour >= 8)
                       & (idx.hour < 20))).sum())
        assert r["Ore peak"] == attese

    def test_peak_piu_caro(self):
        idx = pd.date_range("2026-01-01", periods=31 * 24, freq="h", tz=TZ)
        v = np.where(((idx.weekday < 5) & (idx.hour >= 8) & (idx.hour < 20)),
                     150.0, 60.0)
        df = calcola_base_peak_mensile(pd.Series(v, index=idx))
        r = df.iloc[0]
        assert r["Peak (€/MWh)"] == pytest.approx(150.0)
        assert r["Offpeak (€/MWh)"] == pytest.approx(60.0)
        assert r["Spread P-O (€/MWh)"] == pytest.approx(90.0)

    def test_serie_vuota(self):
        df = calcola_base_peak_mensile(
            pd.Series([], dtype=float, index=pd.DatetimeIndex([], tz=TZ)))
        assert len(df) == 0
        assert list(df.columns) == ["Mese", "Base (€/MWh)", "Peak (€/MWh)",
                                    "Offpeak (€/MWh)", "Spread P-O (€/MWh)",
                                    "Spread %", "Ore peak"]

    def test_indice_non_datetime(self):
        df = calcola_base_peak_mensile(pd.Series([1.0, 2.0, 3.0]))
        assert len(df) == 0
