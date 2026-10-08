"""Test tab270 'Geotermia profonda: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab270.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("gt270_num", "gt270_int", "gt270_produzione_annua", "gt270_quota_capex",
          "gt270_costo_annuo", "gt270_lcoe", "gt270_ricavi",
          "gt270_margine", "gt270_fattore_rendita",
          "gt270_van", "gt270_payback", "gt270_confronto",
          "gt270_sensibilita", "gt270_co2_evitata")
gt270_num = _F["gt270_num"]
gt270_int = _F["gt270_int"]
gt270_produzione_annua = _F["gt270_produzione_annua"]
gt270_quota_capex = _F["gt270_quota_capex"]
gt270_costo_annuo = _F["gt270_costo_annuo"]
gt270_lcoe = _F["gt270_lcoe"]
gt270_ricavi = _F["gt270_ricavi"]
gt270_margine = _F["gt270_margine"]
gt270_fattore_rendita = _F["gt270_fattore_rendita"]
gt270_van = _F["gt270_van"]
gt270_payback = _F["gt270_payback"]
gt270_confronto = _F["gt270_confronto"]
gt270_sensibilita = _F["gt270_sensibilita"]
gt270_co2_evitata = _F["gt270_co2_evitata"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE284 = "🏭 Unit commitment CCGT: accendere o no?"
TITLE285 = "🛛️ Differenziali greggio: sweet vs sour"
TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE269 = "🌊 Idroelettrico run-of-river: business case"

POT = 5.0
CF = 90.0
CAPEX = 25_000_000.0
OEM_PCT = 3.0
POZZI = 200_000.0
ANNI = 30
TASSO = 6.0
PREZZO = 100.0
CO2 = 350.0

MWH = POT * 8760.0 * CF / 100.0   # 39_420.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab270:
    def test_tab270_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 317
        assert TITLE270 in titoli
        assert "tab270" in dvars
        assert "tab270" in withs
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[-1] == TITLE317
        keys = re.findall(r'key="(gt270_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_269_270(self):
        _, titoli, dvars, _ = _registry()
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
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestGt270Num:
    def test_ok(self):
        assert gt270_num(3, "x") == 3.0
        assert gt270_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                gt270_num(bad, "x")

    def test_int(self):
        assert gt270_int(30, "anni") == 30
        assert gt270_int(30.0, "anni") == 30
        for bad in (0, -3, 2.5, "30"):
            with pytest.raises(ValueError):
                gt270_int(bad, "anni")


class TestGt270Produzione:
    def test_base(self):
        assert gt270_produzione_annua(POT, CF) == pytest.approx(MWH)

    def test_cf_max(self):
        assert gt270_produzione_annua(1.0, 100.0) == pytest.approx(8760.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_produzione_annua(0.0, CF)
        with pytest.raises(ValueError):
            gt270_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            gt270_produzione_annua(POT, 101.0)


class TestGt270CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, POZZI)
        assert set(c) == {"quota_capex", "oem", "fondo_pozzi", "totale"}
        atteso_quota = CAPEX * (0.06 / (1.0 - 1.06 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.03)
        assert c["fondo_pozzi"] == pytest.approx(POZZI)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["fondo_pozzi"])

    def test_tasso_zero(self):
        c = gt270_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, POZZI)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert gt270_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert gt270_quota_capex(CAPEX, 1, 6.0) == pytest.approx(CAPEX * 1.06)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, POZZI)
        with pytest.raises(ValueError):
            gt270_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, POZZI)
        with pytest.raises(ValueError):
            gt270_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, POZZI)
        with pytest.raises(ValueError):
            gt270_costo_annuo(CAPEX, ANNI, TASSO, 101.0, POZZI)
        with pytest.raises(ValueError):
            gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0)


class TestGt270Lcoe:
    def test_base(self):
        c = gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, POZZI)
        assert gt270_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert gt270_lcoe(500_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            gt270_lcoe(500_000.0, -5.0)


class TestGt270RicaviMargine:
    def test_ricavi(self):
        assert gt270_ricavi(MWH, PREZZO) == pytest.approx(MWH * PREZZO)
        assert gt270_ricavi(MWH, 80.0) == pytest.approx(MWH * 80.0)

    def test_margine(self):
        assert gt270_margine(810_000.0, 510_000.0) == pytest.approx(300_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            gt270_ricavi(-1.0, PREZZO)
        with pytest.raises(ValueError):
            gt270_margine(100.0, -1.0)


class TestGt270FattoreRendita:
    def test_tasso_zero(self):
        assert gt270_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert gt270_fattore_rendita(6.0, 1) == pytest.approx(1 / 1.06)

    def test_formula(self):
        atteso = sum(1 / 1.06 ** t for t in range(1, 11))
        assert gt270_fattore_rendita(6.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            gt270_fattore_rendita(6.0, 0)


class TestGt270VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.06 ** t for t in range(1, 11))
        assert gt270_van(100_000.0, 10, 6.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert gt270_van(-50_000.0, 10, 6.0) < 0

    def test_payback(self):
        assert gt270_payback(CAPEX, 1_250_000.0) == pytest.approx(20.0)

    def test_payback_mai(self):
        assert gt270_payback(CAPEX, 0.0) is None
        assert gt270_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            gt270_van(100.0, 0, 6.0)


class TestGt270Confronto:
    def test_non_competitivo(self):
        r = gt270_confronto(110.0, PREZZO)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_energia"] == pytest.approx(100.0)
        assert r["margine_eur_mwh"] == pytest.approx(-10.0)
        assert r["soglia_eur_mwh"] == pytest.approx(5.0)

    def test_competitivo(self):
        r = gt270_confronto(90.0, PREZZO)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(10.0)

    def test_competitivo_al_limite(self):
        # numeri esatti in binario: margine == soglia == 5.0 -> competitivo
        r = gt270_confronto(95.0, 100.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(5.0)
        assert r["soglia_eur_mwh"] == pytest.approx(5.0)

    def test_indifferente(self):
        r = gt270_confronto(97.0, PREZZO)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_confronto(-1.0, PREZZO)
        with pytest.raises(ValueError):
            gt270_confronto(90.0, 0.0)


class TestGt270Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, POZZI)
        righe = gt270_sensibilita(200.0, 100.0, MWH, c["totale"])
        assert len(righe) == 3
        assert righe[0]["prezzo_energia"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_energia"] == pytest.approx(200.0)
        assert set(righe[0]) == {"prezzo_energia", "ricavi_annui",
                                 "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, POZZI)
        righe = gt270_sensibilita(200.0, 100.0, MWH, c["totale"])
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_energia"] == pytest.approx(100.0)
        assert righe[1]["ricavi_annui"] == pytest.approx(MWH * PREZZO)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * PREZZO - c["totale"])

    def test_invalidi(self):
        c = gt270_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, POZZI)
        with pytest.raises(ValueError):
            gt270_sensibilita(0.0, 100.0, MWH, c["totale"])
        with pytest.raises(ValueError):
            gt270_sensibilita(200.0, 0.0, MWH, c["totale"])


class TestGt270Co2:
    def test_base(self):
        assert gt270_co2_evitata(MWH, CO2) == pytest.approx(13797.0)

    def test_zero(self):
        assert gt270_co2_evitata(0.0, CO2) == pytest.approx(0.0)
        assert gt270_co2_evitata(MWH, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gt270_co2_evitata(-1.0, CO2)
        with pytest.raises(ValueError):
            gt270_co2_evitata(MWH, -1.0)
