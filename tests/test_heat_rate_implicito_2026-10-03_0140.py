"""Test calcola_heat_rate_implicito - tab166 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (IHR clean/lordo, regimi,
efficienza implicita, tabella mensile), confini di soglia, ore scartate,
casi di errore, robustezza dati (NaN/tz/duplicati), determinismo,
registry tab166.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_heat_rate_implicito")
ihr = fns["calcola_heat_rate_implicito"]

# replica locale delle soglie di regime (self-contained per l'estrazione via AST)
REGIMI = [
    (1.50, "Rinnovabili/nucleare sul margine"),
    (2.00, "CCGT moderno sul margine"),
    (2.50, "Gas a media efficienza"),
    (3.20, "OCGT / picco gas"),
    (float("inf"), "Scarsita' / premio di scarsita'"),
]


def serie_48h(prezzo=100.0, start="2026-01-05"):
    idx = pd.date_range(start, periods=48, freq="h")
    return pd.Series(float(prezzo), index=idx)


class TestNumeriAMano:
    def test_scenario_a_piatto_100(self):
        # 48h piatte a 100, G=40, E=80, ef=0.4 -> num=68 -> IHR=1.7
        r = ihr(serie_48h(), 40.0, 80.0, 0.4)
        assert r["valido"] and r["errore"] is None
        assert r["medio"] == pytest.approx(1.7, abs=1e-9)
        assert r["mediana"] == pytest.approx(1.7, abs=1e-9)
        assert r["minimo"] == pytest.approx(1.7, abs=1e-9)
        assert r["massimo"] == pytest.approx(1.7, abs=1e-9)
        assert r["medio_lordo"] == pytest.approx(2.5, abs=1e-9)
        assert r["eff_implicita_pct"] == pytest.approx(58.8, abs=1e-9)
        assert r["ore_valide"] == 48 and r["ore_totali"] == 48
        assert r["ore_scartate"] == 0
        assert r["regime_dominante"] == "CCGT moderno sul margine"
        assert r["quote_regimi"]["CCGT moderno sul margine"] == pytest.approx(100.0)
        assert r["quota_scarsita"] == pytest.approx(0.0)
        assert "CCGT moderno sul margine" in r["verdetto"]
        assert len(r["serie_ihr"]) == 48
        assert r["serie_ihr"].name == "Heat rate implicito (MWh_th/MWh_e)"
        m = r["tabella_mensile"]
        assert len(m) == 1 and m.iloc[0]["Mese"] == "2026-01"
        assert m.iloc[0]["Ore valide"] == 48
        assert m.iloc[0]["Heat rate implicito medio"] == pytest.approx(1.70, abs=1e-9)
        assert m.iloc[0]["Efficienza implicita (%)"] == pytest.approx(58.8, abs=0.05)
        assert m.iloc[0]["Regime dominante"] == "CCGT moderno sul margine"
        assert m.iloc[0]["Scarsita' (%)"] == pytest.approx(0.0)

    def test_regimi_tutti(self):
        # G=40, E=0, ef=0.4 -> IHR = P/40
        # P: 40 -> 1.0 rinnovabili | 68 -> 1.7 CCGT | 88 -> 2.2 media eff.
        #    108 -> 2.7 OCGT | 140 -> 3.5 scarsita'
        vals = [40.0] * 24 + [68.0] * 24 + [88.0] * 24 + [108.0] * 24 + [140.0] * 24
        idx = pd.date_range("2026-01-05", periods=120, freq="h")
        p = pd.Series(vals, index=idx)
        r = ihr(p, 40.0, 0.0, 0.4)
        assert r["valido"]
        assert r["regime_dominante"] in [n for _, n in REGIMI]  # pareggio 5x24
        q = r["quote_regimi"]
        for _, nome in REGIMI:
            assert q[nome] == pytest.approx(20.0, abs=1e-9)
        assert r["quota_scarsita"] == pytest.approx(20.0, abs=1e-9)
        assert r["medio"] == pytest.approx((1.0 + 1.7 + 2.2 + 2.7 + 3.5) / 5, abs=1e-9)
        # pareggio: verdetto cita comunque un regime esistente
        assert any(n in r["verdetto"] for _, n in REGIMI)
        assert "premio di scarsita'" in r["verdetto"]  # 20% >= 10% -> nota scarsita'

    def test_confini_soglia(self):
        # G=100, E=0 -> IHR = P/100; confini esatti
        casi = [(149.0, "Rinnovabili/nucleare sul margine"),
                (150.0, "CCGT moderno sul margine"),
                (199.0, "CCGT moderno sul margine"),
                (200.0, "Gas a media efficienza"),
                (249.0, "Gas a media efficienza"),
                (250.0, "OCGT / picco gas"),
                (319.0, "OCGT / picco gas"),
                (320.0, "Scarsita' / premio di scarsita'")]
        for prezzo, atteso in casi:
            r = ihr(serie_48h(prezzo), 100.0, 0.0, 0.4)
            assert r["valido"], prezzo
            assert r["regime_dominante"] == atteso, (prezzo, r["regime_dominante"])

    def test_ore_scartate_parziali(self):
        # 24h a 100 (IHR 1.7) + 24h a 20 (num=20-32<0 -> scartate)
        idx = pd.date_range("2026-01-05", periods=48, freq="h")
        p = pd.Series([100.0] * 24 + [20.0] * 24, index=idx)
        r = ihr(p, 40.0, 80.0, 0.4)
        assert r["valido"]
        assert r["ore_valide"] == 24 and r["ore_scartate"] == 24
        assert r["ore_totali"] == 48
        assert r["medio"] == pytest.approx(1.7, abs=1e-9)

    def test_tutte_scartate(self):
        r = ihr(serie_48h(20.0), 40.0, 80.0, 0.4)  # num < 0 ovunque
        assert not r["valido"] and "insufficienti" in r["errore"]

    def test_verdetto_eff_alta(self):
        # prezzo basso -> IHR 0.45, eff 222% -> nota eff > 66.7%
        r = ihr(serie_48h(50.0), 40.0, 80.0, 0.4)
        assert r["valido"]
        assert r["regime_dominante"] == "Rinnovabili/nucleare sul margine"
        assert r["medio"] == pytest.approx(0.45, abs=1e-9)
        assert "66.7%" in r["verdetto"]


class TestErrori:
    def test_prezzi_none(self):
        r = ihr(None, 40.0, 80.0)
        assert not r["valido"] and r["errore"] is not None

    def test_prezzi_non_serie(self):
        r = ihr([100.0] * 48, 40.0, 80.0)
        assert not r["valido"]

    def test_indice_non_datetime(self):
        p = pd.Series([100.0] * 48)
        r = ihr(p, 40.0, 80.0)
        assert not r["valido"] and "datetime" in r["errore"]

    def test_serie_vuota(self):
        p = pd.Series([], index=pd.DatetimeIndex([]), dtype=float)
        r = ihr(p, 40.0, 80.0)
        assert not r["valido"]

    def test_gas_non_positivo(self):
        r = ihr(serie_48h(), 0.0, 80.0)
        assert not r["valido"] and "gas" in r["errore"]
        r2 = ihr(serie_48h(), -5.0, 80.0)
        assert not r2["valido"]

    def test_co2_negativo(self):
        r = ihr(serie_48h(), 40.0, -1.0)
        assert not r["valido"] and "CO2" in r["errore"]

    def test_ef_non_positivo(self):
        r = ihr(serie_48h(), 40.0, 80.0, 0.0)
        assert not r["valido"]

    def test_parametri_non_numerici(self):
        r = ihr(serie_48h(), "abc", 80.0)
        assert not r["valido"] and "non numerici" in r["errore"]

    def test_serie_troppo_corta(self):
        idx = pd.date_range("2026-01-05", periods=10, freq="h")
        r = ihr(pd.Series(100.0, index=idx), 40.0, 80.0, min_ore=24)
        assert not r["valido"] and "insufficienti" in r["errore"]

    def test_non_numerica(self):
        idx = pd.date_range("2026-01-05", periods=48, freq="h")
        p = pd.Series(["x"] * 48, index=idx)
        r = ihr(p, 40.0, 80.0)
        assert not r["valido"]  # tutto NaN dopo to_numeric


class TestRobustezza:
    def test_nan_scartati(self):
        p = serie_48h()
        p.iloc[5] = np.nan
        r = ihr(p, 40.0, 80.0, 0.4)
        assert r["valido"] and r["ore_totali"] == 47 and r["ore_valide"] == 47

    def test_tz_aware(self):
        idx = pd.date_range("2026-01-05", periods=48, freq="h", tz="Europe/Rome")
        r = ihr(pd.Series(100.0, index=idx), 40.0, 80.0, 0.4)
        assert r["valido"] and r["medio"] == pytest.approx(1.7, abs=1e-9)

    def test_duplicati_keep_first(self):
        p = serie_48h()
        dup = pd.concat([p, p.iloc[[0]]])
        r = ihr(dup, 40.0, 80.0, 0.4)
        assert r["valido"] and r["ore_totali"] == 48

    def test_mensile_due_mesi(self):
        p = pd.concat([serie_48h(100.0, "2026-01-30"), serie_48h(100.0, "2026-02-27")])
        r = ihr(p, 40.0, 80.0, 0.4)
        assert r["valido"]
        assert list(r["tabella_mensile"]["Mese"]) == ["2026-01", "2026-02"]

    def test_determinismo(self):
        p = serie_48h()
        ra, rb = ihr(p, 40.0, 80.0, 0.4), ihr(p, 40.0, 80.0, 0.4)
        assert ra["medio"] == rb["medio"] == pytest.approx(1.7, abs=1e-12)
        assert ra["serie_ihr"].equals(rb["serie_ihr"])
        assert ra["tabella_mensile"].equals(rb["tabella_mensile"])
        assert ra["verdetto"] == rb["verdetto"]


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab166_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab166" in dvars and dvars.index("tab166") == 165
        assert len(dvars) == len(set(dvars))  # nessun duplicato
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab166" in withs
        assert len(dvars) == len(withs)  # dichiarazione e blocchi allineati
        assert '"🔥 Heat rate implicito"' in src
        keys = re.findall(r'key="(ihr166_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 5
        assert re.search(r"^def calcola_heat_rate_implicito\(", src, re.M) is not None
