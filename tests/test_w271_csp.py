"""Test tab271 'Solare termodinamico (CSP): business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab271.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cs271_num", "cs271_int", "cs271_produzione_annua", "cs271_quota_capex",
          "cs271_costo_annuo", "cs271_lcoe", "cs271_ricavi",
          "cs271_margine", "cs271_fattore_rendita",
          "cs271_van", "cs271_payback", "cs271_confronto",
          "cs271_sensibilita", "cs271_co2_evitata")
cs271_num = _F["cs271_num"]
cs271_int = _F["cs271_int"]
cs271_produzione_annua = _F["cs271_produzione_annua"]
cs271_quota_capex = _F["cs271_quota_capex"]
cs271_costo_annuo = _F["cs271_costo_annuo"]
cs271_lcoe = _F["cs271_lcoe"]
cs271_ricavi = _F["cs271_ricavi"]
cs271_margine = _F["cs271_margine"]
cs271_fattore_rendita = _F["cs271_fattore_rendita"]
cs271_van = _F["cs271_van"]
cs271_payback = _F["cs271_payback"]
cs271_confronto = _F["cs271_confronto"]
cs271_sensibilita = _F["cs271_sensibilita"]
cs271_co2_evitata = _F["cs271_co2_evitata"]

APP = Path(__file__).parent.parent / "app.py"

TITLE271 = "☀️ Solare termodinamico (CSP): business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
TITLE270 = "🔥 Geotermia profonda: business case"
TITLE269 = "🌊 Idroelettrico run-of-river: business case"

POT = 50.0
CF = 45.0
CAPEX = 180_000_000.0
OEM_PCT = 2.5
ACQUA = 800_000.0
ANNI = 30
TASSO = 6.0
PREZZO = 110.0
CO2 = 350.0

MWH = POT * 8760.0 * CF / 100.0   # 197_100.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab271:
    def test_tab271_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 275
        assert TITLE271 in titoli
        assert "tab271" in dvars
        assert "tab271" in withs
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[-1] == TITLE275
        keys = re.findall(r'key="(cs271_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_269_270_271(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[dvars.index("tab274")] == TITLE274
        assert titoli[dvars.index("tab275")] == TITLE275


class TestCs271Num:
    def test_ok(self):
        assert cs271_num(3, "x") == 3.0
        assert cs271_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                cs271_num(bad, "x")

    def test_int(self):
        assert cs271_int(30, "anni") == 30
        assert cs271_int(30.0, "anni") == 30
        for bad in (0, -3, 2.5, "30"):
            with pytest.raises(ValueError):
                cs271_int(bad, "anni")


class TestCs271Produzione:
    def test_base(self):
        assert cs271_produzione_annua(POT, CF) == pytest.approx(MWH)

    def test_cf_max(self):
        assert cs271_produzione_annua(1.0, 100.0) == pytest.approx(8760.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_produzione_annua(0.0, CF)
        with pytest.raises(ValueError):
            cs271_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            cs271_produzione_annua(POT, 101.0)


class TestCs271CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, ACQUA)
        assert set(c) == {"quota_capex", "oem", "acqua", "totale"}
        atteso_quota = CAPEX * (0.06 / (1.0 - 1.06 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.025)
        assert c["acqua"] == pytest.approx(ACQUA)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["acqua"])

    def test_tasso_zero(self):
        c = cs271_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, ACQUA)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert cs271_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert cs271_quota_capex(CAPEX, 1, 6.0) == pytest.approx(CAPEX * 1.06)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, ACQUA)
        with pytest.raises(ValueError):
            cs271_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, ACQUA)
        with pytest.raises(ValueError):
            cs271_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, ACQUA)
        with pytest.raises(ValueError):
            cs271_costo_annuo(CAPEX, ANNI, TASSO, 101.0, ACQUA)
        with pytest.raises(ValueError):
            cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0)


class TestCs271Lcoe:
    def test_base(self):
        c = cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, ACQUA)
        assert cs271_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert cs271_lcoe(500_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            cs271_lcoe(500_000.0, -5.0)


class TestCs271RicaviMargine:
    def test_ricavi(self):
        assert cs271_ricavi(MWH, PREZZO) == pytest.approx(MWH * PREZZO)
        assert cs271_ricavi(MWH, 80.0) == pytest.approx(MWH * 80.0)

    def test_margine(self):
        assert cs271_margine(810_000.0, 510_000.0) == pytest.approx(300_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            cs271_ricavi(-1.0, PREZZO)
        with pytest.raises(ValueError):
            cs271_margine(100.0, -1.0)


class TestCs271FattoreRendita:
    def test_tasso_zero(self):
        assert cs271_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert cs271_fattore_rendita(6.0, 1) == pytest.approx(1 / 1.06)

    def test_formula(self):
        atteso = sum(1 / 1.06 ** t for t in range(1, 11))
        assert cs271_fattore_rendita(6.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            cs271_fattore_rendita(6.0, 0)


class TestCs271VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.06 ** t for t in range(1, 11))
        assert cs271_van(100_000.0, 10, 6.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert cs271_van(-50_000.0, 10, 6.0) < 0

    def test_payback(self):
        assert cs271_payback(CAPEX, 9_000_000.0) == pytest.approx(20.0)

    def test_payback_mai(self):
        assert cs271_payback(CAPEX, 0.0) is None
        assert cs271_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            cs271_van(100.0, 0, 6.0)


class TestCs271Confronto:
    def test_non_competitivo(self):
        r = cs271_confronto(120.0, PREZZO)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_energia"] == pytest.approx(110.0)
        assert r["margine_eur_mwh"] == pytest.approx(-10.0)
        assert r["soglia_eur_mwh"] == pytest.approx(5.5)

    def test_competitivo(self):
        r = cs271_confronto(100.0, PREZZO)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(10.0)

    def test_competitivo_al_limite(self):
        # numeri esatti in binario: margine == soglia == 5.5 -> competitivo
        r = cs271_confronto(104.5, 110.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(5.5)
        assert r["soglia_eur_mwh"] == pytest.approx(5.5)

    def test_indifferente(self):
        r = cs271_confronto(107.0, PREZZO)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_confronto(-1.0, PREZZO)
        with pytest.raises(ValueError):
            cs271_confronto(90.0, 0.0)


class TestCs271Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, ACQUA)
        righe = cs271_sensibilita(220.0, 110.0, MWH, c["totale"])
        assert len(righe) == 3
        assert righe[0]["prezzo_energia"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_energia"] == pytest.approx(220.0)
        assert set(righe[0]) == {"prezzo_energia", "ricavi_annui",
                                 "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, ACQUA)
        righe = cs271_sensibilita(220.0, 110.0, MWH, c["totale"])
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_energia"] == pytest.approx(110.0)
        assert righe[1]["ricavi_annui"] == pytest.approx(MWH * PREZZO)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * PREZZO - c["totale"])

    def test_invalidi(self):
        c = cs271_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, ACQUA)
        with pytest.raises(ValueError):
            cs271_sensibilita(0.0, 110.0, MWH, c["totale"])
        with pytest.raises(ValueError):
            cs271_sensibilita(220.0, 0.0, MWH, c["totale"])


class TestCs271Co2:
    def test_base(self):
        assert cs271_co2_evitata(MWH, CO2) == pytest.approx(68985.0)

    def test_zero(self):
        assert cs271_co2_evitata(0.0, CO2) == pytest.approx(0.0)
        assert cs271_co2_evitata(MWH, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs271_co2_evitata(-1.0, CO2)
        with pytest.raises(ValueError):
            cs271_co2_evitata(MWH, -1.0)
