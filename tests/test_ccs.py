"""Test tab193 (stile pytest): cattura e stoccaggio CO2 (CCS).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Modello: emissioni_lorde = E * (1 + penalita_energetica%); t_catturate =
lorde * tasso_cattura%; t_residue = lorde * (1 - tasso_cattura%);
costo_ccs = t_catturate * costo_eur_t; risparmio_ets = (E - t_residue) *
prezzo_co2; netto = risparmio_ets - costo_ccs;
break-even = costo_ccs / (E - t_residue) (None se la penalita' energetica
annulla il beneficio).

Numeri a mano (caso base: E = 500.000 t/anno, cattura 90%, penalita' 20%,
costo 90 EUR/t, CO2 85 EUR/t, 400 MW x 6.000 h):
  lorde = 600.000; catturate = 540.000; residue = 60.000;
  costo_ccs = 48.600.000; ets_senza = 42.500.000; ets_con = 5.100.000;
  risparmio = 37.400.000; netto = -11.200.000;
  -11,2M < -10% * 42,5M (-4,25M) -> NON CONVENIENTE;
  break-even = 48.600.000 / 440.000 = 110,4545 EUR/t;
  costo_eur_mwh = 48.600.000 / 2.400.000 = 20,25;
  sensibilita': p_max = max(2*85, 1,5*110,45) = 170; 11 punti;
  pendenza netto vs prezzo CO2 = E - residue = 440.000 EUR/(EUR/t).
  T2: prezzo_co2 = 120 -> risparmio 52.800.000, netto 4.200.000 -> CONVENIENTE.
  T3: costo 60 EUR/t, prezzo_co2 = 140 -> costo_ccs 32.400.000,
      ets_senza 70.000.000, risparmio 61.600.000, netto 29.200.000 >=
      25% * 70.000.000 -> MOLTO CONVENIENTE.
  T4: prezzo_co2 = 100 -> risparmio 44.000.000, netto -4.600.000 >=
      -10% * 50.000.000 -> MARGINALE (verdetto cita break-even 110).
  T5: cattura 0,01%, penalita' 200% -> residue 1.499.850 > E ->
      break-even None, netto -85.000.750 -> NON CONVENIENTE.
"""

import numpy as np
import pytest

from appfuncs import load

_F = load("calcola_ccs")
calcola_ccs = _F["calcola_ccs"]

KW = dict(emissioni_annue_t=500000.0, tasso_cattura_pct=90.0,
          penalita_energetica_pct=20.0, costo_ccs_eur_t=90.0,
          prezzo_co2=85.0, potenza_mw=400.0, ore_annue=6000.0)


