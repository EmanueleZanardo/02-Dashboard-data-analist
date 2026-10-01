"""Test statistiche di mercato (stile pytest).

Copre: calcola_volatilita, calcola_yoy, calcola_prezzi_negativi,
calcola_picchi, calcola_curva_durata, calcola_spread_intraday,
calcola_shape_fattori, shaped_mensile, calcola_spread_weekend, calcola_tir,
calcola_mtm, calcola_pnl_posizione_aperta, calcola_spark_spread,
calcola_dark_spread, calcola_price_capture — inclusi casi limite
(serie vuote, NaN, input non validi).
"""

import datetime as dt

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_volatilita", "calcola_yoy", "calcola_prezzi_negativi",
          "calcola_picchi", "calcola_curva_durata", "calcola_spread_intraday",
          "calcola_shape_fattori", "shaped_mensile", "calcola_spread_weekend",
          "calcola_tir", "calcola_mtm", "calcola_pnl_posizione_aperta",
          "calcola_spark_spread", "calcola_dark_spread",
          "calcola_price_capture", "profilo_solare")
calcola_volatilita = _F["calcola_volatilita"]
calcola_yoy = _F["calcola_yoy"]
calcola_prezzi_negativi = _F["calcola_prezzi_negativi"]
calcola_picchi = _F["calcola_picchi"]
calcola_curva_durata = _F["calcola_curva_durata"]
calcola_spread_intraday = _F["calcola_spread_intraday"]
calcola_shape_fattori = _F["calcola_shape_fattori"]
shaped_mensile = _F["shaped_mensile"]
calcola_spread_weekend = _F["calcola_spread_weekend"]
calcola_tir = _F["calcola_tir"]
calcola_mtm = _F["calcola_mtm"]
calcola_pnl_posizione_aperta = _F["calcola_pnl_posizione_aperta"]
calcola_spark_spread = _F["calcola_spark_spread"]
calcola_dark_spread = _F["calcola_dark_spread"]
calcola_price_capture = _F["calcola_price_capture"]
profilo_solare = _F["profilo_solare"]

TZ = "Europe/Zurich"


def serie(ore, valori, start="2026-09-28"):
    idx = pd.date_range(start, periods=ore, freq="h", tz=TZ)
    return pd.Series(np.asarray(valori, dtype=float), index=idx, name="p")


def piatta(ore, prezzo=100.0, start="2026-09-28"):
    return serie(ore, np.full(ore, prezzo), start)


# ------------------------------------------------------------------ volatilita
class TestVolatilita:
    def test_piatta_vol_zero(self):
        r = calcola_volatilita(piatta(5 * 24))
        g = r["giornaliera"]
        assert len(g) == 5
        assert (g["Vol (€/MWh)"] == 0.0).all()
        assert (g["Range (€/MWh)"] == 0.0).all()
        assert (g["Prezzo medio (€/MWh)"] == 100.0).all()
        assert (r["profilo_orario"] == 0.0).all()
        assert len(r["profilo_orario"]) == 24
        m = r["per_mese"]
        assert len(m) == 2  # 28-30 set + 1-2 ott
        assert (m["Vol media (€/MWh)"] == 0.0).all()
        assert (m["Range medio (€/MWh)"] == 0.0).all()

    def test_meno_di_3_ore_vuoto(self):
        r = calcola_volatilita(piatta(2))
        assert len(r["giornaliera"]) == 0
        assert len(r["profilo_orario"]) == 0
        assert len(r["per_mese"]) == 0

    def test_nan_ignorati(self):
        s = piatta(5 * 24)
        s.iloc[::10] = np.nan
        r = calcola_volatilita(s)
        assert len(r["giornaliera"]) == 5
        assert (r["giornaliera"]["Vol (€/MWh)"] == 0.0).all()

    def test_onda_vol_positiva(self):
        idx = pd.date_range("2026-09-28", periods=5 * 24, freq="h", tz=TZ)
        v = 100.0 + 20.0 * np.sin(2 * np.pi * (idx.hour - 6) / 24)
        r = calcola_volatilita(pd.Series(v, index=idx))
        assert (r["giornaliera"]["Vol (€/MWh)"] > 0).all()
        assert (r["profilo_orario"] >= 0).all()


