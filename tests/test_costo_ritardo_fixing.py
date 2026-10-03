"""Test calcola_costo_ritardo_fixing - tab182 (stile pytest, via appfuncs).

Copertura: serie con rampa settimanale calcolabile a mano (5 settimane
100/110/120/130/140, k=2 -> Delta=[20,20,20]), serie piatta (Delta=0,
giudizio CONTENUTA), giudizio MODERATO/ALTO/NON VALUTABILE, parametri non
validi (k: 0/-1/27/2.5/"4"/True/None; soglia: negativa/NaN/inf/"x"/True),
serie troppo corta (errore con conteggio settimane), serie vuota, indice non
datetime, NaN/duplicati/tz (gestiti), determinismo, curva del rimpianto
(colonne, E|Delta| >= |media Delta|, P90 monotono su rampa), soglia custom,
registry tab182.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_costo_ritardo_fixing")
crf = fns["calcola_costo_ritardo_fixing"]


def serie_rampa(settimane=5, base=100.0, passo=10.0, start="2025-01-06"):
    """Settimane intere lun-dom con prezzo orario costante per settimana."""
    vals = []
    for w in range(settimane):
        vals.extend([base + w * passo] * 168)
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


class TestCostoRitardoBase:
    def test_rampa_a_mano(self):
        # medie settimanali [100,110,120,130,140], k=2 -> Delta=[20,20,20]
        r = crf(serie_rampa(), settimane_attesa=2, soglia_eur=5.0)
        assert r["valido"] and r["errore"] is None
        assert r["n_settimane"] == 5 and r["n_oss"] == 3
        assert r["costo_atteso"] == pytest.approx(20.0)
        assert r["mediana_delta"] == pytest.approx(20.0)
        assert r["p10"] == pytest.approx(20.0) and r["p90"] == pytest.approx(20.0)
        assert r["prob_risparmio"] == pytest.approx(0.0)
        assert r["prob_sopra_soglia"] == pytest.approx(1.0)
        assert r["max_rimpianto"] == pytest.approx(20.0)
        assert r["max_risparmio"] == pytest.approx(20.0)
        assert r["prezzo_medio_settimanale"] == pytest.approx(120.0)
        assert r["giudizio"] == "CONTENUTA"  # spread P90-P10 = 0
        d = r["df_delta"]
        assert d["Variazione (EUR/MWh)"].tolist() == [20.0, 20.0, 20.0]

    def test_rampa_inversa_risparmio(self):
        # prezzi in calo: aspettare fa risparmiare -> prob 1.0, costo negativo
        r = crf(serie_rampa(base=140.0, passo=-10.0), settimane_attesa=2)
        assert r["valido"]
        assert r["costo_atteso"] == pytest.approx(-20.0)
        assert r["prob_risparmio"] == pytest.approx(1.0)
        assert r["max_risparmio"] == pytest.approx(-20.0)

    def test_serie_piatta(self):
        idx = pd.date_range("2025-01-06", periods=4 * 168, freq="h")
        r = crf(pd.Series(np.full(len(idx), 100.0), index=idx), settimane_attesa=1)
        assert r["valido"]
        assert r["costo_atteso"] == pytest.approx(0.0)
        assert r["p10"] == pytest.approx(0.0) and r["p90"] == pytest.approx(0.0)
        assert r["giudizio"] == "CONTENUTA"

    def test_giudizio_soglie(self):
        rng = np.random.default_rng(11)
        # rumore settimanale alternato +-40 su base 100 -> spread alto
        vals = []
        for w in range(12):
            vals.extend([100.0 + (40.0 if w % 2 == 0 else -40.0)] * 168)
        idx = pd.date_range("2025-01-06", periods=len(vals), freq="h")
        r = crf(pd.Series(vals, index=idx), settimane_attesa=1)
        assert r["valido"]
        # Delta a k=1: +-80 -> P90-P10 = 160 su media 100 = 160% -> ALTO
        assert r["giudizio"] == "ALTO"
        assert r["spread_p90_p10_pct"] == pytest.approx(160.0)
        _ = rng  # seed documentato, serie deterministica

    def test_giudizio_non_valutabile(self):
        idx = pd.date_range("2025-01-06", periods=4 * 168, freq="h")
        r = crf(pd.Series(np.full(len(idx), -5.0), index=idx), settimane_attesa=1)
        assert r["valido"]
        assert r["giudizio"] == "NON VALUTABILE"
        assert r["costo_atteso"] == pytest.approx(0.0)

    def test_curva_rimpianto(self):
        r = crf(serie_rampa(settimane=5), settimane_attesa=2)
        assert r["valido"]
        c = r["df_curva_rimpianto"]
        # n_sett=5 -> k_max = min(26, 3) = 3
        assert c["Settimane di attesa"].tolist() == [1, 2, 3]
        # rampa lineare: E|Delta_k| = 10*k
        assert c["Costo atteso |Delta| (EUR/MWh)"].tolist() == pytest.approx([10.0, 20.0, 30.0])
        assert c["P90 Delta (EUR/MWh)"].tolist() == pytest.approx([10.0, 20.0, 30.0])
        assert c["Media Delta (EUR/MWh)"].tolist() == pytest.approx([10.0, 20.0, 30.0])
        # E|Delta| >= |media Delta| sempre
        assert (c["Costo atteso |Delta| (EUR/MWh)"].abs()
                >= c["Media Delta (EUR/MWh)"].abs() - 1e-9).all()

    def test_curva_rimpianto_clamp(self):
        # 30 settimane -> k_max = 26
        r = crf(serie_rampa(settimane=30), settimane_attesa=4)
        assert r["valido"]
        c = r["df_curva_rimpianto"]
        assert c["Settimane di attesa"].tolist() == list(range(1, 27))

    def test_soglia_custom(self):
        r = crf(serie_rampa(), settimane_attesa=2, soglia_eur=25.0)
        assert r["valido"] and r["soglia_eur"] == 25.0
        assert r["prob_sopra_soglia"] == pytest.approx(0.0)  # Delta=20 < 25
        r2 = crf(serie_rampa(), settimane_attesa=2, soglia_eur=0.0)
        assert r2["valido"] and r2["prob_sopra_soglia"] == pytest.approx(1.0)


class TestCostoRitardoErrori:
    def test_k_non_validi(self):
        base = serie_rampa()
        for k in [0, -1, 27, 100, 2.5, "4", True, None]:
            r = crf(base, settimane_attesa=k)
            assert not r["valido"] and r["errore"] is not None, k

    def test_soglia_non_valida(self):
        base = serie_rampa()
        for s in [-1.0, float("nan"), float("inf"), "x", True, None]:
            r = crf(base, soglia_eur=s)
            assert not r["valido"] and r["errore"] is not None, s

    def test_serie_troppo_corta(self):
        # 3 settimane con k=2: servono k+2=4 -> errore con conteggio
        r = crf(serie_rampa(settimane=3), settimane_attesa=2)
        assert not r["valido"] and "3" in r["errore"] and "4" in r["errore"]

    def test_serie_vuota(self):
        r = crf(pd.Series(dtype=float))
        assert not r["valido"] and r["errore"] is not None

    def test_indice_non_datetime(self):
        r = crf(pd.Series([1.0, 2.0, 3.0]))
        assert not r["valido"] and r["errore"] is not None

    def test_nan_duplicati_tz(self):
        p = serie_rampa(settimane=6)
        p.iloc[50] = np.nan
        p = pd.concat([p, p.iloc[[0]]])
        p = p.tz_localize("Europe/Zurich", nonexistent="shift_forward", ambiguous="NaT")
        r = crf(p, settimane_attesa=2)
        assert r["valido"]
        assert r["n_settimane"] == 6 and r["n_oss"] == 4
        assert r["costo_atteso"] == pytest.approx(20.0)

    def test_determinismo(self):
        a = crf(serie_rampa(settimane=8), settimane_attesa=3, soglia_eur=7.5)
        b = crf(serie_rampa(settimane=8), settimane_attesa=3, soglia_eur=7.5)
        assert a["valido"] and b["valido"]
        pd.testing.assert_frame_equal(a["df_delta"], b["df_delta"])
        pd.testing.assert_frame_equal(a["df_curva_rimpianto"], b["df_curva_rimpianto"])
        assert a["costo_atteso"] == b["costo_atteso"]


class TestRegistryTab182:
    def test_tab182_registrata(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab182" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab182" in withs
        assert len(withs) == len(dvars) >= 182
        assert '"⏳ Costo del ritardo"' in src
        assert "calcola_costo_ritardo_fixing" in src
        keys = re.findall(r'key="(rdf182_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 3
