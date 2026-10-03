"""Test calcola_diversita_carico - tab167 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (fattore di diversita',
picco coincidente, somma picchi, risparmio quota potenza, tabella per sito
e mensile), casi di errore, robustezza dati (NaN/tz/duplicati), DataFrame
input, determinismo, registry tab167.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_diversita_carico")
dv = fns["calcola_diversita_carico"]

# replica locale dei pesi di profilo (self-contained per l'estrazione via AST)
PESI = {
    "piatto": [1.0] * 24,
    "diurno": [0.625] * 7 + [1.25] * 14 + [0.625] * 3,
    "notturno": [1.25] * 7 + [0.625] * 14 + [1.25] * 3,
    "uffici": [0.3] * 7 + [0.8, 1.1] + [1.3] * 9 + [1.0, 0.7, 0.5, 0.4] + [0.3] * 2,
}


def serie_piatta(mw, start="2026-01-05", n=48):
    idx = pd.date_range(start, periods=n, freq="h")
    return pd.Series(float(mw), index=idx)


def serie_forma(mw, forma, start="2026-01-05", n=48):
    w = np.asarray(PESI[forma], dtype=float)
    w = w / w.mean()
    idx = pd.date_range(start, periods=n, freq="h")
    return pd.Series(float(mw) * w[idx.hour.to_numpy()], index=idx)


class TestNumeriAMano:
    def test_nessuna_diversita_piatti(self):
        # A=10 piatto, B=5 piatto su 48h -> picchi coincidenti sempre
        r = dv({"A": serie_piatta(10), "B": serie_piatta(5)})
        assert r["valido"] and r["errore"] is None
        assert r["n_siti"] == 2 and r["n_ore"] == 48
        assert r["picco_coincidente_mw"] == pytest.approx(15.0)
        assert r["somma_picchi_mw"] == pytest.approx(15.0)
        assert r["fattore_diversita"] == pytest.approx(1.0)
        assert r["fattore_coincidenza"] == pytest.approx(1.0)
        assert r["giudizio"] == "BASSA"
        assert r["ora_picco"] == pd.Timestamp("2026-01-05 00:00")
        assert r["kw_risparmiati"] == pytest.approx(0.0)
        assert r["risparmio_eur_anno"] == pytest.approx(0.0)
        t = r["tabella"]
        ra = t[t["Sito"] == "A"].iloc[0]
        assert ra["Picco individuale (MW)"] == pytest.approx(10.0)
        assert ra["Energia (MWh)"] == pytest.approx(480.0)
        assert ra["Fattore di carico (%)"] == pytest.approx(100.0)
        assert ra["Contributo al picco coincidente (%)"] == pytest.approx(66.7, abs=0.05)
        assert ra["Quota energia (%)"] == pytest.approx(66.7, abs=0.05)
        assert len(r["tabella_mensile"]) == 1
        assert r["tabella_mensile"].iloc[0]["Mese"] == "2026-01"
        assert r["tabella_mensile"].iloc[0]["Fattore di diversita'"] == pytest.approx(1.0)

    def test_diversita_diurno_notturno(self):
        # A diurno 10 MW, B notturno 6 MW -> picchi sfalsati
        # A: picco 10*1.25/0.9895833 = 12.6316 (ore 7-20), notte 6.3158
        # B: picco 6*1.25/0.8854167 = 8.4706 (ore 0-6,21-23), giorno 4.2353
        # portafoglio giorno 16.8669 / notte 14.7864 -> picco coincidente 16.8669
        r = dv({"A": serie_forma(10, "diurno"), "B": serie_forma(6, "notturno")}, 60.0)
        assert r["valido"]
        assert r["picco_coincidente_mw"] == pytest.approx(16.8669, abs=1e-3)
        assert r["somma_picchi_mw"] == pytest.approx(21.1022, abs=1e-3)
        assert r["fattore_diversita"] == pytest.approx(1.2511, abs=1e-3)
        assert r["fattore_coincidenza"] == pytest.approx(1 / 1.2511013215859033, abs=1e-6)
        assert r["giudizio"] == "ALTA"
        assert r["ora_picco"] == pd.Timestamp("2026-01-05 07:00")
        assert r["kw_risparmiati"] == pytest.approx(4235.3, abs=0.5)
        assert r["risparmio_eur_anno"] == pytest.approx(254117.0, abs=30.0)
        t = r["tabella"]
        assert t[t["Sito"] == "A"].iloc[0]["Picco individuale (MW)"] == pytest.approx(12.632, abs=1e-3)
        assert t[t["Sito"] == "B"].iloc[0]["Picco individuale (MW)"] == pytest.approx(8.471, abs=1e-3)
        assert t[t["Sito"] == "A"].iloc[0]["Contributo al picco coincidente (%)"] == pytest.approx(74.9, abs=0.05)
        assert t[t["Sito"] == "B"].iloc[0]["Contributo al picco coincidente (%)"] == pytest.approx(25.1, abs=0.05)
        assert "ALTA" in r["verdetto"] and "A" in r["verdetto"]
        assert len(r["serie_portafoglio"]) == 48

    def test_tre_siti_piatti(self):
        r = dv({"A": serie_piatta(10), "B": serie_piatta(5), "C": serie_piatta(2)})
        assert r["valido"]
        assert r["fattore_diversita"] == pytest.approx(1.0)
        assert r["picco_coincidente_mw"] == pytest.approx(17.0)
        assert r["giudizio"] == "BASSA"

    def test_quota_zero(self):
        r = dv({"A": serie_piatta(10), "B": serie_piatta(5)},
               quota_potenza_eur_kw_anno=0.0)
        assert r["valido"]
        assert r["risparmio_eur_anno"] == pytest.approx(0.0)

    def test_dataframe_input(self):
        df = pd.DataFrame({"A": serie_piatta(10), "B": serie_piatta(5)})
        r = dv(df)
        assert r["valido"]
        assert r["fattore_diversita"] == pytest.approx(1.0)
        assert r["picco_coincidente_mw"] == pytest.approx(15.0)


class TestErrori:
    @pytest.mark.parametrize("bad", [
        None, {}, {"solo": None}, {"A": serie_piatta(10)},
    ])
    def test_input_non_validi(self, bad):
        siti = {"A": serie_piatta(10)} if bad == {"solo": None} else bad
        if bad == {"solo": None}:
            siti = {"A": serie_piatta(10)}
        r = dv(siti)
        assert not r["valido"] and r["errore"]

    def test_nomi_duplicati(self):
        df = pd.DataFrame(np.ones((48, 2)), columns=["X", "X"],
                          index=pd.date_range("2026-01-05", periods=48, freq="h"))
        # DataFrame con colonne duplicate: i nomi strippati collidono
        r = dv({"X": serie_piatta(5), " X ": serie_piatta(5)})
        assert not r["valido"] and "duplicati" in r["errore"]

    def test_nome_vuoto(self):
        r = dv({"": serie_piatta(5), "B": serie_piatta(5)})
        assert not r["valido"] and r["errore"]

    def test_carichi_negativi(self):
        s = serie_piatta(5)
        s.iloc[3] = -1.0
        r = dv({"A": s, "B": serie_piatta(5)})
        assert not r["valido"] and "negativi" in r["errore"]

    def test_sito_fermo(self):
        r = dv({"A": serie_piatta(0), "B": serie_piatta(5)})
        assert not r["valido"] and "energia nulla" in r["errore"]

    def test_poche_ore_in_comune(self):
        a = serie_piatta(5, start="2026-01-05", n=48)
        b = serie_piatta(5, start="2026-01-07", n=48)
        r = dv({"A": a, "B": b})
        assert not r["valido"] and "ore in comune" in r["errore"]

    def test_indice_non_datetime(self):
        a = pd.Series([1.0, 2.0, 3.0], index=["x", "y", "z"])
        r = dv({"A": a, "B": a})
        assert not r["valido"] and r["errore"]

    def test_quota_negativa(self):
        r = dv({"A": serie_piatta(5), "B": serie_piatta(5)}, quota_potenza_eur_kw_anno=-1)
        assert not r["valido"] and r["errore"]

    def test_min_ore_non_valido(self):
        r = dv({"A": serie_piatta(5), "B": serie_piatta(5)}, min_ore=1)
        assert not r["valido"] and r["errore"]

    def test_tipo_input_sbagliato(self):
        r = dv([serie_piatta(5), serie_piatta(5)])
        assert not r["valido"] and r["errore"]


class TestRobustezza:
    def test_nan_diventano_zero(self):
        a = serie_piatta(10)
        a.iloc[0:6] = np.nan  # 6 ore fermo
        r = dv({"A": a, "B": serie_piatta(5)})
        assert r["valido"]
        assert r["tabella"][r["tabella"]["Sito"] == "A"].iloc[0]["Ore con NaN"] == 6
        assert r["tabella"][r["tabella"]["Sito"] == "A"].iloc[0]["Energia (MWh)"] == pytest.approx(420.0)

    def test_tz_aware(self):
        idx = pd.date_range("2026-01-05", periods=48, freq="h", tz="Europe/Rome")
        a = pd.Series(10.0, index=idx)
        b = pd.Series(5.0, index=idx.tz_localize(None))
        r = dv({"A": a, "B": b})
        assert r["valido"]
        assert r["fattore_diversita"] == pytest.approx(1.0)

    def test_duplicati_keep_first(self):
        a = serie_piatta(10)
        dup = pd.concat([a, a.iloc[[0]]])  # duplicato dell'ora 0
        r = dv({"A": dup, "B": serie_piatta(5)})
        assert r["valido"]
        assert r["n_ore"] == 48

    def test_determinismo(self):
        siti = {"A": serie_forma(10, "diurno"), "B": serie_forma(6, "notturno")}
        r1 = dv(siti, 60.0)
        r2 = dv(siti, 60.0)
        assert r1["fattore_diversita"] == r2["fattore_diversita"]
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["tabella"].equals(r2["tabella"])


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab167_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        # appartenenza + sequenza senza buchi (non conteggio esatto)
        assert "tab167" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab167" in withs
        assert len(withs) == len(dvars) >= 167
        assert '"🔌 Diversità di carico"' in src
        keys = re.findall(r'key="(dv167_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 4
        # chiavi dinamiche per sito (f-string): nome/mw/forma
        for k in ["dv167_nome{i}", "dv167_mw{i}", "dv167_forma{i}"]:
            assert ('key=f"%s"' % k) in src
        assert re.search(r"^def calcola_diversita_carico\(", src, re.M) is not None
