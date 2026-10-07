"""Test tab274 'Nucleare SMR: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab274.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("sm274_num", "sm274_int", "sm274_produzione_annua", "sm274_quota_capex",
          "sm274_costo_annuo", "sm274_lcoe", "sm274_ricavi",
          "sm274_margine", "sm274_fattore_rendita", "sm274_van",
          "sm274_payback", "sm274_confronto", "sm274_sensibilita",
          "sm274_co2_evitata")
sm274_num = _F["sm274_num"]
sm274_int = _F["sm274_int"]
sm274_produzione_annua = _F["sm274_produzione_annua"]
sm274_quota_capex = _F["sm274_quota_capex"]
sm274_costo_annuo = _F["sm274_costo_annuo"]
sm274_lcoe = _F["sm274_lcoe"]
sm274_ricavi = _F["sm274_ricavi"]
sm274_margine = _F["sm274_margine"]
sm274_fattore_rendita = _F["sm274_fattore_rendita"]
sm274_van = _F["sm274_van"]
sm274_payback = _F["sm274_payback"]
sm274_confronto = _F["sm274_confronto"]
sm274_sensibilita = _F["sm274_sensibilita"]
sm274_co2_evitata = _F["sm274_co2_evitata"]

APP = Path(__file__).parent.parent / "app.py"

TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
TITLE276 = "💧 Cash flow at risk (CFaR)"
TITLE277 = "⚡ Aste MI: scostamenti vs MGP"
TITLE278 = "🌡️ Stress climatico: domanda e prezzo"
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE284 = "🏭 Unit commitment CCGT: accendere o no?"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE272 = "🌬️ Eolico offshore: business case"

POT = 300.0
CF = 90.0
CAPEX = 1_800_000_000.0
ANNI = 60
TASSO = 5.0
OEM_PCT = 2.5
COMB = 9.0
PREZZO = 95.0
SMANT = 12_000_000.0
CO2 = 350.0

MWH = POT * 8760.0 * CF / 100.0   # 2_365_200.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab274:
    def test_tab274_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 284
        assert TITLE274 in titoli
        assert "tab274" in dvars
        assert "tab274" in withs
        assert titoli[dvars.index("tab274")] == TITLE274
        assert titoli[-1] == TITLE284
        keys = re.findall(r'key="(sm274_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_272_273_274(self):
        _, titoli, dvars, _ = _registry()
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
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284


class TestSm274Num:
    def test_ok(self):
        assert sm274_num(3, "x") == 3.0
        assert sm274_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                sm274_num(bad, "x")

    def test_int(self):
        assert sm274_int(60, "anni") == 60
        assert sm274_int(60.0, "anni") == 60
        for bad in (0, -3, 2.5, "60"):
            with pytest.raises(ValueError):
                sm274_int(bad, "anni")


class TestSm274Produzione:
    def test_base(self):
        assert sm274_produzione_annua(POT, CF) == pytest.approx(MWH)

    def test_pieno_carico(self):
        assert sm274_produzione_annua(100.0, 100.0) == pytest.approx(876000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_produzione_annua(0.0, CF)
        with pytest.raises(ValueError):
            sm274_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            sm274_produzione_annua(POT, 100.1)
        with pytest.raises(ValueError):
            sm274_produzione_annua(POT, -5.0)


class TestSm274CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        assert set(c) == {"quota_capex", "oem", "combustibile",
                          "smantellamento", "totale"}
        atteso_quota = CAPEX * (0.05 / (1.0 - 1.05 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.025)
        assert c["combustibile"] == pytest.approx(COMB * MWH)
        assert c["smantellamento"] == pytest.approx(SMANT)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"]
                                            + c["combustibile"] + c["smantellamento"])

    def test_tasso_zero(self):
        c = sm274_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, COMB, MWH, SMANT)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert sm274_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert sm274_quota_capex(CAPEX, 1, 5.0) == pytest.approx(CAPEX * 1.05)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, COMB, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, COMB, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, ANNI, TASSO, 101.0, COMB, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, -1.0, SMANT)
        with pytest.raises(ValueError):
            sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, -1.0)


class TestSm274Lcoe:
    def test_base(self):
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        assert sm274_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_ordine_grandezza(self):
        # con i default il LCOE deve stare sotto il prezzo di 95 €/MWh
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        assert sm274_lcoe(c["totale"], MWH) < PREZZO

    def test_produzione_nulla(self):
        assert sm274_lcoe(500_000_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            sm274_lcoe(500_000_000.0, -5.0)


class TestSm274RicaviMargine:
    def test_ricavi(self):
        assert sm274_ricavi(MWH, PREZZO) == pytest.approx(MWH * PREZZO)

    def test_margine(self):
        assert sm274_margine(810_000.0, 510_000.0) == pytest.approx(300_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            sm274_ricavi(-1.0, PREZZO)
        with pytest.raises(ValueError):
            sm274_margine(100.0, -1.0)


class TestSm274FattoreRendita:
    def test_tasso_zero(self):
        assert sm274_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert sm274_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert sm274_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            sm274_fattore_rendita(5.0, 0)


class TestSm274VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.05 ** t for t in range(1, 11))
        assert sm274_van(100_000.0, 10, 5.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert sm274_van(-50_000.0, 10, 5.0) < 0

    def test_payback(self):
        assert sm274_payback(CAPEX, 51_316_440.0) == pytest.approx(CAPEX / 51_316_440.0)

    def test_payback_mai(self):
        assert sm274_payback(CAPEX, 0.0) is None
        assert sm274_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            sm274_van(100.0, 0, 5.0)


class TestSm274Confronto:
    def test_non_competitivo(self):
        r = sm274_confronto(110.0, PREZZO)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_energia"] == pytest.approx(95.0)
        assert r["margine_eur_mwh"] == pytest.approx(-15.0)
        assert r["soglia_eur_mwh"] == pytest.approx(4.75)

    def test_competitivo(self):
        r = sm274_confronto(80.0, PREZZO)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(15.0)

    def test_competitivo_al_limite(self):
        # margine == soglia -> competitivo (margine >= soglia)
        r = sm274_confronto(95.0 * 0.95, 95.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(95.0 * 0.05)
        assert r["soglia_eur_mwh"] == pytest.approx(95.0 * 0.05)

    def test_indifferente(self):
        r = sm274_confronto(93.0, PREZZO)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_confronto(-1.0, PREZZO)
        with pytest.raises(ValueError):
            sm274_confronto(90.0, 0.0)


class TestSm274Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        righe = sm274_sensibilita(180.0, 90.0, MWH, c["totale"])
        assert len(righe) == 3
        assert righe[0]["prezzo_energia"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_energia"] == pytest.approx(180.0)
        assert set(righe[0]) == {"prezzo_energia", "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        righe = sm274_sensibilita(180.0, 90.0, MWH, c["totale"])
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_energia"] == pytest.approx(90.0)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * 90.0 - c["totale"])

    def test_invalidi(self):
        c = sm274_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, COMB, MWH, SMANT)
        with pytest.raises(ValueError):
            sm274_sensibilita(0.0, 90.0, MWH, c["totale"])
        with pytest.raises(ValueError):
            sm274_sensibilita(180.0, 0.0, MWH, c["totale"])
        with pytest.raises(ValueError):
            sm274_sensibilita(180.0, 90.0, -1.0, c["totale"])
        with pytest.raises(ValueError):
            sm274_sensibilita(180.0, 90.0, MWH, -1.0)


class TestSm274Co2:
    def test_base(self):
        assert sm274_co2_evitata(MWH, CO2) == pytest.approx(827820.0)

    def test_zero(self):
        assert sm274_co2_evitata(0.0, CO2) == pytest.approx(0.0)
        assert sm274_co2_evitata(MWH, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sm274_co2_evitata(-1.0, CO2)
        with pytest.raises(ValueError):
            sm274_co2_evitata(MWH, -1.0)