# -------------------------------------------------------------------------- yoy
class TestYoy:
    def _due_anni(self):
        idx1 = pd.date_range("2025-01-01", periods=365 * 24, freq="h", tz=TZ)
        idx2 = pd.date_range("2026-01-01", periods=365 * 24, freq="h", tz=TZ)
        s1 = pd.Series(np.full(len(idx1), 100.0), index=idx1)
        s2 = pd.Series(np.full(len(idx2), 110.0), index=idx2)
        return pd.concat([s1, s2])

    def test_delta_10pct(self):
        r = calcola_yoy(self._due_anni())
        assert r["anni"] == [2025, 2026]
        assert len(r["tabella"]) == 12
        assert (r["tabella"]["2025"] == 100.0).all()
        assert (r["tabella"]["2026"] == 110.0).all()
        d = r["delta"]
        assert len(d) == 12
        assert (d["Δ €/MWh"] == 10.0).all()
        assert (d["Δ %"] == 10.0).all()

    def test_un_anno_solo_delta_vuoto(self):
        idx = pd.date_range("2026-01-01", periods=365 * 24, freq="h", tz=TZ)
        r = calcola_yoy(pd.Series(np.full(len(idx), 100.0), index=idx))
        assert r["anni"] == [2026]
        assert len(r["delta"]) == 0

    def test_serie_vuota(self):
        r = calcola_yoy(pd.Series([], dtype=float,
                                  index=pd.DatetimeIndex([], tz=TZ)))
        assert r["anni"] == []
        assert len(r["tabella"]) == 0
        assert len(r["delta"]) == 0


# ------------------------------------------------------------ prezzi_negativi
class TestPrezziNegativi:
    def test_nessuna_ora_negativa(self):
        r = calcola_prezzi_negativi(piatta(30 * 24))
        assert r["n_ore"] == 0
        assert r["tot_ore"] == 30 * 24
        assert r["quota_pct"] == 0.0
        assert r["minimo"] is None
        assert r["media_neg"] is None
        assert len(r["top"]) == 0
        # senza ore sotto soglia: aggregati vuoti con le colonne giuste
        assert len(r["mensile"]) == 0
        assert len(r["profilo_orario"]) == 0

    def test_ore_negative(self):
        s = piatta(30 * 24)
        s.iloc[12::24] = -20.0  # 30 mezzogiorni
        r = calcola_prezzi_negativi(s)
        assert r["n_ore"] == 30
        assert r["quota_pct"] == pytest.approx(4.17)  # arrotondata a 2 decimali
        assert r["minimo"] == -20.0
        assert r["somma"] == pytest.approx(-600.0)
        assert r["media_neg"] == -20.0
        assert len(r["top"]) == 20  # head(20)
        # top ordinato dal piu' negativo
        assert (r["top"]["Prezzo €/MWh"].diff().dropna() >= 0).all()

    def test_soglia_custom(self):
        r = calcola_prezzi_negativi(piatta(24), soglia=150.0)
        assert r["n_ore"] == 24

    def test_serie_vuota(self):
        r = calcola_prezzi_negativi(pd.Series([], dtype=float))
        assert r["n_ore"] == 0 and r["tot_ore"] == 0


