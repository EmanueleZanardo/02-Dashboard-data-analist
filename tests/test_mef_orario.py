"""Test tab228 (stile pytest): MEF orario / emissioni marginali da merit order.

Funzione pura calcola_mef_orario estratta da app.py via AST (tests/appfuncs).
Stile QA: numeri calcolati a mano + validazione input + determinismo +
registry tab228.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("calcola_mef_orario")
calcola_mef_orario = _F["calcola_mef_orario"]


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_carbone_vs_ccgt(self):
        # picco 100, carbone 70 (45 eur, 0.95 t/MWh), CCGT 100 (75, 0.40).
        # carico<=70 -> ore 0..6 e 23 (8 ore): carbone copre tutto -> MEF 0.95.
        # carico>70 -> 16 ore: carbone 70 + CCGT -> MEF 0.40.
        # carico tot = 100*18.35 = 1835; ore carbone = 100*(4.30+0.64) = 494.
        # medio = (0.95*494 + 0.40*1341)/1835
        r = calcola_mef_orario(100.0, cap_carbone_mw=70.0, cap_ccgt_mw=100.0)
        assert r["valido"] and r["errore"] is None
        assert r["mef_max_tco2_mwh"] == pytest.approx(0.95)
        assert r["ora_mef_max"] == 0
        assert r["mef_min_tco2_mwh"] == pytest.approx(0.40)
        assert r["ora_mef_min"] == 7
        assert r["delta_mef_spostabile_tco2_mwh"] == pytest.approx(0.55)
        assert r["ore_mef_zero"] == 0
        assert r["mix_marginale_ore"] == {"Carbone": 8, "Gas CCGT": 16}
        assert r["deficit"] is False
        atteso = round((0.95 * 494.0 + 0.40 * 1341.0) / 1835.0, 4)
        assert r["mef_medio_ponderato_tco2_mwh"] == pytest.approx(atteso, abs=1e-9)

    def test_rinnovabili_azzerano_mef(self):
        # picco 100, FV 300 estate: h13 -> 300*0.9*sin(pi/2)=270 MW >= 80
        # -> FV marginale, MEF 0.
        r = calcola_mef_orario(100.0, cap_fv_mw=300.0,
                               cap_carbone_mw=200.0, stagione="estate")
        assert r["valido"]
        df = r["df_orario"]
        assert df.loc[df["ora"] == 13, "mef_tco2_mwh"].iloc[0] == 0.0
        assert df.loc[df["ora"] == 13,
                      "tecnologia_marginale"].iloc[0] == "Fotovoltaico"
        assert r["mef_min_tco2_mwh"] == 0.0
        assert r["ore_mef_zero"] >= 1
        assert r["stagione_usata"] == "estate"
        assert list(df.columns) == ["ora", "carico_MW", "mef_tco2_mwh",
                                    "tecnologia_marginale"]
        assert len(df) == 24

    def test_inverno_fv_ridotto(self):
        # inverno: sole 8-16, cf picco 0.60; h12 -> 300*0.6=180 >= 80 -> MEF 0
        # h13 -> 300*0.6*sin(pi*5/8) = 180*0.924 = 166.3 >= 80 -> MEF 0
        # h18 -> notte -> carbone marginale
        r = calcola_mef_orario(100.0, cap_fv_mw=300.0,
                               cap_carbone_mw=200.0, stagione="inverno")
        assert r["valido"]
        df = r["df_orario"]
        assert df.loc[df["ora"] == 18, "mef_tco2_mwh"].iloc[0] == pytest.approx(0.95)
        assert df.loc[df["ora"] == 18,
                      "tecnologia_marginale"].iloc[0] == "Carbone"
        assert r["stagione_usata"] == "inverno"

    def test_nucleare_baseload(self):
        # picco 100, nucleare 200 -> 170 MW sempre disponibili > carico max 100
        # -> nucleare sempre marginale, MEF 0 ovunque, 24 ore a zero.
        r = calcola_mef_orario(100.0, cap_nucleare_mw=200.0)
        assert r["valido"]
        assert r["ore_mef_zero"] == 24
        assert r["mef_medio_ponderato_tco2_mwh"] == 0.0
        assert r["mix_marginale_ore"] == {"Nucleare": 24}

    def test_deficit(self):
        # picco 1000 con solo 10 MW di carbone -> mai coperto
        r = calcola_mef_orario(1000.0, cap_carbone_mw=10.0)
        assert r["valido"]  # calcolo valido, ma con deficit segnalato
        assert r["deficit"] is True
        assert r["mix_marginale_ore"] == {"Carbone": 24}


# ------------------------------------------------------- validazione
class TestValidazione:
    def test_picco_non_positivo(self):
        for bad in (0.0, -5.0):
            r = calcola_mef_orario(bad, cap_carbone_mw=100.0)
            assert not r["valido"] and r["errore"] is not None

    def test_capacita_negativa(self):
        assert not calcola_mef_orario(100.0, cap_ccgt_mw=-1.0)["valido"]

    def test_capacita_totale_nulla(self):
        r = calcola_mef_orario(100.0)
        assert not r["valido"] and "nulla" in r["errore"]

    def test_fattore_eolico_fuori_range(self):
        r = calcola_mef_orario(100.0, cap_eolico_mw=50.0, fattore_eolico=1.5)
        assert not r["valido"]

    def test_stagione_sconosciuta(self):
        r = calcola_mef_orario(100.0, cap_fv_mw=50.0, stagione="primavera")
        assert not r["valido"]

    def test_input_non_numerici(self):
        r = calcola_mef_orario("tanto", cap_carbone_mw=100.0)
        assert not r["valido"]


# ------------------------------------------------------- determinismo
class TestDeterminismo:
    def test_stesso_input_stesso_output(self):
        kw = dict(cap_nucleare_mw=1500.0, cap_idro_mw=800.0,
                  cap_eolico_mw=1200.0, cap_fv_mw=2500.0,
                  cap_carbone_mw=800.0, cap_ccgt_mw=2000.0,
                  cap_ocgt_mw=600.0, cap_import_mw=500.0,
                  stagione="estate", fattore_eolico=0.35)
        r1 = calcola_mef_orario(5000.0, **kw)
        r2 = calcola_mef_orario(5000.0, **kw)
        assert r1["mef_medio_ponderato_tco2_mwh"] == r2["mef_medio_ponderato_tco2_mwh"]
        assert r1["delta_mef_spostabile_tco2_mwh"] == r2["delta_mef_spostabile_tco2_mwh"]
        assert (r1["df_orario"]["mef_tco2_mwh"]
                == r2["df_orario"]["mef_tco2_mwh"]).all()


# ------------------------------------------------------- registry
class TestRegistryTab228:
    def test_tab228_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 325
        assert titoli[-1] == "📈📉 Calmar ratio: il rendimento che paga il drawdown"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab228" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab228" in withs
        assert len(withs) == len(dvars) == 325
        keys = re.findall(r'key="(ai228_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8
