"""Test tab273 'Fotovoltaico utility-scale: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab273.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("fv273_num", "fv273_int", "fv273_produzione_annua", "fv273_quota_capex",
          "fv273_costo_annuo", "fv273_lcoe", "fv273_prezzo_medio",
          "fv273_ricavi", "fv273_margine", "fv273_fattore_rendita",
          "fv273_van", "fv273_payback", "fv273_confronto",
          "fv273_sensibilita", "fv273_co2_evitata")
fv273_num = _F["fv273_num"]
fv273_int = _F["fv273_int"]
fv273_produzione_annua = _F["fv273_produzione_annua"]
fv273_quota_capex = _F["fv273_quota_capex"]
fv273_costo_annuo = _F["fv273_costo_annuo"]
fv273_lcoe = _F["fv273_lcoe"]
fv273_prezzo_medio = _F["fv273_prezzo_medio"]
fv273_ricavi = _F["fv273_ricavi"]
fv273_margine = _F["fv273_margine"]
fv273_fattore_rendita = _F["fv273_fattore_rendita"]
fv273_van = _F["fv273_van"]
fv273_payback = _F["fv273_payback"]
fv273_confronto = _F["fv273_confronto"]
fv273_sensibilita = _F["fv273_sensibilita"]
fv273_co2_evitata = _F["fv273_co2_evitata"]

APP = Path(__file__).parent.parent / "app.py"

TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE271 = "☀️ Solare termodinamico (CSP): business case"

POT = 50.0
YIELD = 1300.0
CAPEX = 40_000_000.0
OEM_PCT = 1.2
TERRENO = 200_000.0
MERCHANT = 90.0
QUOTA_PPA = 60.0
PPA = 85.0
ANNI = 25
TASSO = 5.0
CO2 = 350.0

MWH = POT * YIELD   # 65_000.0
PMED = QUOTA_PPA / 100.0 * PPA + (1.0 - QUOTA_PPA / 100.0) * MERCHANT   # 87.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab273:
    def test_tab273_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 273
        assert TITLE273 in titoli
        assert "tab273" in dvars
        assert "tab273" in withs
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[-1] == TITLE273
        keys = re.findall(r'key="(fv273_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_271_272_273(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273


class TestFv273Num:
    def test_ok(self):
        assert fv273_num(3, "x") == 3.0
        assert fv273_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                fv273_num(bad, "x")

    def test_int(self):
        assert fv273_int(25, "anni") == 25
        assert fv273_int(25.0, "anni") == 25
        for bad in (0, -3, 2.5, "25"):
            with pytest.raises(ValueError):
                fv273_int(bad, "anni")


class TestFv273Produzione:
    def test_base(self):
        assert fv273_produzione_annua(POT, YIELD) == pytest.approx(MWH)

    def test_conversioni(self):
        assert fv273_produzione_annua(1.0, 1300.0) == pytest.approx(1300.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_produzione_annua(0.0, YIELD)
        with pytest.raises(ValueError):
            fv273_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            fv273_produzione_annua(POT, -10.0)


class TestFv273CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, TERRENO)
        assert set(c) == {"quota_capex", "oem", "terreno", "totale"}
        atteso_quota = CAPEX * (0.05 / (1.0 - 1.05 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.012)
        assert c["terreno"] == pytest.approx(TERRENO)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["terreno"])

    def test_tasso_zero(self):
        c = fv273_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, TERRENO)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert fv273_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert fv273_quota_capex(CAPEX, 1, 5.0) == pytest.approx(CAPEX * 1.05)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, TERRENO)
        with pytest.raises(ValueError):
            fv273_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, TERRENO)
        with pytest.raises(ValueError):
            fv273_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, TERRENO)
        with pytest.raises(ValueError):
            fv273_costo_annuo(CAPEX, ANNI, TASSO, 101.0, TERRENO)
        with pytest.raises(ValueError):
            fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0)


class TestFv273Lcoe:
    def test_base(self):
        c = fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, TERRENO)
        assert fv273_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert fv273_lcoe(500_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            fv273_lcoe(500_000.0, -5.0)


class TestFv273PrezzoMedio:
    def test_base(self):
        assert fv273_prezzo_medio(MERCHANT, QUOTA_PPA, PPA) == pytest.approx(PMED)

    def test_quota_zero_e_cento(self):
        assert fv273_prezzo_medio(MERCHANT, 0.0, PPA) == pytest.approx(MERCHANT)
        assert fv273_prezzo_medio(MERCHANT, 100.0, PPA) == pytest.approx(PPA)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_prezzo_medio(-1.0, QUOTA_PPA, PPA)
        with pytest.raises(ValueError):
            fv273_prezzo_medio(MERCHANT, -1.0, PPA)
        with pytest.raises(ValueError):
            fv273_prezzo_medio(MERCHANT, 101.0, PPA)
        with pytest.raises(ValueError):
            fv273_prezzo_medio(MERCHANT, QUOTA_PPA, -1.0)


class TestFv273RicaviMargine:
    def test_ricavi(self):
        assert fv273_ricavi(MWH, PMED) == pytest.approx(MWH * PMED)

    def test_margine(self):
        assert fv273_margine(810_000.0, 510_000.0) == pytest.approx(300_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            fv273_ricavi(-1.0, PMED)
        with pytest.raises(ValueError):
            fv273_margine(100.0, -1.0)


class TestFv273FattoreRendita:
    def test_tasso_zero(self):
        assert fv273_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert fv273_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert fv273_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            fv273_fattore_rendita(5.0, 0)


class TestFv273VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.05 ** t for t in range(1, 11))
        assert fv273_van(100_000.0, 10, 5.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert fv273_van(-50_000.0, 10, 5.0) < 0

    def test_payback(self):
        assert fv273_payback(CAPEX, 4_000_000.0) == pytest.approx(10.0)

    def test_payback_mai(self):
        assert fv273_payback(CAPEX, 0.0) is None
        assert fv273_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            fv273_van(100.0, 0, 5.0)


class TestFv273Confronto:
    def test_non_competitivo(self):
        r = fv273_confronto(100.0, PMED)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_medio"] == pytest.approx(87.0)
        assert r["margine_eur_mwh"] == pytest.approx(-13.0)
        assert r["soglia_eur_mwh"] == pytest.approx(4.35)

    def test_competitivo(self):
        r = fv273_confronto(80.0, PMED)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(7.0)

    def test_competitivo_al_limite(self):
        # margine == soglia -> competitivo (margine >= soglia)
        r = fv273_confronto(88.0 * 0.95, 88.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(88.0 * 0.05)
        assert r["soglia_eur_mwh"] == pytest.approx(88.0 * 0.05)

    def test_indifferente(self):
        r = fv273_confronto(86.0, PMED)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_confronto(-1.0, PMED)
        with pytest.raises(ValueError):
            fv273_confronto(90.0, 0.0)


class TestFv273Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, TERRENO)
        righe = fv273_sensibilita(180.0, 90.0, MWH, c["totale"], QUOTA_PPA, PPA)
        assert len(righe) == 3
        assert righe[0]["prezzo_merchant"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_merchant"] == pytest.approx(180.0)
        assert set(righe[0]) == {"prezzo_merchant", "prezzo_medio",
                                 "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, TERRENO)
        righe = fv273_sensibilita(180.0, 90.0, MWH, c["totale"], QUOTA_PPA, PPA)
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_merchant"] == pytest.approx(90.0)
        assert righe[1]["prezzo_medio"] == pytest.approx(PMED)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * PMED - c["totale"])

    def test_invalidi(self):
        c = fv273_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, TERRENO)
        with pytest.raises(ValueError):
            fv273_sensibilita(0.0, 90.0, MWH, c["totale"], QUOTA_PPA, PPA)
        with pytest.raises(ValueError):
            fv273_sensibilita(180.0, 0.0, MWH, c["totale"], QUOTA_PPA, PPA)
        with pytest.raises(ValueError):
            fv273_sensibilita(180.0, 90.0, MWH, c["totale"], 101.0, PPA)
        with pytest.raises(ValueError):
            fv273_sensibilita(180.0, 90.0, MWH, c["totale"], QUOTA_PPA, -1.0)


class TestFv273Co2:
    def test_base(self):
        assert fv273_co2_evitata(MWH, CO2) == pytest.approx(22750.0)

    def test_zero(self):
        assert fv273_co2_evitata(0.0, CO2) == pytest.approx(0.0)
        assert fv273_co2_evitata(MWH, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv273_co2_evitata(-1.0, CO2)
        with pytest.raises(ValueError):
            fv273_co2_evitata(MWH, -1.0)