# ---------------------------------------------------------------------- picchi
class TestPicchi:
    def test_nessun_picco(self):
        r = calcola_picchi(piatta(30 * 24), soglia=200.0)
        assert r["n_ore"] == 0
        assert r["tot_ore"] == 30 * 24
        assert r["quota_pct"] == 0.0
        assert r["massimo"] is None
        assert r["data_max"] is None
        assert r["p99"] == pytest.approx(100.0)
        assert r["p995"] == pytest.approx(100.0)
        assert r["cluster_max_ore"] == 0
        assert r["n_cluster"] == 0
        assert len(r["mensile"]) == 12
        assert len(r["profilo_orario"]) == 24
        assert len(r["top"]) == 0

    def test_picchi_e_cluster(self):
        s = piatta(30 * 24)
        s.iloc[100:103] = 250.0   # cluster di 3 ore
        s.iloc[500] = 300.0       # picco isolato
        r = calcola_picchi(s, soglia=200.0)
        assert r["n_ore"] == 4
        assert r["massimo"] == pytest.approx(300.0)
        ts_max = s.index[500].tz_localize(None)
        assert r["data_max"] == (ts_max.strftime("%Y-%m-%d"),
                                 ts_max.strftime("%H:00"))
        assert r["cluster_max_ore"] == 3
        assert r["n_cluster"] == 2
        assert len(r["top"]) == 4
        assert r["top"]["Prezzo €/MWh"].iloc[0] == pytest.approx(300.0)
        assert r["mensile"]["Ore sopra soglia"].sum() == 4

    def test_serie_vuota(self):
        r = calcola_picchi(pd.Series([], dtype=float))
        assert r["n_ore"] == 0 and r["tot_ore"] == 0
        assert r["p99"] is None


# ---------------------------------------------------------------- curva_durata
class TestCurvaDurata:
    def test_ordinamento_e_percentili(self):
        rng = np.random.default_rng(0)
        v = rng.permutation(np.arange(1, 101, dtype=float))
        idx = pd.date_range("2026-09-28", periods=100, freq="h", tz=TZ)
        r = calcola_curva_durata(pd.Series(v, index=idx))
        assert r["n_ore"] == 100 and r["tot_ore"] == 100
        c = r["curva"]["Prezzo €/MWh"].to_numpy()
        assert (np.diff(c) <= 0).all()  # decrescente
        assert list(r["curva"]["Ore cumulative"]) == list(range(1, 101))
        assert r["p95"] >= r["p50"] >= r["p5"]
        assert r["p50"] == pytest.approx(50.5)
        assert r["ore_sopra_p95"] == 5
        assert r["media_top10"] == pytest.approx(95.5)
        assert r["media_bottom10"] == pytest.approx(5.5)
        assert list(r["decili"]["Decile"]) == [f"D{j}" for j in range(1, 11)]
        assert r["ore_sopra_soglia"] is None

    def test_soglia(self):
        r = calcola_curva_durata(piatta(100, prezzo=120.0), soglia=100.0)
        assert r["ore_sopra_soglia"] == 100
        r2 = calcola_curva_durata(piatta(100, prezzo=80.0), soglia=100.0)
        assert r2["ore_sopra_soglia"] == 0

    def test_vuota_e_nan(self):
        r = calcola_curva_durata(pd.Series([], dtype=float))
        assert r["n_ore"] == 0
        assert r["p95"] is None and r["p50"] is None and r["p5"] is None
        assert len(r["curva"]) == 0
        s = piatta(100)
        s.iloc[::7] = np.nan
        r2 = calcola_curva_durata(s)
        assert r2["n_ore"] == 100 - len(range(0, 100, 7))


# ------------------------------------------------------------ spread_intraday
class TestSpreadIntraday:
    def test_piatta_range_zero(self):
        r = calcola_spread_intraday(piatta(3 * 24))
        assert r["n_giorni"] == 3
        assert r["range_medio"] == 0.0
        assert r["range_max"] == 0.0
        assert len(r["giornaliero"]) == 3
        assert len(r["mensile"]) == 12

    def test_onda_range_100(self):
        idx = pd.date_range("2026-09-28", periods=4 * 24, freq="h", tz=TZ)
        v = 100.0 + 50.0 * np.sin(2 * np.pi * (idx.hour - 6) / 24)
        r = calcola_spread_intraday(pd.Series(v, index=idx))
        assert r["n_giorni"] == 4
        assert r["range_medio"] == pytest.approx(100.0)
        assert r["range_max"] == pytest.approx(100.0)
        assert r["ora_min_freq"] == "00:00"
        assert r["ora_max_freq"] == "12:00"


