"""Test calcola_orologio_prezzo - tab179 (stile pytest, via appfuncs).

Orologio del prezzo: profilo orario medio per mese (matrice 12x24),
ora piu' economica/cara e spread giorno/notte per mese, ora migliore/
peggiore su media annua. Casi: serie piatta, numeri calcolabili a mano,
serie vuota/corta/indice non datetime, NaN/duplicati, serie su 2 mesi,
determinismo, replica indipendente, registry tab179.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_orologio_prezzo")
orologio = _F["calcola_orologio_prezzo"]

TZ = "Europe/Zurich"


def serie(vals, start="2026-01-01"):
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=TZ)
    return pd.Series(np.asarray(vals, dtype=float), index=idx, name="p")


class TestOrologioPrezzo:
    def test_piatta_30gg(self):
        r = orologio(serie([100.0] * 720))
        assert r["valido"] and r["errore"] is None
        assert len(r["df_matrice"]) == 12 * 24
        assert len(r["df_mesi"]) == 1  # solo gennaio
        assert r["df_mesi"]["Mese"].tolist() == [1]
        assert r["df_mesi"]["Spread (EUR/MWh)"].iloc[0] == pytest.approx(0.0)
        # a parita' di prezzo, argmin/argmax -> prima occorrenza (ora 0)
        assert r["ora_migliore_anno"] == 0
        assert r["ora_peggiore_anno"] == 0
        assert r["spread_medio_mensile"] == pytest.approx(0.0)
        assert r["mese_spread_max"] == 1
        assert r["prezzo_medio_annuo"] == pytest.approx(100.0)
        assert r["n_ore"] == 720
        assert r["mesi_presenti"] == [1]

    def test_numeri_a_mano(self):
        # 2 giorni: ora 0 -> 50, ora 12 -> 150, resto 100
        vals = []
        for _ in range(2):
            g = [100.0] * 24
            g[0] = 50.0
            g[12] = 150.0
            vals.extend(g)
        r = orologio(serie(vals))
        assert r["valido"]
        m = r["df_matrice"]
        assert m.loc[(m["Mese"] == 1) & (m["Ora del giorno"] == 0),
                     "Prezzo medio (EUR/MWh)"].iloc[0] == pytest.approx(50.0)
        assert m.loc[(m["Mese"] == 1) & (m["Ora del giorno"] == 12),
                     "Prezzo medio (EUR/MWh)"].iloc[0] == pytest.approx(150.0)
        assert m.loc[(m["Mese"] == 1) & (m["Ora del giorno"] == 7),
                     "Prezzo medio (EUR/MWh)"].iloc[0] == pytest.approx(100.0)
        s = r["df_mesi"].iloc[0]
        assert s["Mese"] == 1
        assert s["Ora più economica"] == 0
        assert s["Prezzo min (EUR/MWh)"] == pytest.approx(50.0)
        assert s["Ora più cara"] == 12
        assert s["Prezzo max (EUR/MWh)"] == pytest.approx(150.0)
        assert s["Spread (EUR/MWh)"] == pytest.approx(100.0)
        assert r["ora_migliore_anno"] == 0
        assert r["ora_peggiore_anno"] == 12
        # media annua: (50 + 150 + 22*100) / 24
        assert r["prezzo_medio_annuo"] == pytest.approx((50 + 150 + 2200) / 24)

    def test_due_mesi(self):
        # gennaio a 80 piatto, febbraio a 120 piatto
        vals = [80.0] * (31 * 24) + [120.0] * (28 * 24)
        r = orologio(serie(vals, start="2026-01-01"))
        assert r["valido"]
        assert r["mesi_presenti"] == [1, 2]
        assert len(r["df_mesi"]) == 2
        g = r["df_mesi"].set_index("Mese")
        assert g.loc[1, "Prezzo min (EUR/MWh)"] == pytest.approx(80.0)
        assert g.loc[2, "Prezzo min (EUR/MWh)"] == pytest.approx(120.0)
        assert g.loc[1, "Spread (EUR/MWh)"] == pytest.approx(0.0)
        # profilo annuo: ogni ora media (80+120)/2 = 100
        assert r["ora_migliore_anno"] == 0
        assert r["prezzo_medio_annuo"] == pytest.approx(
            (80.0 * 31 * 24 + 120.0 * 28 * 24) / (59 * 24))

    def test_serie_vuota(self):
        r = orologio(pd.Series([], dtype=float,
                               index=pd.DatetimeIndex([], tz=TZ), name="p"))
        assert not r["valido"] and r["errore"]
        assert len(r["df_matrice"]) == 0 and len(r["df_mesi"]) == 0

    def test_serie_troppo_corta(self):
        r = orologio(serie([100.0] * 23))
        assert not r["valido"] and "24" in r["errore"]

    def test_indice_non_datetime(self):
        r = orologio(pd.Series([100.0] * 48, index=range(48), name="p"))
        assert not r["valido"] and r["errore"]

    def test_nan_e_duplicati(self):
        vals = [100.0] * 48
        vals[5] = np.nan
        vals[10] = np.nan
        s = serie(vals)
        s = pd.concat([s, s.iloc[[20]]])  # duplicato ora 20
        r = orologio(s)
        assert r["valido"]
        assert r["n_ore"] == 46  # 48 - 2 NaN (duplicato keep-first)
        assert r["prezzo_medio_annuo"] == pytest.approx(100.0)

    def test_determinismo(self):
        rng = np.random.default_rng(7)
        s = serie(rng.uniform(30, 200, 24 * 90))
        r1, r2 = orologio(s), orologio(s)
        pd.testing.assert_frame_equal(r1["df_matrice"], r2["df_matrice"])
        pd.testing.assert_frame_equal(r1["df_mesi"], r2["df_mesi"])
        assert r1["ora_migliore_anno"] == r2["ora_migliore_anno"]

    def test_replica_indipendente(self):
        # profilo a gradino: ore 0-7 a 60, ore 8-23 a 140, 10 giorni
        vals = []
        for _ in range(10):
            vals.extend([60.0] * 8 + [140.0] * 16)
        r = orologio(serie(vals))
        assert r["valido"]
        s = r["df_mesi"].iloc[0]
        assert s["Ora più economica"] == 0
        assert s["Ora più cara"] == 8  # prima occorrenza del max
        assert s["Spread (EUR/MWh)"] == pytest.approx(80.0)
        assert r["ora_migliore_anno"] == 0
        assert r["ora_peggiore_anno"] == 8
        assert r["spread_medio_mensile"] == pytest.approx(80.0)

    def test_registry_tab179(self):
        src = Path(__file__).resolve().parent.parent / "app.py"
        txt = src.read_text(encoding="utf-8")
        assert "tab179" in txt
        assert "Orologio del prezzo" in txt
        assert "calcola_orologio_prezzo" in txt
        assert 'key="op179_mesi"' in txt and 'key="op179_csv"' in txt
