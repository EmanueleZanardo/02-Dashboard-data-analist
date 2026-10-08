"""Test tab267 'Biometano: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab267.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("bm267_num", "bm267_int", "bm267_resa_biometano", "bm267_mwh_annui",
          "bm267_costo_annuo", "bm267_lcog", "bm267_ricavi", "bm267_margine",
          "bm267_fattore_rendita", "bm267_van", "bm267_payback",
          "bm267_confronto", "bm267_sensibilita")
bm267_num = _F["bm267_num"]
bm267_int = _F["bm267_int"]
bm267_resa_biometano = _F["bm267_resa_biometano"]
bm267_mwh_annui = _F["bm267_mwh_annui"]
bm267_costo_annuo = _F["bm267_costo_annuo"]
bm267_lcog = _F["bm267_lcog"]
bm267_ricavi = _F["bm267_ricavi"]
bm267_margine = _F["bm267_margine"]
bm267_fattore_rendita = _F["bm267_fattore_rendita"]
bm267_van = _F["bm267_van"]
bm267_payback = _F["bm267_payback"]
bm267_confronto = _F["bm267_confronto"]
bm267_sensibilita = _F["bm267_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"

TITLE267 = "🟢 Biometano: business case"
TITLE268 = "🌬️ Eolico onshore: business case"
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
TITLE266 = "🌾️ Agrivoltaico: doppio reddito"

T_ANNO = 30000.0
RESA = 100.0
C_SUB = 25.0
CAPEX = 4500000.0
OEM_PCT = 4.0
ANNI = 25
TASSO = 5.0
P_GAS = 35.0

NM3 = T_ANNO * RESA            # 3_000_000
MWH = NM3 * 10.5 / 1000.0     # 31_500


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab267:
    def test_tab267_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 307
        assert TITLE267 in titoli
        assert "tab267" in dvars
        assert "tab267" in withs
        assert titoli[dvars.index("tab267")] == TITLE267
        assert titoli[-1] == TITLE307
        keys = re.findall(r'key="(bm267_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_266_267(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab266")] == TITLE266
        assert titoli[dvars.index("tab267")] == TITLE267
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
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestBm267Num:
    def test_ok(self):
        assert bm267_num(3, "x") == 3.0
        assert bm267_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                bm267_num(bad, "x")

    def test_int(self):
        assert bm267_int(25, "anni") == 25
        assert bm267_int(25.0, "anni") == 25
        for bad in (0, -3, 2.5, "25"):
            with pytest.raises(ValueError):
                bm267_int(bad, "anni")


class TestBm267Resa:
    def test_base(self):
        assert bm267_resa_biometano(T_ANNO, RESA) == pytest.approx(NM3)
        assert bm267_mwh_annui(NM3) == pytest.approx(MWH)

    def test_pcs(self):
        assert bm267_mwh_annui(1_000_000.0) == pytest.approx(10_500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_resa_biometano(0.0, RESA)
        with pytest.raises(ValueError):
            bm267_resa_biometano(T_ANNO, -1.0)
        with pytest.raises(ValueError):
            bm267_mwh_annui(0.0)


class TestBm267CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        assert set(c) == {"quota_capex", "oem", "substrato", "totale"}
        atteso_quota = CAPEX * (0.05 / (1.0 - 1.05 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.04)
        assert c["substrato"] == pytest.approx(T_ANNO * C_SUB)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["substrato"])

    def test_tasso_zero(self):
        c = bm267_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, T_ANNO, C_SUB)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        with pytest.raises(ValueError):
            bm267_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, T_ANNO, C_SUB)
        with pytest.raises(ValueError):
            bm267_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, T_ANNO, C_SUB)
        with pytest.raises(ValueError):
            bm267_costo_annuo(CAPEX, ANNI, TASSO, 101.0, T_ANNO, C_SUB)
        with pytest.raises(ValueError):
            bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, -5.0)


class TestBm267Lcog:
    def test_base(self):
        c = bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        assert bm267_lcog(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert bm267_lcog(1_000_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_lcog(-1.0, MWH)
        with pytest.raises(ValueError):
            bm267_lcog(1_000_000.0, -5.0)


class TestBm267RicaviMargine:
    def test_ricavi(self):
        assert bm267_ricavi(MWH, P_GAS, 0.0) == pytest.approx(MWH * P_GAS)
        assert bm267_ricavi(MWH, P_GAS, 15.0) == pytest.approx(MWH * (P_GAS + 15.0))

    def test_margine(self):
        assert bm267_margine(1_102_500.0, 1_249_283.0) == pytest.approx(-146_783.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_ricavi(MWH, -1.0, 0.0)
        with pytest.raises(ValueError):
            bm267_ricavi(MWH, P_GAS, -1.0)
        with pytest.raises(ValueError):
            bm267_margine(100.0, -1.0)


class TestBm267FattoreRendita:
    def test_tasso_zero(self):
        assert bm267_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert bm267_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert bm267_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            bm267_fattore_rendita(5.0, 0)


class TestBm267VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.05 ** t for t in range(1, 11))
        assert bm267_van(100_000.0, 10, 5.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert bm267_van(-50_000.0, 10, 5.0) < 0

    def test_payback(self):
        assert bm267_payback(CAPEX, 300_000.0) == pytest.approx(15.0)

    def test_payback_mai(self):
        assert bm267_payback(CAPEX, 0.0) is None
        assert bm267_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_payback(-1.0, 300_000.0)
        with pytest.raises(ValueError):
            bm267_van(100.0, 0, 5.0)


class TestBm267Confronto:
    def test_non_competitivo(self):
        r = bm267_confronto(39.0, P_GAS, 0.0)
        assert r["verdetto"] == "non_competitivo"
        assert r["ricavo_unitario"] == pytest.approx(35.0)
        assert r["margine_eur_mwh"] == pytest.approx(-4.0)
        assert r["soglia_eur_mwh"] == pytest.approx(1.75)

    def test_competitivo(self):
        r = bm267_confronto(30.0, P_GAS, 0.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(5.0)

    def test_competitivo_al_limite(self):
        r = bm267_confronto(33.25, P_GAS, 0.0)
        assert r["verdetto"] == "competitivo"

    def test_indifferente(self):
        r = bm267_confronto(34.0, P_GAS, 0.0)
        assert r["verdetto"] == "indifferente"

    def test_incentivo_ribalta(self):
        r = bm267_confronto(39.0, P_GAS, 10.0)
        assert r["ricavo_unitario"] == pytest.approx(45.0)
        assert r["verdetto"] == "competitivo"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bm267_confronto(-1.0, P_GAS, 0.0)
        with pytest.raises(ValueError):
            bm267_confronto(30.0, -1.0, 0.0)
        with pytest.raises(ValueError):
            bm267_confronto(30.0, 0.0, 0.0)


class TestBm267Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        righe = bm267_sensibilita(70.0, 35.0, MWH, c["totale"], 0.0)
        assert len(righe) == 3
        assert righe[0]["prezzo_gas"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_gas"] == pytest.approx(70.0)
        assert set(righe[0]) == {"prezzo_gas", "ricavi_annui", "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        righe = bm267_sensibilita(70.0, 35.0, MWH, c["totale"], 0.0)
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["ricavi_annui"] == pytest.approx(MWH * 35.0)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * 35.0 - c["totale"])

    def test_invalidi(self):
        c = bm267_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, T_ANNO, C_SUB)
        with pytest.raises(ValueError):
            bm267_sensibilita(0.0, 35.0, MWH, c["totale"], 0.0)
        with pytest.raises(ValueError):
            bm267_sensibilita(70.0, 0.0, MWH, c["totale"], 0.0)
