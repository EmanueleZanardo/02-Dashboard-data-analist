"""Test tab268 'Eolico onshore: business case': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab268.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("eo268_num", "eo268_int", "eo268_produzione_annua", "eo268_quota_capex",
          "eo268_costo_annuo", "eo268_lcoe", "eo268_prezzo_catturato",
          "eo268_ricavi", "eo268_margine", "eo268_fattore_rendita",
          "eo268_van", "eo268_payback", "eo268_confronto", "eo268_sensibilita")
eo268_num = _F["eo268_num"]
eo268_int = _F["eo268_int"]
eo268_produzione_annua = _F["eo268_produzione_annua"]
eo268_quota_capex = _F["eo268_quota_capex"]
eo268_costo_annuo = _F["eo268_costo_annuo"]
eo268_lcoe = _F["eo268_lcoe"]
eo268_prezzo_catturato = _F["eo268_prezzo_catturato"]
eo268_ricavi = _F["eo268_ricavi"]
eo268_margine = _F["eo268_margine"]
eo268_fattore_rendita = _F["eo268_fattore_rendita"]
eo268_van = _F["eo268_van"]
eo268_payback = _F["eo268_payback"]
eo268_confronto = _F["eo268_confronto"]
eo268_sensibilita = _F["eo268_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE267 = "🟢 Biometano: business case"

POT = 10.0
ORE = 2500.0
CAPEX = 12_000_000.0
OEM_PCT = 2.5
OPEX_KW = 40.0
ANNI = 25
TASSO = 5.0
P_BASE = 75.0
SCONTO = 12.0

MWH = POT * ORE               # 25_000
P_CATT = P_BASE * (1 - SCONTO / 100.0)   # 66.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab268:
    def test_tab268_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 352
        assert TITLE268 in titoli
        assert "tab268" in dvars
        assert "tab268" in withs
        assert titoli[dvars.index("tab268")] == TITLE268
        assert titoli[-1] == TITLE352
        keys = re.findall(r'key="(eo268_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_267_268(self):
        _, titoli, dvars, _ = _registry()
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


class TestEo268Num:
    def test_ok(self):
        assert eo268_num(3, "x") == 3.0
        assert eo268_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                eo268_num(bad, "x")

    def test_int(self):
        assert eo268_int(25, "anni") == 25
        assert eo268_int(25.0, "anni") == 25
        for bad in (0, -3, 2.5, "25"):
            with pytest.raises(ValueError):
                eo268_int(bad, "anni")


class TestEo268Produzione:
    def test_base(self):
        assert eo268_produzione_annua(POT, ORE) == pytest.approx(MWH)

    def test_ore_max(self):
        assert eo268_produzione_annua(1.0, 8760.0) == pytest.approx(8760.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_produzione_annua(0.0, ORE)
        with pytest.raises(ValueError):
            eo268_produzione_annua(POT, 0.0)
        with pytest.raises(ValueError):
            eo268_produzione_annua(POT, 8761.0)


class TestEo268CostoAnnuo:
    def test_chiavi_e_scomposizione(self):
        c = eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        assert set(c) == {"quota_capex", "oem", "opex_fisso", "totale"}
        atteso_quota = CAPEX * (0.05 / (1.0 - 1.05 ** -ANNI))
        assert c["quota_capex"] == pytest.approx(atteso_quota)
        assert c["oem"] == pytest.approx(CAPEX * 0.025)
        assert c["opex_fisso"] == pytest.approx(POT * 1000.0 * OPEX_KW)
        assert c["totale"] == pytest.approx(c["quota_capex"] + c["oem"] + c["opex_fisso"])

    def test_tasso_zero(self):
        c = eo268_costo_annuo(CAPEX, ANNI, 0.0, OEM_PCT, OPEX_KW, POT)
        assert c["quota_capex"] == pytest.approx(CAPEX / ANNI)

    def test_quota_capex_diretta(self):
        assert eo268_quota_capex(CAPEX, ANNI, 0.0) == pytest.approx(CAPEX / ANNI)
        assert eo268_quota_capex(CAPEX, 1, 5.0) == pytest.approx(CAPEX * 1.05)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_costo_annuo(-1.0, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        with pytest.raises(ValueError):
            eo268_costo_annuo(CAPEX, 0, TASSO, OEM_PCT, OPEX_KW, POT)
        with pytest.raises(ValueError):
            eo268_costo_annuo(CAPEX, ANNI, -1.0, OEM_PCT, OPEX_KW, POT)
        with pytest.raises(ValueError):
            eo268_costo_annuo(CAPEX, ANNI, TASSO, 101.0, OPEX_KW, POT)
        with pytest.raises(ValueError):
            eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, -1.0, POT)
        with pytest.raises(ValueError):
            eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, 0.0)


class TestEo268Lcoe:
    def test_base(self):
        c = eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        assert eo268_lcoe(c["totale"], MWH) == pytest.approx(c["totale"] / MWH)

    def test_produzione_nulla(self):
        assert eo268_lcoe(1_000_000.0, 0.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_lcoe(-1.0, MWH)
        with pytest.raises(ValueError):
            eo268_lcoe(1_000_000.0, -5.0)


class TestEo268PrezzoCatturato:
    def test_base(self):
        assert eo268_prezzo_catturato(P_BASE, SCONTO) == pytest.approx(P_CATT)

    def test_sconto_zero(self):
        assert eo268_prezzo_catturato(P_BASE, 0.0) == pytest.approx(P_BASE)

    def test_sconto_pieno(self):
        assert eo268_prezzo_catturato(P_BASE, 100.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_prezzo_catturato(-1.0, SCONTO)
        with pytest.raises(ValueError):
            eo268_prezzo_catturato(P_BASE, -1.0)
        with pytest.raises(ValueError):
            eo268_prezzo_catturato(P_BASE, 100.5)


class TestEo268RicaviMargine:
    def test_ricavi(self):
        assert eo268_ricavi(MWH, P_CATT) == pytest.approx(MWH * P_CATT)
        assert eo268_ricavi(MWH, P_BASE) == pytest.approx(MWH * P_BASE)

    def test_margine(self):
        assert eo268_margine(1_650_000.0, 1_500_000.0) == pytest.approx(150_000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_ricavi(MWH, -1.0)
        with pytest.raises(ValueError):
            eo268_ricavi(-1.0, P_CATT)
        with pytest.raises(ValueError):
            eo268_margine(100.0, -1.0)


class TestEo268FattoreRendita:
    def test_tasso_zero(self):
        assert eo268_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert eo268_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert eo268_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            eo268_fattore_rendita(5.0, 0)


class TestEo268VanPayback:
    def test_van(self):
        atteso = 100_000.0 * sum(1 / 1.05 ** t for t in range(1, 11))
        assert eo268_van(100_000.0, 10, 5.0) == pytest.approx(atteso)

    def test_van_negativo(self):
        assert eo268_van(-50_000.0, 10, 5.0) < 0

    def test_payback(self):
        assert eo268_payback(CAPEX, 800_000.0) == pytest.approx(15.0)

    def test_payback_mai(self):
        assert eo268_payback(CAPEX, 0.0) is None
        assert eo268_payback(CAPEX, -10.0) is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_payback(-1.0, 800_000.0)
        with pytest.raises(ValueError):
            eo268_van(100.0, 0, 5.0)


class TestEo268Confronto:
    def test_non_competitivo(self):
        r = eo268_confronto(70.0, P_CATT)
        assert r["verdetto"] == "non_competitivo"
        assert r["prezzo_catturato"] == pytest.approx(66.0)
        assert r["margine_eur_mwh"] == pytest.approx(-4.0)
        assert r["soglia_eur_mwh"] == pytest.approx(3.3)

    def test_competitivo(self):
        r = eo268_confronto(60.0, P_CATT)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(6.0)

    def test_competitivo_al_limite(self):
        # numeri esatti in binario: margine == soglia == 5.0 -> competitivo
        r = eo268_confronto(95.0, 100.0)
        assert r["verdetto"] == "competitivo"
        assert r["margine_eur_mwh"] == pytest.approx(5.0)
        assert r["soglia_eur_mwh"] == pytest.approx(5.0)

    def test_indifferente(self):
        r = eo268_confronto(65.0, P_CATT)
        assert r["verdetto"] == "indifferente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            eo268_confronto(-1.0, P_CATT)
        with pytest.raises(ValueError):
            eo268_confronto(60.0, 0.0)


class TestEo268Sensibilita:
    def test_lunghezza_e_chiavi(self):
        c = eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        righe = eo268_sensibilita(150.0, 75.0, MWH, c["totale"], SCONTO)
        assert len(righe) == 3
        assert righe[0]["prezzo_baseload"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_baseload"] == pytest.approx(150.0)
        assert set(righe[0]) == {"prezzo_baseload", "prezzo_catturato",
                                 "ricavi_annui", "margine_annuo"}

    def test_monotonia_e_coerenza(self):
        c = eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        righe = eo268_sensibilita(150.0, 75.0, MWH, c["totale"], SCONTO)
        mg = [r["margine_annuo"] for r in righe]
        assert all(b > a for a, b in zip(mg, mg[1:]))
        assert righe[1]["prezzo_catturato"] == pytest.approx(P_CATT)
        assert righe[1]["ricavi_annui"] == pytest.approx(MWH * P_CATT)
        assert righe[1]["margine_annuo"] == pytest.approx(MWH * P_CATT - c["totale"])

    def test_invalidi(self):
        c = eo268_costo_annuo(CAPEX, ANNI, TASSO, OEM_PCT, OPEX_KW, POT)
        with pytest.raises(ValueError):
            eo268_sensibilita(0.0, 75.0, MWH, c["totale"], SCONTO)
        with pytest.raises(ValueError):
            eo268_sensibilita(150.0, 0.0, MWH, c["totale"], SCONTO)