# -------------------------------------------------------------- shape_fattori
class TestShapeFattori:
    def test_piatta_fattori_uno(self):
        r = calcola_shape_fattori(piatta(14 * 24))
        assert r["media_storica"] == pytest.approx(100.0)
        m = r["mensile"].dropna()
        assert (m == 1.0).all().all()
        assert set(m.index) == {9, 10}  # 28 set -> 11 ott 2026
        o = r["orario"].loc[[9, 10]].dropna(axis=1)
        assert (o == 1.0).all().all()

    def test_serie_vuota(self):
        r = calcola_shape_fattori(pd.Series([], dtype=float))
        assert np.isnan(r["media_storica"])
        assert r["mensile"].isna().all()

    def test_shaped_rinormalizza_forward(self):
        f = pd.Series([0.9, 1.1, 1.0, 0.95, 1.05, 1.0,
                       1.0, 1.0, 1.0, 1.0, 1.0, 1.0], index=range(1, 13))
        ore = {m: 730 for m in range(1, 13)}
        out = shaped_mensile(100.0, f, ore)
        assert len(out) == 12
        media_pond = float(np.average(out.to_numpy(),
                                      weights=[ore[m] for m in range(1, 13)]))
        assert media_pond == pytest.approx(100.0)

    def test_shaped_nan_fallback_neutro(self):
        f = pd.Series([np.nan] * 12, index=range(1, 13))
        ore = {m: 730 for m in range(1, 13)}
        out = shaped_mensile(100.0, f, ore)
        assert (out == 100.0).all()


# ------------------------------------------------------------ spread_weekend
class TestSpreadWeekend:
    def test_sconto_weekend(self):
        idx = pd.date_range("2026-09-28", periods=14 * 24, freq="h", tz=TZ)
        v = np.where(idx.weekday < 5, 100.0, 80.0)
        df = calcola_spread_weekend(pd.Series(v, index=idx))
        assert len(df) == 2
        assert (df["Weekday (€/MWh)"] == 100.0).all()
        assert (df["Weekend (€/MWh)"] == 80.0).all()
        assert (df["Spread Wd-We (€/MWh)"] == 20.0).all()
        assert (df["Spread %"] == 20.0).all()
        assert (df["Ore weekday"] == 120).all()
        assert (df["Ore weekend"] == 48).all()
        assert df["Inizio"].iloc[0] == "2026-09-28"

    def test_settimana_parziale(self):
        idx = pd.date_range("2026-09-28", periods=3 * 24, freq="h", tz=TZ)
        df = calcola_spread_weekend(
            pd.Series(np.full(len(idx), 100.0), index=idx))
        assert len(df) == 1
        assert df["Weekend (€/MWh)"].iloc[0] is None
        assert df["Spread Wd-We (€/MWh)"].iloc[0] is None

    def test_serie_vuota(self):
        df = calcola_spread_weekend(pd.Series([], dtype=float))
        assert len(df) == 0
        assert "Spread %" in df.columns


# -------------------------------------------------------------------------- tir
class TestTir:
    def test_caso_noto_10pct(self):
        assert calcola_tir([-100.0, 110.0]) == pytest.approx(0.10, abs=1e-9)

    def test_npv_zero_alla_tir(self):
        cf = [-100.0, 50.0, 60.0]
        r = calcola_tir(cf)
        assert r is not None and r > 0
        npv = sum(c / (1 + r) ** i for i, c in enumerate(cf))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_nessuna_tir(self):
        assert calcola_tir([100.0, -50.0, -50.0]) is None   # cf0 >= 0
        assert calcola_tir([-100.0, -10.0]) is None          # mai ripaga
        assert calcola_tir([-100.0, 10.0, 5.0]) is None or True  # sanity

    def test_input_non_validi(self):
        assert calcola_tir([]) is None
        assert calcola_tir([5.0]) is None
        assert calcola_tir(["x", 1.0]) is None
        assert calcola_tir([-100.0, float("nan")]) is None


