"""Test calcola_dunkelflaute - tab168 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (premio di scarsita',
giudizi RILEVANTE/MODERATO/LIMITATO, replicazione manuale indipendente del
pipeline, tabella mensile), casi di errore, robustezza dati
(NaN/tz/duplicati), determinismo, registry tab168.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_dunkelflaute", "profilo_solare", "profilo_eolico")
dk = fns["calcola_dunkelflaute"]
p_fv = fns["profilo_solare"]
p_eo = fns["profilo_eolico"]


def serie_piatta(val=100.0, start="2026-01-01", n_giorni=30):
    idx = pd.date_range(start, periods=24 * n_giorni, freq="h")
    return pd.Series(float(val), index=idx)


def serie_anticorrelata(k, start="2026-01-01", n_giorni=30):
    """Prezzo alto nei giorni con poco vento/sole: stress costruito."""
    idx = pd.date_range(start, periods=24 * n_giorni, freq="h")
    base = serie_piatta(100.0, start, n_giorni)
    sf = dk(base)["serie_fattore"]
    fh = sf.reindex(idx, method="ffill").to_numpy()
    return pd.Series(40.0 + k * (1.0 - fh), index=idx)


class TestNumeriAMano:
    def test_prezzo_piatto_premio_zero(self):
        # prezzo piatto -> i giorni DF costano come la media: premio 0
        r = dk(serie_piatta())
        assert r["valido"] and r["errore"] is None
        assert r["n_giorni"] == 30
        assert r["n_df"] == 3  # peggior decile su 30 giorni
        assert r["quota_df_pct"] == pytest.approx(10.0)
        assert r["prezzo_medio"] == pytest.approx(100.0)
        assert r["prezzo_medio_df"] == pytest.approx(100.0)
        assert r["premio_eur_mwh"] == pytest.approx(0.0)
        assert r["premio_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "LIMITATO"
        assert r["limite_fattore"] == pytest.approx(0.30955, abs=1e-4)
        assert r["fattore_medio_df"] == pytest.approx(0.29775, abs=1e-4)
        assert r["peggior_giorno"] in set(r["giorni_df"])
        assert len(r["serie_fattore"]) == 30
        assert len(r["serie_prezzo_g"]) == 30
        assert len(r["tabella_mensile"]) == 1
        assert r["tabella_mensile"].iloc[0]["Mese"] == "2026-01"
        assert "premio di scarsita' +0.00" in r["verdetto"]

    def test_replicazione_manuale(self):
        # replica indipendente del pipeline: stessi KPI dell'helper
        prezzi = serie_piatta()
        r = dk(prezzi)
        idx = prezzi.index
        giorni = idx.floor("D")
        gen = (pd.to_numeric(p_fv(prezzi, 100.0), errors="coerce").fillna(0.0)
               + pd.to_numeric(p_eo(prezzi, 100.0), errors="coerce").fillna(0.0))
        en_g = gen.groupby(giorni).sum()
        p_g = prezzi.groupby(giorni).mean()
        fattore = en_g / (giorni.value_counts().sort_index() * 200.0)
        lim = float(np.percentile(fattore.values, 10.0))
        is_df = fattore <= lim
        assert r["n_df"] == int(is_df.sum())
        assert r["limite_fattore"] == pytest.approx(lim)
        assert r["prezzo_medio_df"] == pytest.approx(float(p_g[is_df].mean()))
        assert r["premio_eur_mwh"] == pytest.approx(float(p_g[is_df].mean() - p_g.mean()))
        assert r["fattore_medio_df"] == pytest.approx(float(fattore[is_df].mean()))
        assert r["peggior_giorno"] == p_g[is_df].idxmax()
        tm = r["tabella_mensile"]
        assert tm.iloc[0]["Giorni dunkelflaute"] == int(is_df.sum())
        assert tm.iloc[0]["Giorni totali"] == 30
        assert tm["Giorni dunkelflaute"].sum() == r["n_df"]

    def test_premio_rilevante(self):
        r = dk(serie_anticorrelata(800))
        assert r["valido"]
        assert r["premio_eur_mwh"] == pytest.approx(24.30, abs=0.05)
        assert r["giudizio"] == "RILEVANTE"
        assert r["prezzo_medio_df"] > r["prezzo_medio"]
        assert "premio di scarsita'" in r["verdetto"]

    def test_premio_moderato(self):
        r = dk(serie_anticorrelata(250))
        assert r["valido"]
        assert r["premio_eur_mwh"] == pytest.approx(7.59, abs=0.05)
        assert r["giudizio"] == "MODERATO"

    def test_confini_giudizio(self):
        # premio esattamente 0 -> LIMITATO; costruzione con prezzi DF noti
        r = dk(serie_piatta())
        assert r["premio_eur_mwh"] == 0.0 and r["giudizio"] == "LIMITATO"

    def test_tabella_mensile_tre_mesi(self):
        r = dk(serie_piatta(start="2026-01-15", n_giorni=60))
        assert r["n_giorni"] == 60
        tm = r["tabella_mensile"]
        assert tm["Mese"].tolist() == ["2026-01", "2026-02", "2026-03"]
        assert tm["Giorni totali"].sum() == 60
        assert tm["Giorni dunkelflaute"].sum() == r["n_df"]

    def test_percentile_piu_alto_piu_giorni(self):
        p = serie_piatta()
        r10 = dk(p, percentile_df=10.0)
        r25 = dk(p, percentile_df=25.0)
        assert r25["n_df"] > r10["n_df"]
        assert r25["limite_fattore"] > r10["limite_fattore"]


class TestErrori:
    @pytest.mark.parametrize("bad", [None, [1, 2, 3], "x"])
    def test_input_non_validi(self, bad):
        r = dk(bad)
        assert not r["valido"] and r["errore"]

    def test_serie_vuota(self):
        r = dk(pd.Series(dtype=float))
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        a = pd.Series([1.0, 2.0, 3.0], index=["x", "y", "z"])
        r = dk(a)
        assert not r["valido"] and r["errore"]

    def test_troppo_pochi_giorni(self):
        r = dk(serie_piatta(n_giorni=3))
        assert not r["valido"] and "almeno 7 giorni" in r["errore"]

    def test_min_giorni_non_valido(self):
        r = dk(serie_piatta(), min_giorni=1)
        assert not r["valido"] and r["errore"]

    def test_capacita_non_valide(self):
        p = serie_piatta()
        for kw in [dict(cap_fv_mw=0), dict(cap_fv_mw=-5), dict(cap_eolico_mw=0)]:
            r = dk(p, **kw)
            assert not r["valido"] and r["errore"]

    def test_percentile_non_valido(self):
        p = serie_piatta()
        for bad in [0, -5, 60, "x", float("nan")]:
            r = dk(p, percentile_df=bad)
            assert not r["valido"] and r["errore"]

    def test_solo_nan(self):
        idx = pd.date_range("2026-01-01", periods=24 * 10, freq="h")
        r = dk(pd.Series(np.nan, index=idx))
        assert not r["valido"] and r["errore"]


class TestRobustezza:
    def test_nan_prezzi_scartati_e_contati(self):
        p = serie_piatta()
        p.iloc[0:6] = np.nan
        r = dk(p)
        assert r["valido"]
        assert r["n_nan_prezzi"] == 6
        assert r["n_giorni"] == 30

    def test_tz_aware(self):
        idx = pd.date_range("2026-01-01", periods=24 * 30, freq="h",
                            tz="Europe/Rome")
        p = pd.Series(100.0, index=idx)
        r = dk(p)
        assert r["valido"]
        assert r["n_giorni"] == 30
        assert r["n_df"] == 3
        assert r["premio_eur_mwh"] == pytest.approx(0.0)

    def test_duplicati_keep_first(self):
        p = serie_piatta()
        dup = pd.concat([p, p.iloc[[0]]])
        r = dk(dup)
        assert r["valido"]
        assert r["n_giorni"] == 30
        assert r["n_df"] == 3

    def test_determinismo(self):
        p = serie_anticorrelata(800)
        r1, r2 = dk(p), dk(p)
        for k in ["n_df", "premio_eur_mwh", "fattore_medio_df", "giudizio",
                  "limite_fattore", "verdetto"]:
            assert r1[k] == r2[k]
        assert r1["tabella_mensile"].equals(r2["tabella_mensile"])
        assert r1["serie_fattore"].equals(r2["serie_fattore"])


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab168_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        # appartenenza + sequenza senza buchi (non conteggio esatto)
        assert "tab168" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        assert len(dvars) >= 168
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab168" in withs
        assert len(withs) == len(dvars)
        assert '"🌫️ Dunkelflaute"' in src
        keys = re.findall(r'key="(df168_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 4
        assert re.search(r"^def calcola_dunkelflaute\(", src, re.M) is not None
