"""Test tab269 'Idroelettrico run-of-river: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab269.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("id269_num", "id269_int", "id269_produzione_annua", "id269_quota_capex",
          "id269_costo_annuo", "id269_lcoe", "id269_ricavi",
          "id269_margine", "id269_fattore_rendita",
          "id269_van", "id269_payback", "id269_confronto",
          "id269_sensibilita", "id269_co2_evitata")
id269_num = _F["id269_num"]
id269_int = _F["id269_int"]
id269_produzione_annua = _F["id269_produzione_annua"]
id269_quota_capex = _F["id269_quota_capex"]
id269_costo_annuo = _F["id269_costo_annuo"]
id269_lcoe = _F["id269_lcoe"]
id269_ricavi = _F["id269_ricavi"]
id269_margine = _F["id269_margine"]
id269_fattore_rendita = _F["id269_fattore_rendita"]
id269_van = _F["id269_van"]
id269_payback = _F["id269_payback"]
id269_confronto = _F["id269_confronto"]
id269_sensibilita = _F["id269_sensibilita"]
id269_co2_evitata = _F["id269_co2_evitata"]

APP = Path(__file__).parent.parent / "app.py"

TITLE269 = "🌊 Idroelettrico run-of-river: business case"
TITLE270 = "🔥 Geotermia profonda: business case"
TITLE271 = "☀️ Solare termodinamico (CSP): business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
TITLE276 = "💧 Cash flow at risk (CFaR)"
TITLE277 = "⚡ Aste MI: scostamenti vs MGP"
TITLE278 = "🌡️ Stress climatico: domanda e prezzo"
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE268 = "🌬️ Eolico onshore: business case"

POT = 2.0
ORE = 4500.0
CAPEX = 6_000_000.0
OEM_PCT = 1.5
CANONE = 30_000.0
ANNI = 30
TASSO = 5.0
PREZZO = 90.0
CO2 = 350.0

MWH = POT * ORE               # 9_000


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab269:
    def test_tab269_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 281
        assert TITLE269 in titoli
        assert "tab269" in dvars
        assert "tab269" in withs
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[-1] == TITLE281
        keys = re.findall(r'key="(id269_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_268_269(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab268")] == TITLE268
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[dvars.index("tab274")] == TITLE274
        assert titoli[dvars.index("tab275")] == TITLE275
        assert titoli[dvars.index("tab276")] == TITLE276
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281


class TestId269Num:
    def test_ok(self):
        assert id269_num(3, "x") == 3.0
        assert id269_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                id269_num(bad, "x")

    def test_int(self):
        assert id269_int(30, "anni") == 30
        assert id269_int(30.0, "anni") == 30
        for bad in (0, -3, 2.5, "30"):
            with pytest.raises(ValueError):
                id269_int(bad, "anni")


class TestId269Produzione:
    def test_base(self):
        assert id269_produzione_annua(POT, ORE) == pytest.approx(MWH)

    def test_ore_max(self):
        assert id269_produzione_annua(1.0, 8760.0) == pytest.approx(8760.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_produzione_annua(0.0, ORE)
        with pytest.raises(ValueError):
            id269_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            id269_produzione_annua(POT, 8761.0)


class TestId269CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, CANONE)
        assert set(c) == {"quota_capex", "oem", "canone", "totale"}
        atteso_quota = CAPEX * (0.05 / (1.0 - 1.05 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.015)
        assert c["canone"] == pytest.approx(CANONE)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["canone"])

    def test_tasso_zero(self):
        c = id269_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, CANONE)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert id269_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert id269_quota_capex(CAPEX, 1, 5.0) == pytest.approx(CAPEX * 1.05)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, CANONE)
        with pytest.raises(ValueError):
            id269_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, CANONE)
        with pytest.raises(ValueError):
            id269_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, CANONE)
        with pytest.raises(ValueError):
            id269_costo_annuo(CAPEX, ANNI, TASSO, 101.0, CANONE)
        with pytest.raises(ValueError):
            id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0)


class TestId269Lcoe:
    def test_base(self):
        c = id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, CANONE)
        assert id269_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert id269_lcoe(500_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            id269_lcoe(500_000.0, -5.0)


class TestId269RicaviMargine:
    def test_ricavi(self):
        assert id269_ricavi(MWH, PREZZO) == pytest.approx(MWH * PREZZO)
        assert id269_ricavi(MWH, 100.0) == pytest.approx(MWH * 100.0)

    def test_margine(self):
        assert id269_margine(810_000.0, 510_000.0) == pytest.approx(300_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            id269_ricavi(-1.0, PREZZO)
        with pytest.raises(ValueError):
            id269_margine(100.0, -1.0)


class TestId269FattoreRendita:
    def test_tasso_zero(self):
        assert id269_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert id269_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert id269_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            id269_fattore_rendita(5.0, 0)


class TestId269VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.05 ** t for t in range(1, 11))
        assert id269_van(100_000.0, 10, 5.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert id269_van(-50_000.0, 10, 5.0) < 0

    def test_payback(self):
        assert id269_payback(CAPEX, 300_000.0) == pytest.approx(20.0)

    def test_payback_mai(self):
        assert id269_payback(CAPEX, 0.0) is None
        assert id269_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            id269_van(100.0, 0, 5.0)


class TestId269Confronto:
    def test_non_competitivo(self):
        r = id269_confronto(100.0, PREZZO)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_energia"] == pytest.approx(90.0)
        assert r["margine_eur_mwh"] == pytest.approx(-10.0)
        assert r["soglia_eur_mwh"] == pytest.approx(4.5)

    def test_competitivo(self):
        r = id269_confronto(80.0, PREZZO)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(10.0)

    def test_competitivo_al_limite(self):
        # numeri esatti in binario: margine == soglia == 4.5 -> competitivo
        r = id269_confronto(85.5, 90.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(4.5)
        assert r["soglia_eur_mwh"] == pytest.approx(4.5)

    def test_indifferente(self):
        r = id269_confronto(88.0, PREZZO)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_confronto(-1.0, PREZZO)
        with pytest.raises(ValueError):
            id269_confronto(80.0, 0.0)


class TestId269Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, CANONE)
        righe = id269_sensibilita(180.0, 90.0, MWH, c["totale"])
        assert len(righe) == 3
        assert righe[0]["prezzo_energia"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_energia"] == pytest.approx(180.0)
        assert set(righe[0]) == {"prezzo_energia", "ricavi_annui",
                                 "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, CANONE)
        righe = id269_sensibilita(180.0, 90.0, MWH, c["totale"])
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_energia"] == pytest.approx(90.0)
        assert righe[1]["ricavi_annui"] == pytest.approx(MWH * PREZZO)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * PREZZO - c["totale"])

    def test_invalidi(self):
        c = id269_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, CANONE)
        with pytest.raises(ValueError):
            id269_sensibilita(0.0, 90.0, MWH, c["totale"])
        with pytest.raises(ValueError):
            id269_sensibilita(180.0, 0.0, MWH, c["totale"])


class TestId269Co2:
    def test_base(self):
        assert id269_co2_evitata(MWH, CO2) == pytest.approx(3150.0)

    def test_zero(self):
        assert id269_co2_evitata(0.0, CO2) == pytest.approx(0.0)
        assert id269_co2_evitata(MWH, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            id269_co2_evitata(-1.0, CO2)
        with pytest.raises(ValueError):
            id269_co2_evitata(MWH, -1.0)