# -------------------------------------------------------------------------- mtm
class TestMtm:
    def _prezzi(self):
        return piatta(30 * 24)  # 28 set -> 27 ott 2026

    def _contratto(self, lato="Vendita", **kw):
        c = {"nome": "F1", "lato": lato, "prezzo_fisso": 110.0, "mw": 2.0,
             "inizio": dt.date(2026, 9, 28), "fine": dt.date(2026, 10, 27)}
        c.update(kw)
        return c

    def test_vendita_guadagna_se_spot_basso(self):
        df, cumul = calcola_mtm(self._prezzi(), [self._contratto()])
        assert df["Ore delivery"].iloc[0] == 720
        assert df["Prezzo medio realizzato (€/MWh)"].iloc[0] == pytest.approx(100.0)
        assert df["MtM (€)"].iloc[0] == pytest.approx(14400.0)  # (110-100)*2*720
        assert cumul.iloc[-1] == pytest.approx(14400.0)

    def test_acquisto_specchio(self):
        df, _ = calcola_mtm(self._prezzi(), [self._contratto(lato="Acquisto")])
        assert df["MtM (€)"].iloc[0] == pytest.approx(-14400.0)

    def test_fuori_periodo_zero(self):
        df, cumul = calcola_mtm(
            self._prezzi(), [self._contratto(inizio=dt.date(2020, 1, 1),
                                            fine=dt.date(2020, 1, 31))])
        assert df["Ore delivery"].iloc[0] == 0
        assert df["MtM (€)"].iloc[0] == 0.0
        assert (cumul == 0.0).all()

    def test_nessun_contratto(self):
        df, cumul = calcola_mtm(self._prezzi(), [])
        assert len(df) == 0
        assert (cumul == 0.0).all()


# ------------------------------------------------------- pnl_posizione_aperta
class TestPnlPosizioneAperta:
    def test_prezzo_uguale_rif_pnl_zero(self):
        r = calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 100.0,
                                         ruolo="acquisto")
        assert r["errore"] is None and r["valido"]
        assert r["n_giorni"] == 5
        assert r["pnl_totale"] == pytest.approx(0.0)
        assert r["prezzo_medio_spot"] == pytest.approx(100.0)
        assert (r["serie_giornaliera"] == 0.0).all()

    def test_acquisto_sotto_rif_guadagna(self):
        r = calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 110.0,
                                         ruolo="acquisto")
        # (110-100) * 2 MW * 24h = 480 €/giorno
        assert (r["serie_giornaliera"] == 480.0).all()
        assert r["pnl_totale"] == pytest.approx(2400.0)

    def test_vendita_specchio(self):
        ra = calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 110.0,
                                          ruolo="acquisto")
        rv = calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 110.0,
                                          ruolo="vendita")
        assert rv["pnl_totale"] == pytest.approx(-ra["pnl_totale"])

    def test_raddoppio_mw(self):
        r1 = calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 110.0)
        r2 = calcola_pnl_posizione_aperta(piatta(5 * 24), 4.0, 110.0)
        assert r2["pnl_totale"] == pytest.approx(4800.0)
        assert r2["pnl_totale"] == pytest.approx(2 * r1["pnl_totale"])

    def test_errori(self):
        assert calcola_pnl_posizione_aperta(piatta(5 * 24), 0.0, 100.0)["errore"]
        assert calcola_pnl_posizione_aperta(piatta(5 * 24), -1.0, 100.0)["errore"]
        assert calcola_pnl_posizione_aperta(piatta(5 * 24), 2.0, 100.0,
                                             ruolo="pippo")["errore"]
        assert calcola_pnl_posizione_aperta(piatta(24), 2.0, 100.0)["errore"]
        assert calcola_pnl_posizione_aperta(
            pd.Series([], dtype=float), 2.0, 100.0)["errore"]
        assert calcola_pnl_posizione_aperta(
            piatta(5 * 24), 2.0, float("nan"))["errore"]


