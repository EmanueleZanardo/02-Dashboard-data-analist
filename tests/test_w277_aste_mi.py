"""Test tab277 'Aste MI: scostamenti vs MGP': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab277.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("mi277_sessioni", "mi277_num", "mi277_valida_sessione", "mi277_parse_prezzi",
          "mi277_spread", "mi277_spread_pct", "mi277_segnale",
          "mi277_analizza", "mi277_statistiche", "mi277_classifica",
          "mi277_sintesi")
mi277_sessioni = _F["mi277_sessioni"]
mi277_num = _F["mi277_num"]
mi277_valida_sessione = _F["mi277_valida_sessione"]
mi277_parse_prezzi = _F["mi277_parse_prezzi"]
mi277_spread = _F["mi277_spread"]
mi277_spread_pct = _F["mi277_spread_pct"]
mi277_segnale = _F["mi277_segnale"]
mi277_analizza = _F["mi277_analizza"]
mi277_statistiche = _F["mi277_statistiche"]
mi277_classifica = _F["mi277_classifica"]
mi277_sintesi = _F["mi277_sintesi"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE276 = "💧 Cash flow at risk (CFaR)"

CSV_PREZZI = "sessione,prezzo_eur_mwh\nMI1,102.5\nMI2,98.0\nMI7,105.0\n"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab277:
    def test_tab277_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 361
        assert TITLE277 in titoli
        assert "tab277" in dvars
        assert "tab277" in withs
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[-1] == TITLE361
        keys = re.findall(r'key="(mi277_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_276_277(self):
        _, titoli, dvars, _ = _registry()
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

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("mi277_sessioni", "mi277_num", "mi277_valida_sessione", "mi277_parse_prezzi",
                   "mi277_spread", "mi277_spread_pct", "mi277_segnale",
                   "mi277_analizza", "mi277_statistiche", "mi277_classifica",
                   "mi277_sintesi"):
            assert src.index(f"def {fn}(") < i_ws
            assert src.index("    with tab277:") > i_ws


class TestMi277NumSessione:
    def test_sessioni(self):
        assert mi277_sessioni() == ("MI1", "MI2", "MI3", "MI4", "MI5", "MI6", "MI7")

    def test_num_ok(self):
        assert mi277_num(100, "x") == 100.0
        assert mi277_num(98.5, "x") == 98.5

    def test_num_invalidi(self):
        import math
        for bad in (True, math.nan, "100", None):
            with pytest.raises(ValueError):
                mi277_num(bad, "x")

    def test_sessione_ok(self):
        assert mi277_valida_sessione("mi1") == "MI1"
        assert mi277_valida_sessione(" MI 7 ") == "MI7"

    def test_sessione_invalidi(self):
        for bad in ("MI8", "MGP", "", None, 3):
            with pytest.raises(ValueError):
                mi277_valida_sessione(bad)


class TestMi277ParsePrezzi:
    def test_base(self):
        pr = mi277_parse_prezzi(CSV_PREZZI)
        assert pr == {"MI1": 102.5, "MI2": 98.0, "MI7": 105.0}

    def test_senza_header(self):
        assert mi277_parse_prezzi("MI3,101.0") == {"MI3": 101.0}

    def test_invalidi(self):
        for bad in ("", "sessione\n", "MI1,xx", "MI9,100",
                    "MI1,-5", "MI1,100\nMI1,101", "MI1,100,extra"):
            with pytest.raises(ValueError):
                mi277_parse_prezzi(bad)


class TestMi277SpreadSegnale:
    def test_spread(self):
        assert mi277_spread(102.5, 100.0) == pytest.approx(2.5)
        assert mi277_spread(98.0, 100.0) == pytest.approx(-2.0)

    def test_spread_pct(self):
        assert mi277_spread_pct(2.5, 100.0) == pytest.approx(2.5)
        assert mi277_spread_pct(-2.0, 100.0) == pytest.approx(-2.0)
        assert mi277_spread_pct(2.5, 0.0) is None

    def test_segnale(self):
        assert mi277_segnale(2.5, 1.0) == "vendita_conveniente"
        assert mi277_segnale(-2.5, 1.0) == "acquisto_conveniente"
        assert mi277_segnale(0.5, 1.0) == "allineata"
        assert mi277_segnale(-0.5, 1.0) == "allineata"
        assert mi277_segnale(1.0, 1.0) == "allineata"

    def test_segnale_invalido(self):
        with pytest.raises(ValueError):
            mi277_segnale(1.0, -1.0)


class TestMi277Analizza:
    def test_base(self):
        pr = mi277_parse_prezzi(CSV_PREZZI)
        ana = mi277_analizza(pr, 100.0, tolleranza=1.0)
        assert [r["sessione"] for r in ana] == ["MI1", "MI2", "MI7"]
        assert ana[0]["spread_eur_mwh"] == pytest.approx(2.5)
        assert ana[0]["spread_pct"] == pytest.approx(2.5)
        assert ana[0]["segnale"] == "vendita_conveniente"
        assert ana[1]["segnale"] == "acquisto_conveniente"
        assert ana[2]["prezzo_mgp"] == 100.0

    def test_ordine_sessioni(self):
        pr = {"MI7": 100.0, "MI1": 100.0}
        ana = mi277_analizza(pr, 100.0)
        assert [r["sessione"] for r in ana] == ["MI1", "MI7"]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            mi277_analizza({}, 100.0)
        with pytest.raises(ValueError):
            mi277_analizza({"MI1": 100.0}, -5.0)


class TestMi277StatisticheSintesi:
    def test_statistiche(self):
        s = mi277_statistiche([2.5, -2.0, 5.0])
        assert s["n"] == 3
        assert s["media"] == pytest.approx(5.5 / 3)
        assert s["mediana"] == pytest.approx(2.5)
        assert s["min"] == pytest.approx(-2.0)
        assert s["max"] == pytest.approx(5.0)
        assert s["dev_std"] > 0
        assert s["quota_positive"] == pytest.approx(2 / 3)

    def test_statistiche_singolo(self):
        s = mi277_statistiche([3.0])
        assert s["dev_std"] == pytest.approx(0.0)
        assert s["mediana"] == pytest.approx(3.0)

    def test_statistiche_vuote(self):
        with pytest.raises(ValueError):
            mi277_statistiche([])

    def test_classifica(self):
        pr = mi277_parse_prezzi(CSV_PREZZI)
        ana = mi277_analizza(pr, 100.0)
        cla = mi277_classifica(ana)
        assert [r["sessione"] for r in cla] == ["MI7", "MI1", "MI2"]

    def test_sintesi(self):
        pr = mi277_parse_prezzi(CSV_PREZZI)
        ana = mi277_analizza(pr, 100.0, tolleranza=1.0)
        s = mi277_sintesi(ana)
        assert s["n_sessioni"] == 3
        assert s["migliore_vendita"] == "MI7"
        assert s["migliore_vendita_spread"] == pytest.approx(5.0)
        assert s["migliore_acquisto"] == "MI2"
        assert s["migliore_acquisto_spread"] == pytest.approx(-2.0)
        assert s["spread_medio"] == pytest.approx((2.5 - 2.0 + 5.0) / 3)
        assert s["n_vendita_conveniente"] == 2
        assert s["n_acquisto_conveniente"] == 1

    def test_sintesi_vuota(self):
        with pytest.raises(ValueError):
            mi277_sintesi([])
