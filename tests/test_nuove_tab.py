"""Test tab 132-134 (stile pytest): volatilita' intraday (Parkinson),
regimi di prezzo, report di periodo + CSV.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("fascia_oraria", "calcola_volatilita_intraday",
          "calcola_regimi_prezzo", "calcola_riepilogo_periodo",
          "genera_csv_report", "calcola_premio_rischio")
calcola_volatilita_intraday = _F["calcola_volatilita_intraday"]
calcola_regimi_prezzo = _F["calcola_regimi_prezzo"]
calcola_riepilogo_periodo = _F["calcola_riepilogo_periodo"]
genera_csv_report = _F["genera_csv_report"]
calcola_premio_rischio = _F["calcola_premio_rischio"]

TZ = "Europe/Zurich"


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


def onda(giorni, base=100.0, amp=30.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    g = np.arange(len(idx)) // 24  # indice giorno 0..N-1
    # onda intraday + drift quadratico (medie giornaliere non lineari)
    v = base + amp * np.sin(2 * np.pi * (idx.hour - 6) / 24) + 5.0 * g + 0.3 * g ** 2
    return pd.Series(v, index=idx, name="p")


# ------------------------------------------------------- volatilita' intraday
class TestVolatilitaIntraday:
    def test_piatta_parkinson_none(self):
        r = calcola_volatilita_intraday(piatta(5))
        g = r["giornaliera"]
        assert len(g) == 5
        # h == l -> Parkinson indefinito (nessun giorno valido)
        assert r["giorni_validi_park"] == 0
        assert r["parkinson"] is None
        assert r["range_medio"] == 0.0
        assert r["range_max"] == 0.0
        assert r["cc_vol"] == pytest.approx(0.0)
        assert r["rapporto"] is None
        assert len(r["profilo_ampiezza_oraria"]) == 24
        assert len(r["top_movimenti_orari"]) == 10

    def test_onda_parkinson_positivo(self):
        r = calcola_volatilita_intraday(onda(5))
        assert r["giorni_validi_park"] == 5
        assert r["parkinson"] is not None and r["parkinson"] > 0
        # formula di Parkinson sul giorno: sqrt(ln(H/L)^2 / (4 ln2));
        # l'aggregato e' la RMS sui giorni (H/L varia col drift)
        base_d = [100.0 + 5.0 * d + 0.3 * d ** 2 for d in range(5)]
        attesi = [np.sqrt((np.log((b + 30.0) / (b - 30.0)) ** 2)
                           / (4.0 * np.log(2.0)))
                  for b in base_d]
        assert r["parkinson"] == pytest.approx(
            round(float(np.sqrt(np.mean(np.square(attesi)))), 2), abs=0.01)
        assert r["range_medio"] == pytest.approx(60.0)
        assert r["range_max"] == pytest.approx(60.0)
        assert r["giorno_range_max"] == "2026-09-28"  # primo a pari merito
        assert r["rapporto"] is not None

    def test_meno_di_48_ore_vuoto(self):
        r = calcola_volatilita_intraday(piatta(1))  # 24 ore
        assert len(r["giornaliera"]) == 0
        assert r["parkinson"] is None
        assert r["giorni_validi_park"] == 0

    def test_giorno_negativo_escluso(self):
        s = onda(5)
        s.iloc[2 * 24:3 * 24] = -10.0  # terzo giorno tutto negativo
        r = calcola_volatilita_intraday(s)
        assert r["giorni_validi_park"] == 4  # il giorno negativo escluso
        assert r["parkinson"] is not None
        assert len(r["giornaliera"]) == 5  # ma resta in tabella

    def test_serie_vuota(self):
        r = calcola_volatilita_intraday(pd.Series([], dtype=float))
        assert len(r["giornaliera"]) == 0
        assert r["parkinson"] is None


# ------------------------------------------------------------ regimi di prezzo
class TestRegimiPrezzo:
    def _tre_livelli(self):
        # 10 gg @80, 10 gg @100, 10 gg @120
        idx = pd.date_range("2026-09-28", periods=30 * 24, freq="h", tz=TZ)
        v = np.concatenate([np.full(10 * 24, 80.0),
                            np.full(10 * 24, 100.0),
                            np.full(10 * 24, 120.0)])
        return pd.Series(v, index=idx)

    def test_tre_regimi(self):
        r = calcola_regimi_prezzo(self._tre_livelli())
        assert r["ok"] is True
        assert len(r["giornaliera"]) == 30
        assert set(r["giornaliera"]["Regime"]) == {"Basso", "Medio", "Alto"}
        t = r["tabella_regimi"]
        assert len(t) == 3
        assert t["Giorni"].sum() == 30

    def test_matrice_righe_sommano_a_uno(self):
        r = calcola_regimi_prezzo(self._tre_livelli())
        cont = r["matrice_conteggi"]
        prob = r["matrice_prob"]
        assert cont.values.sum() == 29  # 30 giorni -> 29 transizioni
        for regime in ("Basso", "Medio", "Alto"):
            if cont.loc[regime].sum() > 0:
                assert prob.loc[regime].sum() == pytest.approx(1.0)

    def test_stazionaria_somma_uno(self):
        r = calcola_regimi_prezzo(self._tre_livelli())
        assert r["stazionaria"].sum() == pytest.approx(1.0, abs=1e-3)
        assert (r["stazionaria"] >= 0).all()

    def test_regime_corrente(self):
        r = calcola_regimi_prezzo(self._tre_livelli())
        assert r["regime_corrente"] == "Alto"
        assert r["giorni_regime_corrente"] == 10
        assert r["prob_resta_corrente"] == pytest.approx(1.0)

    def test_pochi_giorni_non_ok(self):
        assert calcola_regimi_prezzo(piatta(8))["ok"] is False

    def test_prezzo_piatto_non_ok(self):
        # terzili non calcolabili su serie costante
        assert calcola_regimi_prezzo(piatta(30))["ok"] is False

    def test_deterministico(self):
        s = self._tre_livelli()
        a = calcola_regimi_prezzo(s)
        b = calcola_regimi_prezzo(s)
        assert a["giornaliera"].equals(b["giornaliera"])
        assert a["matrice_prob"].equals(b["matrice_prob"])


# ---------------------------------------------------------- report di periodo
class TestRiepilogoPeriodo:
    def test_piatta(self):
        r = calcola_riepilogo_periodo(piatta(14))
        assert r["ok"] is True
        k = r["kpi"]
        assert k["ore"] == 353
        assert k["giorni"] == 14
        assert k["medio"] == pytest.approx(100.0)
        assert k["mediano"] == pytest.approx(100.0)
        assert k["std"] == pytest.approx(0.0)
        assert k["min"] == k["max"] == pytest.approx(100.0)
        assert k["quota_negativi"] == pytest.approx(0.0)
        assert k["baseload_1MW"] == pytest.approx(33600.0)
        assert len(r["mensile"]) == 2            # set + ott
        assert r["mensile"]["Ore"].sum() == 353
        assert list(r["fasce"]["Fascia"]) == ["F1", "F2", "F3"]
        assert r["fasce"]["Ore"].sum() == 353
        assert len(r["giorni"]) == 14
        assert r["giorni"]["Range (€/MWh)"].sum() == 0.0
        assert list(r["settimanale"]["Giorno settimana"]) == \
            ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
        assert r["settimanale"]["Ore"].sum() == 353

    def test_serie_vuota(self):
        r = calcola_riepilogo_periodo(pd.Series([], dtype=float))
        assert r["ok"] is False
        assert r["kpi"] == {}

    def test_quota_negativi(self):
        s = piatta(14)
        s.iloc[::24] = -5.0
        r = calcola_riepilogo_periodo(s)
        assert r["kpi"]["quota_negativi"] == pytest.approx(100.0 / 24, abs=0.05)
        assert r["kpi"]["min"] == pytest.approx(-5.0)

    def test_csv_report(self):
        r = calcola_riepilogo_periodo(piatta(14))
        csv = genera_csv_report(r, "2026-09-28", "2026-10-11")
        assert isinstance(csv, str)
        for sezione in ("# SEZIONE;KPI", "# SEZIONE;MENSILE", "# SEZIONE;FASCE",
                        "# SEZIONE;SETTIMANALE", "# SEZIONE;GIORNI"):
            assert sezione in csv
        assert "336" in csv  # ore analizzate
        assert "2026-09-28" in csv and "2026-10-11" in csv


# ------------------------------------------------------------ premio di rischio
class TestPremioRischio:
    def _sei_mesi(self, prezzi, tz=None):
        idx = pd.date_range("2026-04-01", "2026-09-30 23:00", freq="h", tz=tz)
        assert len(idx) == len(prezzi)
        return pd.Series(prezzi, index=idx)

    def test_piatta_premio_zero(self):
        s = self._sei_mesi(np.full(183 * 24, 100.0))
        r = calcola_premio_rischio(s)
        assert r["ok"] is True
        assert r["n_mesi"] == 3  # lug, ago, set (servono 3 mesi di formazione)
        assert r["premio_medio_base"] == pytest.approx(0.0)
        assert r["premio_medio_peak"] == pytest.approx(0.0)
        assert r["quota_mesi_positivi"] == pytest.approx(0.0)
        assert list(r["df"]["Mese consegna"]) == ["2026-07", "2026-08", "2026-09"]
        assert (r["df"]["Premio Base (€/MWh)"] == 0.0).all()

    def test_trend_crescente_premio_negativo(self):
        # spot in salita: il proxy (media passata) sta sotto il realizzato
        n = 183 * 24
        s = self._sei_mesi(80.0 + 60.0 * np.arange(n) / n)
        r = calcola_premio_rischio(s)
        assert r["ok"] is True
        assert r["premio_medio_base"] < 0
        assert r["mese_ultimo"] == "2026-09"

    def test_serie_vuota(self):
        r = calcola_premio_rischio(pd.Series([], dtype=float))
        assert r["ok"] is False
        assert r["n_mesi"] == 0

    def test_deterministico(self):
        s = self._sei_mesi(np.full(183 * 24, 100.0))
        a = calcola_premio_rischio(s)
        b = calcola_premio_rischio(s)
        assert a["df"].equals(b["df"])
        assert a["premio_medio_base"] == b["premio_medio_base"]

    def test_tz_aware_non_sollevato(self):
        # i dati mock dell'app sono tz-aware (Europe/Zurich): la tab non
        # deve sollevare eccezioni (docstring: "mai eccezioni")
        s = self._sei_mesi(np.full(183 * 24, 100.0), tz=TZ)
        r = calcola_premio_rischio(s)
        assert r["ok"] is True
        assert r["n_mesi"] == 3
