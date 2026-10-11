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
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
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
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert TITLE269 in titoli
        assert "tab269" in dvars
        assert "tab269" in withs
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[-1] == TITLE372
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
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


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
