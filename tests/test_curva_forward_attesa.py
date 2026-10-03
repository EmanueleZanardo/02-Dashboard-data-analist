"""Test calcola_curva_forward_attesa - tab181 (stile pytest, via appfuncs).

Copertura: serie piatta (fattori 1.0, atteso = base), caso calcolabile a
mano (2 anni: gennaio caro, luglio economico), base None (usa media
annua), parametri non validi (base <= 0, n_mesi fuori range/tipo, banda
invertita), serie vuota (errore pulito), indice non datetime (errore
pulito), media annua non positiva (errore), mese senza storico (errore),
data_inizio custom e default (primo del mese dopo l'ultima ora), NaN e
duplicati (gestiti), tz-aware (reso naive), determinismo, ampiezza e
giudizio (soglie 15/30), registry tab181.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_curva_forward_attesa")
cfa = fns["calcola_curva_forward_attesa"]


def serie(vals, start="2025-01-01"):
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


def serie_2anni():
    """2025-2026: gennaio a 200, luglio a 50, resto a 100."""
    idx = pd.date_range("2025-01-01", "2026-12-31 23:00", freq="h")
    v = np.full(len(idx), 100.0)
    m = idx.month
    v[m == 1] = 200.0
    v[m == 7] = 50.0
    return pd.Series(v, index=idx)


# 2025 e 2026 NON sono bisestili: 730 giorni; gennaio 62gg a 200, luglio 62gg a 50, resto 606gg a 100
MEDIA_2ANNI = (62 * 200.0 + 62 * 50.0 + 606 * 100.0) / 730.0


class TestCurvaForwardAttesa:
    def test_serie_piatta(self):
        r = cfa(serie([100.0] * 8760), prezzo_base=120.0, data_inizio="2026-01-01", n_mesi=12)
        assert r["valido"] and r["errore"] is None
        df = r["df_curva"]
        assert len(df) == 12
        assert (df["Fattore stagionale"] == 1.0).all()
        assert (df["Prezzo atteso (EUR/MWh)"] == 120.0).all()
        assert (df["Banda bassa (EUR/MWh)"] == 120.0).all()
        assert (df["Banda alta (EUR/MWh)"] == 120.0).all()
        assert df["Mese"].tolist() == [f"2026-{m:02d}" for m in range(1, 13)]
        assert r["prezzo_base_usato"] == 120.0
        assert r["ampiezza_eur"] == pytest.approx(0.0)
        assert r["giudizio"] == "CONTENUTA"

    def test_caso_calcolabile_a_mano(self):
        r = cfa(serie_2anni(), prezzo_base=100.0, data_inizio="2027-01-01", n_mesi=12)
        assert r["valido"]
        df = r["df_curva"].set_index("Mese")
        # fattori: 200/media, 50/media, 100/media
        assert df.loc["2027-01", "Fattore stagionale"] == pytest.approx(200.0 / MEDIA_2ANNI, rel=1e-3)
        assert df.loc["2027-07", "Fattore stagionale"] == pytest.approx(50.0 / MEDIA_2ANNI, rel=1e-3)
        assert df.loc["2027-04", "Fattore stagionale"] == pytest.approx(100.0 / MEDIA_2ANNI, rel=1e-3)
        assert df.loc["2027-01", "Prezzo atteso (EUR/MWh)"] == pytest.approx(20000.0 / MEDIA_2ANNI, rel=1e-3)
        assert df.loc["2027-07", "Prezzo atteso (EUR/MWh)"] == pytest.approx(5000.0 / MEDIA_2ANNI, rel=1e-3)
        # bande nulle su blocchi costanti: P10=P90=media del mese
        assert df.loc["2027-01", "Banda bassa (EUR/MWh)"] == pytest.approx(df.loc["2027-01", "Prezzo atteso (EUR/MWh)"])
        assert df.loc["2027-01", "Banda alta (EUR/MWh)"] == pytest.approx(df.loc["2027-01", "Prezzo atteso (EUR/MWh)"])
        # riepilogo
        assert r["mese_piu_caro"]["periodo"] == "Gen 2027"
        assert r["mese_piu_economico"]["periodo"] == "Lug 2027"
        assert r["ampiezza_eur"] == pytest.approx(15000.0 / MEDIA_2ANNI, rel=1e-3)
        # ampiezza % = (200-50) / media dei 12 fattori scalati = 150/104.1667 = 144% -> ALTA
        assert r["ampiezza_pct"] == pytest.approx(144.0, rel=1e-3)
        assert r["giudizio"] == "ALTA"
        assert r["n_anni_storico"] == 2

    def test_base_none_usa_media_annua(self):
        r = cfa(serie_2anni(), data_inizio="2027-01-01", n_mesi=3)
        assert r["valido"]
        assert r["prezzo_base_usato"] == pytest.approx(MEDIA_2ANNI, rel=1e-6)
        df = r["df_curva"].set_index("Mese")
        assert df.loc["2027-01", "Prezzo atteso (EUR/MWh)"] == pytest.approx(200.0, rel=1e-3)

    def test_giudizio_soglie(self):
        # stagionalita' moderata: gennaio 120, resto 100 -> ampiezza 20/104.16 = 19.2%
        idx = pd.date_range("2025-01-01", "2025-12-31 23:00", freq="h")
        v = np.full(len(idx), 100.0)
        v[idx.month == 1] = 120.0
        r = cfa(pd.Series(v, index=idx), prezzo_base=100.0, data_inizio="2026-01-01", n_mesi=12)
        assert r["valido"]
        assert 15.0 <= r["ampiezza_pct"] < 30.0
        assert r["giudizio"] == "MODERATA"

    def test_data_inizio_default(self):
        # senza data_inizio: primo giorno del mese dopo l'ultima ora
        r = cfa(serie_2anni(), prezzo_base=100.0, n_mesi=3)
        assert r["valido"]
        assert r["df_curva"]["Mese"].tolist() == ["2027-01", "2027-02", "2027-03"]

    def test_data_inizio_custom(self):
        r = cfa(serie_2anni(), prezzo_base=100.0, data_inizio="2027-03-15", n_mesi=2)
        assert r["valido"]
        assert r["df_curva"]["Mese"].tolist() == ["2027-03", "2027-04"]
        assert r["df_curva"]["Periodo"].tolist() == ["Mar 2027", "Apr 2027"]

    def test_n_mesi_non_validi(self):
        base = dict(prezzo_base=100.0, data_inizio="2027-01-01")
        for nm in [0, -1, 37, 12.5, "12", True, None]:
            r = cfa(serie_2anni(), n_mesi=nm, **base)
            assert not r["valido"] and r["errore"] is not None, nm

    def test_base_non_valida(self):
        for b in [0.0, -5.0, float("nan"), float("inf"), "x"]:
            r = cfa(serie_2anni(), prezzo_base=b, data_inizio="2027-01-01")
            assert not r["valido"] and r["errore"] is not None, b

    def test_banda_non_valida(self):
        r = cfa(serie_2anni(), q_bassa=90.0, q_alta=10.0)
        assert not r["valido"]
        r = cfa(serie_2anni(), q_bassa=-5.0, q_alta=90.0)
        assert not r["valido"]
        r = cfa(serie_2anni(), q_bassa=10.0, q_alta=150.0)
        assert not r["valido"]

    def test_serie_vuota(self):
        r = cfa(pd.Series(dtype=float))
        assert not r["valido"] and r["errore"] is not None

    def test_indice_non_datetime(self):
        r = cfa(pd.Series([1.0, 2.0, 3.0]))
        assert not r["valido"] and r["errore"] is not None

    def test_media_annua_non_positiva(self):
        r = cfa(serie([-10.0] * 8760), prezzo_base=100.0, data_inizio="2026-01-01")
        assert not r["valido"] and "non positiva" in r["errore"]

    def test_mese_senza_storico(self):
        # solo gennaio-marzo 2026: proiettare aprile -> errore
        idx = pd.date_range("2026-01-01", "2026-03-31 23:00", freq="h")
        p = pd.Series(np.full(len(idx), 100.0), index=idx)
        r = cfa(p, prezzo_base=100.0, data_inizio="2026-01-01", n_mesi=4)
        assert not r["valido"] and "mese 4" in r["errore"]

    def test_nan_duplicati_tz(self):
        p = serie_2anni()
        p.iloc[100] = np.nan
        p = pd.concat([p, p.iloc[[0]]])  # duplicato
        p = p.tz_localize("Europe/Zurich", nonexistent="shift_forward", ambiguous="NaT")
        r = cfa(p, prezzo_base=100.0, data_inizio="2027-01-01", n_mesi=12)
        assert r["valido"]
        assert r["df_curva"]["Mese"].tolist()[0] == "2027-01"
        assert r["mese_piu_caro"]["periodo"] == "Gen 2027"

    def test_determinismo(self):
        a = cfa(serie_2anni(), prezzo_base=97.5, data_inizio="2027-06-01", n_mesi=18)
        b = cfa(serie_2anni(), prezzo_base=97.5, data_inizio="2027-06-01", n_mesi=18)
        assert a["valido"] and b["valido"]
        pd.testing.assert_frame_equal(a["df_curva"], b["df_curva"])
        assert a["ampiezza_pct"] == b["ampiezza_pct"]

    def test_banda_custom_colonne(self):
        r = cfa(serie([100.0] * 72), prezzo_base=100.0, data_inizio="2026-01-01",
                n_mesi=1, q_bassa=5.0, q_alta=95.0)
        assert r["valido"]
        assert r["q_bassa"] == 5.0 and r["q_alta"] == 95.0

    def test_registry_tab181(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "tab181" in src
        assert "with tab181:" in src
        assert "Curva forward attesa" in src
        assert "calcola_curva_forward_attesa" in src
        assert 'key="cfa181_base"' in src and 'key="cfa181_mesi"' in src
        assert 'key="cfa181_inizio"' in src and 'key="cfa181_csv"' in src