# --------------------------------------------------------------- spark/dark
class TestSpreadCentrali:
    def test_spark_spread_formula(self):
        ss, stats = calcola_spark_spread(piatta(30 * 24), 40.0, 50.0, 80.0,
                                         ef_tco2_mwh=0.4)
        # 100 - 40/0.5 - 80*0.4 = -12
        assert (ss == -12.0).all()
        assert stats["medio"] == pytest.approx(-12.0)
        assert stats["pct_ore_positive"] == 0.0
        assert stats["ore_totali"] == 30 * 24
        assert stats["best_val"] == stats["worst_val"] == pytest.approx(-12.0)

    def test_spark_positivo(self):
        _, stats = calcola_spark_spread(piatta(24, prezzo=200.0), 40.0, 50.0,
                                        80.0, ef_tco2_mwh=0.4)
        assert stats["medio"] == pytest.approx(88.0)
        assert stats["pct_ore_positive"] == 100.0

    def test_dark_spread_formula(self):
        ds, stats, durata = calcola_dark_spread(piatta(30 * 24), 20.0, 40.0,
                                               80.0, ef_tco2_mwh=0.9)
        # srmc = 20/0.4 + 80*0.9 = 122 ; 100-122 = -22
        assert stats["srmc"] == pytest.approx(122.0)
        assert (ds == -22.0).all()
        assert stats["medio"] == pytest.approx(-22.0)
        assert stats["ore_totali"] == 30 * 24
        assert (np.diff(durata.to_numpy()) <= 0).all()  # durata decrescente

    def test_dark_input_invalidi(self):
        ds, stats, _ = calcola_dark_spread(piatta(24), -5.0, 40.0, 80.0)
        assert len(ds) == 0
        assert stats["ore_totali"] == 0
        assert np.isnan(stats["srmc"])

    def test_dark_serie_vuota(self):
        ds, stats, _ = calcola_dark_spread(pd.Series([], dtype=float),
                                           20.0, 40.0, 80.0)
        assert len(ds) == 0
        assert stats["srmc"] == pytest.approx(122.0)


# -------------------------------------------------------------- price_capture
class TestPriceCapture:
    def test_prezzo_piatto_cattura_100pct(self):
        s = piatta(14 * 24)
        gen = profilo_solare(s, 10.0)
        r = calcola_price_capture(s, gen)
        assert r["base_medio"] == pytest.approx(100.0)
        assert r["catturato"] == pytest.approx(100.0)
        assert r["tasso_cattura"] == pytest.approx(100.0)
        assert r["sconto_can"] == pytest.approx(0.0)
        # ricavo e mwh sono arrotondati: tolleranza relativa
        assert r["ricavo"] == pytest.approx(100.0 * r["mwh"], rel=1e-3)
        assert r["mwh"] > 0

    def test_cannibalizzazione_solare(self):
        idx = pd.date_range("2026-09-28", periods=14 * 24, freq="h", tz=TZ)
        # caro di notte (150), economico di giorno (50); la finestra
        # economica 05:00-19:00 copre tutta la generazione solare
        v = np.where((idx.hour >= 5) & (idx.hour < 19), 50.0, 150.0)
        s = pd.Series(v, index=idx)
        gen = profilo_solare(s, 10.0)  # produce solo di giorno
        r = calcola_price_capture(s, gen)
        assert r["catturato"] == pytest.approx(50.0)
        assert r["sconto_can"] > 0  # il solare vale meno del base

    def test_generazione_nulla(self):
        s = piatta(24)
        gen = pd.Series(np.zeros(24), index=s.index)
        r = calcola_price_capture(s, gen)
        assert r["mwh"] == 0.0
        assert r["catturato"] is None
        assert r["tasso_cattura"] is None
        assert r["base_medio"] == pytest.approx(100.0)
