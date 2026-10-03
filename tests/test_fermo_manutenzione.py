"""Test calcola_finestra_fermo_consumo - tab176 (stile pytest, via appfuncs).

Copre: numeri calcolabili a mano su prezzi piatti (fasce F1/F2/F3),
carico residuo, clamp della durata, prezzi negativi (la finestra ottimale
li evita), casi di errore, robustezza dati (NaN/tz/duplicati),
determinismo, registry tab176.
"""
import re

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_finestra_fermo_consumo", "fascia_oraria")
calcola = _F["calcola_finestra_fermo_consumo"]

TZ = "Europe/Zurich"


def serie(valori, start="2026-01-05", tz=None):
    idx = pd.date_range(start, periods=len(valori), freq="h", tz=tz)
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


def piatta(giorni=7, prezzo=100.0, start="2026-01-05", tz=None):
    return serie([prezzo] * (giorni * 24), start=start, tz=tz)


# ------------------------------------------------------------------ numeri a mano
class TestNumeriAMano:
    def test_finestra_migliore_peggiore_piatta(self):
        # 7 giorni da lunedi', prezzo piatto 100: lun-ven evitano 3100/giorno,
        # sabato 2000, domenica 1200 (F1=11h, F2=5h, F3=8h nei feriali).
        p = piatta(7, 100.0)
        r = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=2, carico_residuo_pct=0.0)
        assert r["valido"] and r["errore"] is None
        assert r["best"]["costo_evitato"] == 6200.0
        assert r["worst"]["costo_evitato"] == 3200.0
        assert str(r["best"]["inizio"]) == "2026-01-05"  # lun-mar, a parita' vince la prima
        assert str(r["best"]["fine"]) == "2026-01-06"
        assert str(r["worst"]["inizio"]) == "2026-01-10"  # sab-dom
        assert r["costo_cattiva_pianificazione"] == 3000.0
        assert r["costo_totale"] == 18700.0
        assert r["quota_best_pct"] == 6200.0 / 18700.0 * 100.0
        assert r["durata_gg"] == 2 and r["giorni"] == 7
        # coerenza: somma giornaliera == totale, finestre ordinate desc
        assert r["df_giorni"]["Costo evitato (EUR)"].sum() == 18700.0
        ev = r["df_finestre"]["Costo evitato (EUR)"].to_numpy()
        assert (np.diff(ev) <= 0).all()

    def test_carico_residuo_dimezza(self):
        p = piatta(7, 100.0)
        r = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=2, carico_residuo_pct=50.0)
        assert r["valido"]
        assert r["best"]["costo_evitato"] == 3100.0
        assert r["df_giorni"]["Energia evitata (MWh)"].sum() == (11 * 2 + 5 * 1 + 8 * 0.5) * 5 * 0.5 + (16 * 1 + 8 * 0.5) * 0.5 + 24 * 0.5 * 0.5

    def test_durata_clampata_al_periodo(self):
        p = piatta(5, 100.0)
        r = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=30, carico_residuo_pct=0.0)
        assert r["valido"]
        assert r["durata_gg"] == 5
        assert r["best"]["costo_evitato"] == r["costo_totale"] == 5 * 3100.0

    def test_prezzi_negativi_evitate(self):
        # giorno 1 a +100, giorno 2 a -10: fermarsi il giorno 2 fa PERDERE soldi
        vals = [100.0] * 24 + [-10.0] * 24
        p = serie(vals)
        r = calcola(p, 1.0, 1.0, 1.0, giorni_fermo=1, carico_residuo_pct=0.0)
        assert r["valido"]
        assert str(r["best"]["inizio"]) == "2026-01-05"
        assert r["best"]["costo_evitato"] == 2400.0
        assert r["worst"]["costo_evitato"] == -240.0
        assert r["costo_cattiva_pianificazione"] == 2640.0


# ------------------------------------------------------------------ errori
class TestErrori:
    def test_serie_vuota(self):
        r = calcola(pd.Series(dtype=float), 1.0, 1.0, 1.0)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        r = calcola(pd.Series([1.0, 2.0, 3.0]), 1.0, 1.0, 1.0)
        assert not r["valido"] and r["errore"]

    def test_carico_nullo(self):
        r = calcola(piatta(3), 0.0, 0.0, 0.0)
        assert not r["valido"] and "Carico nullo" in r["errore"]

    def test_durata_non_valida(self):
        r = calcola(piatta(3), 1.0, 1.0, 1.0, giorni_fermo=0)
        assert not r["valido"] and r["errore"]

    def test_residuo_non_valido(self):
        r = calcola(piatta(3), 1.0, 1.0, 1.0, carico_residuo_pct=100.0)
        assert not r["valido"] and r["errore"]
        r2 = calcola(piatta(3), 1.0, 1.0, 1.0, carico_residuo_pct=-5.0)
        assert not r2["valido"] and r2["errore"]

    def test_tutti_nan(self):
        r = calcola(serie([np.nan] * 48), 1.0, 1.0, 1.0)
        assert not r["valido"] and r["errore"]


# ------------------------------------------------------------------ robustezza
class TestRobustezza:
    def test_nan_scartati(self):
        vals = [100.0] * 48
        vals[5] = np.nan
        p = serie(vals)
        r = calcola(p, 1.0, 1.0, 1.0, giorni_fermo=1, carico_residuo_pct=0.0)
        assert r["valido"]
        assert r["giorni"] == 2

    def test_duplicati_keep_first(self):
        p = piatta(2, 100.0)
        dup = pd.concat([p, p.iloc[[0]]])
        r = calcola(dup, 1.0, 1.0, 1.0, giorni_fermo=1, carico_residuo_pct=0.0)
        assert r["valido"] and r["giorni"] == 2

    def test_tz_aware(self):
        p = piatta(3, 100.0, tz=TZ)
        r = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=2, carico_residuo_pct=0.0)
        assert r["valido"] and r["best"]["costo_evitato"] == 6200.0

    def test_determinismo(self):
        p = piatta(10, 80.0)
        a = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=3, carico_residuo_pct=10.0)
        b = calcola(p, 2.0, 1.0, 0.5, giorni_fermo=3, carico_residuo_pct=10.0)
        assert a["best"] == b["best"] and a["worst"] == b["worst"]
        assert a["df_finestre"].equals(b["df_finestre"])
        assert a["costo_cattiva_pianificazione"] == b["costo_cattiva_pianificazione"]


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab176_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab176" in dvars
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(dvars) == len(withs)
        assert '"🛠️ Fermo manutenzione"' in src
        keys = re.findall(r'key="(fm176_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 3
        assert re.search(r"^def calcola_finestra_fermo_consumo\(", src, re.M) is not None