class TestCasiBase:
    def test_caso_base_non_conveniente(self):
        r = calcola_ccs(**KW)
        assert r["valido"] and r["errore"] is None
        assert r["emissioni_lorde_t"] == pytest.approx(600000.0)
        assert r["t_catturate"] == pytest.approx(540000.0)
        assert r["t_residue"] == pytest.approx(60000.0)
        assert r["costo_ccs_annuo"] == pytest.approx(48600000.0)
        assert r["costo_ets_senza"] == pytest.approx(42500000.0)
        assert r["costo_ets_con"] == pytest.approx(5100000.0)
        assert r["risparmio_ets"] == pytest.approx(37400000.0)
        assert r["netto_annuo"] == pytest.approx(-11200000.0)
        assert r["giudizio"] == "NON CONVENIENTE"
        assert r["prezzo_co2_break_even"] == pytest.approx(110.454545, rel=1e-6)
        assert r["costo_eur_mwh"] == pytest.approx(20.25)

    def test_prezzo_alto_conveniente(self):
        r = calcola_ccs(**{**KW, "prezzo_co2": 120.0})
        assert r["valido"]
        assert r["risparmio_ets"] == pytest.approx(52800000.0)
        assert r["netto_annuo"] == pytest.approx(4200000.0)
        assert r["giudizio"] == "CONVENIENTE"

    def test_molto_conveniente(self):
        r = calcola_ccs(**{**KW, "costo_ccs_eur_t": 60.0,
                           "prezzo_co2": 140.0})
        assert r["valido"]
        assert r["costo_ccs_annuo"] == pytest.approx(32400000.0)
        assert r["costo_ets_senza"] == pytest.approx(70000000.0)
        assert r["risparmio_ets"] == pytest.approx(61600000.0)
        assert r["netto_annuo"] == pytest.approx(29200000.0)
        assert r["netto_annuo"] >= 0.25 * r["costo_ets_senza"]
        assert r["giudizio"] == "MOLTO CONVENIENTE"

    def test_marginale(self):
        r = calcola_ccs(**{**KW, "prezzo_co2": 100.0})
        assert r["valido"]
        assert r["netto_annuo"] == pytest.approx(-4600000.0)
        assert r["giudizio"] == "MARGINALE"
        assert "110" in r["verdetto"]

    def test_break_even_none_penalita_domina(self):
        r = calcola_ccs(**{**KW, "tasso_cattura_pct": 0.01,
                           "penalita_energetica_pct": 200.0})
        assert r["valido"]
        assert r["t_residue"] == pytest.approx(1499850.0)
        assert r["prezzo_co2_break_even"] is None
        assert r["netto_annuo"] == pytest.approx(-85000750.0)
        assert r["giudizio"] == "NON CONVENIENTE"
        assert "EUR/t" not in r["verdetto"]

    def test_sensibilita_e_confronto(self):
        r = calcola_ccs(**KW)
        df = r["df_sensibilita"]
        assert len(df) == 11
        assert df["Prezzo CO2 (EUR/t)"].iloc[0] == pytest.approx(0.0)
        assert df["Prezzo CO2 (EUR/t)"].iloc[-1] == pytest.approx(170.0)
        assert df["Netto annuo (EUR)"].iloc[0] == pytest.approx(-48600000.0)
        pendenza = ((df["Netto annuo (EUR)"].iloc[-1]
                     - df["Netto annuo (EUR)"].iloc[0])
                    / (df["Prezzo CO2 (EUR/t)"].iloc[-1]
                       - df["Prezzo CO2 (EUR/t)"].iloc[0]))
        assert pendenza == pytest.approx(440000.0)
        conf = r["df_confronto"]
        assert list(conf["Scenario"]) == ["Senza CCS", "Con CCS"]
        assert conf["Costo ETS (EUR/anno)"].tolist() == [42500000.0, 5100000.0]
        assert conf["Costo CCS (EUR/anno)"].tolist() == [0.0, 48600000.0]
        assert conf["Totale (EUR/anno)"].tolist() == [42500000.0, 53700000.0]
        assert conf["Emissioni nette (t/anno)"].tolist() == [500000.0, 60000.0]

    def test_determinismo(self):
        a = calcola_ccs(**KW)
        b = calcola_ccs(**KW)
        assert a["netto_annuo"] == b["netto_annuo"]
        assert a["giudizio"] == b["giudizio"]
        assert a["df_sensibilita"].equals(b["df_sensibilita"])


class TestParametriInvalidi:
    @pytest.mark.parametrize("kw", [
        {"emissioni_annue_t": 0.0},
        {"emissioni_annue_t": -5.0},
        {"emissioni_annue_t": "x"},
        {"emissioni_annue_t": True},
        {"emissioni_annue_t": None},
        {"emissioni_annue_t": float("inf")},
        {"tasso_cattura_pct": 0.0},
        {"tasso_cattura_pct": 100.01},
        {"penalita_energetica_pct": -1.0},
        {"penalita_energetica_pct": 200.01},
        {"costo_ccs_eur_t": -1.0},
        {"prezzo_co2": -1.0},
        {"potenza_mw": 0.0},
        {"ore_annue": 0.0},
        {"ore_annue": 8761.0},
        {"n_punti": 2},
        {"n_punti": 2.5},
    ])
    def test_invalidi(self, kw):
        r = calcola_ccs(**{**KW, **kw})
        assert not r["valido"] and r["errore"]

    def test_costo_zero_valido(self):
        r = calcola_ccs(**{**KW, "costo_ccs_eur_t": 0.0})
        assert r["valido"]
        assert r["costo_ccs_annuo"] == pytest.approx(0.0)
        assert r["prezzo_co2_break_even"] == pytest.approx(0.0)
        assert r["giudizio"] == "MOLTO CONVENIENTE"


class TestRegistryTab193:
    def test_tab193_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "calcola_ccs" in src
        assert '"💨 Cattura CO₂ (CCS)"' in src
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab193" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert "tab193" in withs
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(withs) == len(dvars) == 374
        keys = re.findall(r'key="(ccs193_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 8
