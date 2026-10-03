"""Test calcola_hellbrise - tab169 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (prezzo piatto 100 su
30gg -> 3 giorni HB, sconto 0.0, CONTENUTA; stress con prezzo legato al
fattore giornaliero -> FORTE/MODERATA/CONTENUTA), ore di potenziale
curtailment, casi di errore, robustezza dati (NaN/tz/duplicati),
determinismo, replicazione indipendente del pipeline, registry tab169.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_hellbrise", "profilo_solare", "profilo_eolico")
hb = fns["calcola_hellbrise"]


def serie_mese(valore=100.0, start="2026-01-01", n_giorni=30):
    idx = pd.date_range(start, periods=n_giorni * 24, freq="h")
    return pd.Series(float(valore), index=idx)


def gen_tot(prezzi, cap=100.0):
    return (fns["profilo_solare"](prezzi, cap)
            + fns["profilo_eolico"](prezzi, cap)).astype(float)


def prezzi_da_fattore_giornaliero(base, slope, n_giorni=30):
    """Prezzo orario = base - slope * (fattore_giorno - fattore_medio)."""
    p0 = serie_mese(100.0, n_giorni=n_giorni)
    g = gen_tot(p0)
    fg = g.groupby(g.index.floor("D")).sum() / 24 / 200.0
    arr = (base - slope * (fg - fg.mean())).to_numpy()
    pos = g.index.floor("D").map(
        pd.Series(np.arange(len(fg)), index=fg.index)).to_numpy()
    return pd.Series(arr[pos], index=p0.index), fg


class TestNumeriAMano:
    def test_piatta_100(self):
        # prezzo piatto 100 su 30gg: nessun premio di eccesso
        r = hb(serie_mese(100.0))
        assert r["valido"] and r["errore"] is None
        assert r["n_giorni"] == 30
        assert r["n_hb"] == 3  # miglior decile di 30 giorni
        assert r["quota_hb_pct"] == pytest.approx(10.0)
        assert r["sconto_eur_mwh"] == pytest.approx(0.0)
        assert r["sconto_pct"] == pytest.approx(0.0)
        assert r["prezzo_medio"] == pytest.approx(100.0)
        assert r["prezzo_medio_hb"] == pytest.approx(100.0)
        assert r["giudizio"] == "CANNIBALIZZAZIONE CONTENUTA"
        assert r["tasso_cattura_periodo"] == pytest.approx(100.0)
        assert r["tasso_cattura_hb"] == pytest.approx(100.0)
        assert r["n_ore_curtailment"] == 0
        assert r["mwh_curtailment"] == pytest.approx(0.0)
        assert r["cap_tot_mw"] == pytest.approx(200.0)
        assert r["n_nan_prezzi"] == 0
        assert r["limite_fattore"] == pytest.approx(0.3524, abs=1e-4)
        assert r["peggior_giorno"] is not None
        assert "hellbrise" in r["verdetto"].lower()

    def test_stress_forte_replica_indipendente(self):
        # prezzo crolla nei giorni ad alto fattore: replicazione manuale
        pp, fg = prezzi_da_fattore_giornaliero(100.0, 600.0)
        r = hb(pp)
        lim = float(np.percentile(fg.values, 90.0))
        is_hb = fg >= lim
        assert r["limite_fattore"] == pytest.approx(lim)
        assert r["n_hb"] == int(is_hb.sum())
        assert r["n_giorni"] == len(fg)
        p_g = pp.groupby(pp.index.floor("D")).mean()
        p_hb_att = float(p_g[is_hb].mean())
        sconto_att = float(p_g.mean()) - p_hb_att
        assert r["prezzo_medio_hb"] == pytest.approx(p_hb_att)
        assert r["sconto_eur_mwh"] == pytest.approx(sconto_att)
        assert r["sconto_pct"] == pytest.approx(
            sconto_att / float(p_g.mean()) * 100.0)
        assert r["giudizio"] == "CANNIBALIZZAZIONE FORTE"
        # giorni HB ordinati: prezzo medio HB < media periodo
        assert r["prezzo_medio_hb"] < r["prezzo_medio"]
        assert r["peggior_giorno"] == p_g[is_hb].idxmin()

    def test_stress_moderata(self):
        pp, _ = prezzi_da_fattore_giornaliero(100.0, 400.0)
        r = hb(pp)
        assert r["valido"]
        assert r["sconto_eur_mwh"] == pytest.approx(11.0, abs=0.05)
        assert r["giudizio"] == "CANNIBALIZZAZIONE MODERATA"

    def test_stress_contenuta(self):
        pp, _ = prezzi_da_fattore_giornaliero(100.0, 150.0)
        r = hb(pp)
        assert r["valido"]
        assert r["sconto_eur_mwh"] == pytest.approx(4.13, abs=0.05)
        assert r["giudizio"] == "CANNIBALIZZAZIONE CONTENUTA"

    def test_curtailment_negativi(self):
        # ore ad alto fattore orario con prezzo negativo -> curtailment
        p0 = serie_mese(100.0)
        g = gen_tot(p0)
        p3 = pd.Series(50.0, index=p0.index)
        p3[g / 200.0 >= 0.8] = -5.0
        r = hb(p3)
        assert r["valido"]
        assert r["n_ore_curtailment"] == 6
        assert r["quota_ore_curtailment_pct"] == pytest.approx(6 / 720 * 100)
        assert r["mwh_curtailment"] == pytest.approx(1024.1, abs=0.5)
        # le ore curtailment sono un sottoinsieme delle ore analizzate
        assert r["n_ore_curtailment"] <= 720

    def test_soglia_curtailment_personalizzata(self):
        p0 = serie_mese(100.0)
        r1 = hb(p0, soglia_curtail_pct=100.0, prezzo_curtail=200.0)
        r2 = hb(p0, soglia_curtail_pct=50.0, prezzo_curtail=200.0)
        assert r1["n_ore_curtailment"] <= r2["n_ore_curtailment"]

    def test_percentile_75_allarga(self):
        p0 = serie_mese(100.0)
        r90 = hb(p0, percentile_hb=90.0)
        r75 = hb(p0, percentile_hb=75.0)
        assert r75["n_hb"] >= r90["n_hb"]

    def test_tabella_mensile(self):
        idx = pd.date_range("2026-01-15", periods=60 * 24, freq="h")
        r = hb(pd.Series(100.0, index=idx))
        tm = r["tabella_mensile"]
        assert len(tm) == 3  # gennaio + febbraio + marzo
        assert list(tm["Mese"]) == ["2026-01", "2026-02", "2026-03"]
        assert tm["Giorni hellbrise"].sum() == r["n_hb"]
        assert tm["Giorni totali"].sum() == 60


class TestErrori:
    def test_percentile_fuori_range(self):
        p0 = serie_mese()
        assert not hb(p0, percentile_hb=40.0)["valido"]
        assert not hb(p0, percentile_hb=100.0)["valido"]
        assert not hb(p0, percentile_hb=np.nan)["valido"]

    def test_soglia_curtailment_fuori_range(self):
        p0 = serie_mese()
        assert not hb(p0, soglia_curtail_pct=0.0)["valido"]
        assert not hb(p0, soglia_curtail_pct=110.0)["valido"]

    def test_capacita_non_positive(self):
        p0 = serie_mese()
        assert not hb(p0, cap_fv_mw=0.0)["valido"]
        assert not hb(p0, cap_eolico_mw=-5.0)["valido"]

    def test_min_giorni(self):
        p0 = serie_mese()
        r = hb(p0, min_giorni=1)
        assert not r["valido"] and "almeno 2" in r["errore"]

    def test_serie_troppo_corta(self):
        idx = pd.date_range("2026-01-01", periods=2, freq="h")
        r = hb(pd.Series([1.0, 2.0], index=idx))
        assert not r["valido"] and "7 giorni" in r["errore"]

    def test_serie_vuota(self):
        r = hb(pd.Series(dtype=float))
        assert not r["valido"]

    def test_indice_non_datetime(self):
        r = hb(pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2]))
        assert not r["valido"]

    def test_input_non_serie(self):
        assert not hb([1, 2, 3])["valido"]

    def test_prezzo_curtail_nan(self):
        p0 = serie_mese()
        assert not hb(p0, prezzo_curtail=np.nan)["valido"]


class TestRobustezza:
    def test_nan_scartati_e_contati(self):
        p0 = serie_mese(100.0)
        p0.iloc[10:15] = np.nan
        r = hb(p0)
        assert r["valido"]
        assert r["n_nan_prezzi"] == 5
        assert r["sconto_eur_mwh"] == pytest.approx(0.0)

    def test_tz_aware(self):
        p0 = serie_mese(100.0).tz_localize("Europe/Zurich")
        r = hb(p0)
        assert r["valido"] and r["n_giorni"] == 30

    def test_duplicati_keep_first(self):
        p0 = serie_mese(100.0)
        dup = pd.concat([p0, p0.iloc[[0]]])
        r = hb(dup)
        assert r["valido"] and r["n_giorni"] == 30

    def test_determinismo(self):
        pp, _ = prezzi_da_fattore_giornaliero(100.0, 400.0)
        r1 = hb(pp)
        r2 = hb(pp)
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["tabella_mensile"].equals(r2["tabella_mensile"])
        assert r1["serie_fattore"].equals(r2["serie_fattore"])


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab169_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        # appartenenza + sequenza senza buchi (non conteggio esatto)
        assert "tab169" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab169" in withs
        assert len(withs) == len(dvars) >= 169
        assert '"🌞 Hellbrise"' in src
        keys = re.findall(r'key="(hb169_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 6
        assert re.search(r"^def calcola_hellbrise\(", src, re.M) is not None
