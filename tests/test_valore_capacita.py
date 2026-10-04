"""Test tab192 (stile pytest): remunerazione della capacita' (capacity market).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Modello: margine energia = somma oraria max(spot - cm, 0) * P annualizzato
(fattore 8760 / n_ore); ricavo capacita' = P * derating% * prezzo_asta
(EUR/kW/anno); penalita' = P * derating% * penalita' * ore_indisp *
quota_critiche%; netto = ricavo + margine - penalita' - opex.

Numeri a mano (P = 100 MW):
  T1: 24h piatte a 100, cm=60, dr=85%, asta=30, opex=25, indisp=0:
      marg_ore = (100-60)*100*24 = 96.000; fattore 365 ->
      marg_energia_annuo = 35.040.000; ore_run = 8.760; p_medio_run = 100;
      derated = 85 MW; ricavo = 85.000 * 30 = 2.550.000;
      opex = 100.000 * 25 = 2.500.000; penalita' = 0;
      netto = 2.550.000 + 35.040.000 - 2.500.000 = 35.090.000 ->
      CONVENIENTE; break-even = 0 (l'energia copre tutto).
      Sensibilita': pendenza netto vs prezzo asta = 85.000 EUR/(EUR/kW).
  T2: 24h a 100, cm=200 (mai in-the-money), stessi parametri:
      margine = 0; netto = 2.550.000 - 2.500.000 = 50.000 >= 0 ->
      CONVENIENTE; BE = 2.500.000 / 85.000 = 29,4118 EUR/kW.
  T3: come T2 ma asta=20: ricavo = 1.700.000; netto = -800.000;
      -800.000 >= -0,5 * 2.500.000 -> MARGINALE.
  T4: come T2 ma indisp=876, quota critiche=2%, penalita'=5000:
      ore critiche in fermo = 876 * 0,02 = 17,52;
      penalita' = 85 * 5000 * 17,52 = 7.446.000;
      netto = 2.550.000 - 7.446.000 - 2.500.000 = -7.396.000 ->
      NON CONVENIENTE;
      BE = (2.500.000 + 7.446.000) / 85.000 = 117,0118 EUR/kW.
  T5: 12h a 50 + 12h a 100, cm=80: dispaccia solo le 12h a 100:
      marg_ore = 20 * 100 * 12 = 24.000 -> annuo 8.760.000;
      ore_run_annue = 4.380; p_medio_run = 100.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_valore_capacita")
calcola_valore_capacita = _F["calcola_valore_capacita"]

TZ = "Europe/Zurich"

KW = dict(potenza_mw=100.0, costo_marginale=60.0, derating_pct=85.0,
          prezzo_asta_eur_kw=30.0, opex_fisso_eur_kw=25.0,
          ore_indisponibili=0.0, quota_ore_critiche_pct=2.0,
          penalita_eur_mw_h=5000.0, min_ore=24)


def serie(prezzi, start="2026-09-28", tz=TZ):
    idx = pd.date_range(start, periods=len(prezzi), freq="h", tz=tz)
    return pd.Series(np.asarray(prezzi, dtype=float), index=idx, name="p")


class TestCasiBase:
    def test_piatta_conveniente(self):
        r = calcola_valore_capacita(serie([100.0] * 24), **KW)
        assert r["valido"] and r["errore"] is None
        assert r["margine_energia_annuo"] == pytest.approx(35_040_000.0, rel=1e-9)
        assert r["ore_run_annue"] == pytest.approx(8760.0)
        assert r["prezzo_medio_run"] == pytest.approx(100.0)
        assert r["potenza_derated_mw"] == pytest.approx(85.0)
        assert r["ricavo_capacita_annuo"] == pytest.approx(2_550_000.0, rel=1e-9)
        assert r["penalita_annua"] == pytest.approx(0.0)
        assert r["opex_fisso_annuo"] == pytest.approx(2_500_000.0, rel=1e-9)
        assert r["netto_annuo"] == pytest.approx(35_090_000.0, rel=1e-9)
        assert r["prezzo_asta_break_even"] == pytest.approx(0.0)
        assert r["giudizio"] == "CONVENIENTE"

    def test_mai_in_the_money(self):
        kw = dict(KW, costo_marginale=200.0)
        r = calcola_valore_capacita(serie([100.0] * 24), **kw)
        assert r["valido"]
        assert r["margine_energia_annuo"] == pytest.approx(0.0)
        assert r["ore_run_annue"] == pytest.approx(0.0)
        assert r["prezzo_medio_run"] == pytest.approx(0.0)
        assert r["netto_annuo"] == pytest.approx(50_000.0, rel=1e-9)
        assert r["prezzo_asta_break_even"] == pytest.approx(29.4117647, rel=1e-6)
        assert r["giudizio"] == "CONVENIENTE"

    def test_marginale(self):
        kw = dict(KW, costo_marginale=200.0, prezzo_asta_eur_kw=20.0)
        r = calcola_valore_capacita(serie([100.0] * 24), **kw)
        assert r["valido"]
        assert r["netto_annuo"] == pytest.approx(-800_000.0, rel=1e-9)
        assert r["giudizio"] == "MARGINALE"

    def test_penalita_non_conveniente(self):
        kw = dict(KW, costo_marginale=200.0, ore_indisponibili=876.0)
        r = calcola_valore_capacita(serie([100.0] * 24), **kw)
        assert r["valido"]
        assert r["penalita_annua"] == pytest.approx(7_446_000.0, rel=1e-9)
        assert r["netto_annuo"] == pytest.approx(-7_396_000.0, rel=1e-9)
        assert r["prezzo_asta_break_even"] == pytest.approx(117.0117647, rel=1e-6)
        assert r["giudizio"] == "NON CONVENIENTE"

    def test_dispatch_parziale(self):
        r = calcola_valore_capacita(serie([50.0] * 12 + [100.0] * 12),
                                   **dict(KW, costo_marginale=80.0))
        assert r["valido"]
        assert r["margine_energia_annuo"] == pytest.approx(8_760_000.0, rel=1e-9)
        assert r["ore_run_annue"] == pytest.approx(4380.0)
        assert r["prezzo_medio_run"] == pytest.approx(100.0)


class TestTabelle:
    def test_sensibilita_lineare(self):
        r = calcola_valore_capacita(serie([100.0] * 24), **KW)
        df = r["df_sensibilita"]
        assert len(df) == 11
        dp = (df["Prezzo asta (EUR/kW/anno)"].iloc[1]
              - df["Prezzo asta (EUR/kW/anno)"].iloc[0])
        dn = df["Netto annuo (EUR)"].iloc[1] - df["Netto annuo (EUR)"].iloc[0]
        assert dn == pytest.approx(85_000.0 * dp, rel=1e-9)
        assert df["Prezzo asta (EUR/kW/anno)"].iloc[0] == pytest.approx(0.0)

    def test_mensile_un_mese(self):
        r = calcola_valore_capacita(serie([100.0] * 24), **KW)
        df = r["df_mensile"]
        assert len(df) == 1 and df["Mese"].iloc[0] == "2026-09"
        assert df["Margine energia (EUR)"].iloc[0] == pytest.approx(96_000.0)
        assert df["Ore di funzionamento"].iloc[0] == 24

    def test_sensibilita_copre_be(self):
        kw = dict(KW, costo_marginale=200.0, ore_indisponibili=876.0)
        r = calcola_valore_capacita(serie([100.0] * 24), **kw)
        df = r["df_sensibilita"]
        assert df["Prezzo asta (EUR/kW/anno)"].max() >= r["prezzo_asta_break_even"]


class TestRobustezza:
    def test_tz_naive_ok(self):
        s = serie([100.0] * 24, tz=None)
        r = calcola_valore_capacita(s, **KW)
        assert r["valido"] and r["netto_annuo"] == pytest.approx(35_090_000.0, rel=1e-9)

    def test_duplicati_keep_first(self):
        s = serie([100.0] * 24)
        dup = pd.concat([s, s.iloc[[0]]])
        r = calcola_valore_capacita(dup, **KW)
        assert r["valido"] and r["n_ore"] == 24

    def test_nan_scartati(self):
        s = serie([100.0] * 24)
        s.iloc[3] = np.nan
        r = calcola_valore_capacita(s, **KW)
        assert not r["valido"]  # 23 ore < min_ore=168

    def test_non_serie(self):
        r = calcola_valore_capacita([100.0] * 200, **KW)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        s = pd.Series(np.full(200, 100.0))
        r = calcola_valore_capacita(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_serie_troppo_corta(self):
        r = calcola_valore_capacita(serie([100.0] * 100),
                                       **dict(KW, min_ore=168))
        assert not r["valido"] and "168" in r["errore"]

    @pytest.mark.parametrize("kw", [
        dict(potenza_mw=0.0), dict(potenza_mw=-5.0),
        dict(derating_pct=0.0), dict(derating_pct=101.0),
        dict(prezzo_asta_eur_kw=-1.0), dict(opex_fisso_eur_kw=-1.0),
        dict(ore_indisponibili=-1.0),
        dict(quota_ore_critiche_pct=-1.0), dict(quota_ore_critiche_pct=101.0),
        dict(penalita_eur_mw_h=-1.0), dict(n_punti=2), dict(min_ore=10),
    ])
    def test_parametri_invalidi(self, kw):
        base = dict(KW)
        base.update(kw)
        r = calcola_valore_capacita(serie([100.0] * 200), **base)
        assert not r["valido"] and r["errore"]

    def test_determinismo(self):
        a = calcola_valore_capacita(serie([100.0] * 24), **KW)
        b = calcola_valore_capacita(serie([100.0] * 24), **KW)
        assert a["netto_annuo"] == b["netto_annuo"]
        assert a["df_sensibilita"].equals(b["df_sensibilita"])


class TestRegistryTab192:
    def test_tab192_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "calcola_valore_capacita" in src
        assert '"⚡ Remunerazione capacità"' in src
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab192" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert "tab192" in withs
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(withs) == len(dvars) == 211
        keys = re.findall(r'key="(mi192_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 8
