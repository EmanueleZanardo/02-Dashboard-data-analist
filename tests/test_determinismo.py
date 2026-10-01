"""Test determinismo (stile pytest).

I grafici dell'app devono essere riproducibili: i generatori Monte Carlo e i
mock usano seed fissi, gli helper di ottimizzazione sono deterministici a
parita' di input. Qui si verifica che due chiamate identiche diano risultati
identici, e che seed diversi diano risultati diversi.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("fascia_oraria", "generate_mock_hourly", "calcola_ventaglio_prezzo",
          "calcola_rischio_quanto", "profilo_solare",
          "calcola_ora_punta_giornaliera", "calcola_efficienza_profilo",
          "calcola_finestra_ottimale")
generate_mock_hourly = _F["generate_mock_hourly"]
calcola_ventaglio_prezzo = _F["calcola_ventaglio_prezzo"]
calcola_rischio_quanto = _F["calcola_rischio_quanto"]
profilo_solare = _F["profilo_solare"]
calcola_ora_punta_giornaliera = _F["calcola_ora_punta_giornaliera"]
calcola_efficienza_profilo = _F["calcola_efficienza_profilo"]
calcola_finestra_ottimale = _F["calcola_finestra_ottimale"]

TZ = "Europe/Zurich"


def mock_60gg():
    # 60 giorni con variabilita' (serve sigma > 0 ai Monte Carlo)
    return generate_mock_hourly("2026-01-01", "2026-03-01")


def deep_equal(a, b):
    """Uguaglianza ricorsiva per i dict ritornati dagli helper."""
    if isinstance(a, pd.DataFrame) and isinstance(b, pd.DataFrame):
        return a.equals(b)
    if isinstance(a, pd.Series) and isinstance(b, pd.Series):
        return a.equals(b)
    if isinstance(a, dict) and isinstance(b, dict):
        return (set(a) == set(b)
                and all(deep_equal(a[k], b[k]) for k in a))
    if isinstance(a, float) and isinstance(b, float):
        return (a == b) or (np.isnan(a) and np.isnan(b))
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(deep_equal(x, y)
                                        for x, y in zip(a, b))
    return a == b


class TestMockHourly:
    def test_due_chiamate_identice(self):
        a = generate_mock_hourly("2026-01-01", "2026-01-31")
        b = generate_mock_hourly("2026-01-01", "2026-01-31")
        assert a.equals(b)

    def test_struttura(self):
        s = generate_mock_hourly("2026-01-01", "2026-01-31")
        assert len(s) == 31 * 24
        assert str(s.index.tz) == TZ
        assert (s >= 5.0).all()  # clip a 5 €/MWh
        assert s.name == "Prezzo Spot (€/MWh)"

    def test_weekend_scontato(self):
        s = generate_mock_hourly("2026-01-01", "2026-02-28")
        we = s[s.index.weekday >= 5].mean()
        wd = s[s.index.weekday < 5].mean()
        assert we < wd  # sconto weekend nel generatore


class TestVentaglioDeterministico:
    def test_stesso_seed_stesso_risultato(self):
        p = mock_60gg()
        a = calcola_ventaglio_prezzo(p, n_giorni=30, n_scenari=200, seed=42)
        b = calcola_ventaglio_prezzo(p, n_giorni=30, n_scenari=200, seed=42)
        assert a["errore"] is None
        assert a["df_bande"].equals(b["df_bande"])
        assert a["p50_fine"] == b["p50_fine"]

    def test_seed_diverso_risultato_diverso(self):
        p = mock_60gg()
        a = calcola_ventaglio_prezzo(p, n_giorni=30, n_scenari=200, seed=42)
        c = calcola_ventaglio_prezzo(p, n_giorni=30, n_scenari=200, seed=43)
        assert not a["df_bande"].equals(c["df_bande"])


class TestRischioQuantoDeterministico:
    def test_stesso_seed_stesso_risultato(self):
        p = mock_60gg()
        kw = dict(n_giorni=30, n_scenari=200, seed=42)
        a = calcola_rischio_quanto(p, **kw)
        b = calcola_rischio_quanto(p, **kw)
        assert a["errore"] is None
        assert a["costi_scenari"] == b["costi_scenari"]
        assert a["df_sensibilita"].equals(b["df_sensibilita"])
        assert a["var95"] == b["var95"]


class TestProfiliDeterministici:
    def test_solare_due_chiamate_identice(self):
        idx = pd.date_range("2026-01-01", periods=30 * 24, freq="h", tz=TZ)
        s = pd.Series(np.full(len(idx), 100.0), index=idx)
        assert profilo_solare(s, 10.0).equals(profilo_solare(s, 10.0))

    def test_solare_notte_zero_e_potenza_zero(self):
        idx = pd.date_range("2026-06-01", periods=24, freq="h", tz=TZ)
        s = pd.Series(np.full(24, 100.0), index=idx)
        g = profilo_solare(s, 10.0)
        assert g.iloc[0] == 0.0      # mezzanotte: notte
        assert g.max() <= 10.0
        assert g.max() > 0.0         # giugno: giorno lungo
        assert (profilo_solare(s, 0.0) == 0.0).all()
        assert (profilo_solare(s, -5.0) == 0.0).all()


class TestOttimizzazioniDeterministiche:
    def _prezzi(self):
        return generate_mock_hourly("2026-09-28", "2026-10-11")

    def test_ora_punta_identica(self):
        s = self._prezzi()
        a = calcola_ora_punta_giornaliera(s, 2.0, 1.5, 1.0)
        b = calcola_ora_punta_giornaliera(s, 2.0, 1.5, 1.0)
        assert deep_equal(a, b)

    def test_ora_punta_prezzi_piatti(self):
        # a parita' di costo vince l'ora piu' piccola (argmax deterministico)
        idx = pd.date_range("2026-09-28", periods=14 * 24, freq="h", tz=TZ)
        s = pd.Series(np.full(len(idx), 100.0), index=idx)
        r = calcola_ora_punta_giornaliera(s, 1.0, 1.0, 1.0)
        assert r["ora_moda"] == 0
        assert r["giorni"] == 14

    def test_efficienza_profilo_identica(self):
        s = self._prezzi()
        a = calcola_efficienza_profilo(s, 2.0, 1.5, 1.0)
        b = calcola_efficienza_profilo(s, 2.0, 1.5, 1.0)
        assert deep_equal(a, b)

    def test_finestra_ottimale_identica(self):
        s = self._prezzi()
        a = calcola_finestra_ottimale(s, 2.0, 1.5, 1.0, n_ore=4)
        b = calcola_finestra_ottimale(s, 2.0, 1.5, 1.0, n_ore=4)
        assert deep_equal(a, b)
