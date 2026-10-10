"""Test tab265 'Fine vita FV: revamping vs dismissione': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab265.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("fv265_num", "fv265_anni", "fv265_produzione_annua",
          "fv265_npv_ricavi", "fv265_scenario_revamping",
          "fv265_scenario_dismissione", "fv265_confronto",
          "fv265_anno_pareggio", "fv265_sensibilita_prezzo")
fv265_num = _F["fv265_num"]
fv265_anni = _F["fv265_anni"]
fv265_produzione_annua = _F["fv265_produzione_annua"]
fv265_npv_ricavi = _F["fv265_npv_ricavi"]
fv265_scenario_revamping = _F["fv265_scenario_revamping"]
fv265_scenario_dismissione = _F["fv265_scenario_dismissione"]
fv265_confronto = _F["fv265_confronto"]
fv265_anno_pareggio = _F["fv265_anno_pareggio"]
fv265_sensibilita_prezzo = _F["fv265_sensibilita_prezzo"]

APP = Path(__file__).parent.parent / "app.py"

TITLE265 = "\U0000267B\uFE0F Fine vita FV: revamping vs dismissione"
TITLE266 = "\U0001F33E\uFE0F Agrivoltaico: doppio reddito"
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
TITLE264 = "\U0001F4DC Garanzie di origine: costo del 100% rinnovabile"

PROD0 = 100000.0
DEGRADO = 0.5
PREZZO = 0.12
ANNI = 10
TASSO = 5.0
OEM = 1500.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab265:
    def test_tab265_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 369
        assert TITLE265 in titoli
        assert "tab265" in dvars
        assert "tab265" in withs
        assert titoli[dvars.index("tab265")] == TITLE265
        assert titoli[-1] == TITLE369
        keys = re.findall(r'key="(fv265_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_264_265(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab264")] == TITLE264
        assert titoli[dvars.index("tab265")] == TITLE265
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


class TestFv265Num:
    def test_ok(self):
        assert fv265_num(3, "x") == 3.0
        assert fv265_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                fv265_num(bad, "x")

    def test_anni(self):
        assert fv265_anni(10, "anni") == 10
        assert fv265_anni(10.0, "anni") == 10
        for bad in (0, -3, 2.5, "10"):
            with pytest.raises(ValueError):
                fv265_anni(bad, "anni")


class TestFv265ProduzioneAnnua:
    def test_anno1_e_anno2(self):
        assert fv265_produzione_annua(PROD0, DEGRADO, 1) == pytest.approx(PROD0)
        assert fv265_produzione_annua(PROD0, DEGRADO, 2) == pytest.approx(PROD0 * 0.995)

    def test_degrado_nullo(self):
        assert fv265_produzione_annua(PROD0, 0.0, 7) == pytest.approx(PROD0)

    def test_monotonia(self):
        prods = [fv265_produzione_annua(PROD0, DEGRADO, a) for a in range(1, 11)]
        assert all(b < a for a, b in zip(prods, prods[1:]))

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_produzione_annua(-1.0, DEGRADO, 1)
        with pytest.raises(ValueError):
            fv265_produzione_annua(PROD0, 51.0, 1)
        with pytest.raises(ValueError):
            fv265_produzione_annua(PROD0, -0.1, 1)
        with pytest.raises(ValueError):
            fv265_produzione_annua(PROD0, DEGRADO, 0)


class TestFv265NpvRicavi:
    def test_tasso_zero(self):
        r = fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, 0.0, OEM)
        atteso = sum(fv265_produzione_annua(PROD0, DEGRADO, a) for a in range(1, ANNI + 1)) * PREZZO - OEM * ANNI
        assert r["npv"] == pytest.approx(atteso)

    def test_chiavi_e_coerenza(self):
        r = fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        assert set(r) == {"npv", "produzioni", "flussi_attualizzati", "produzione_totale_kwh"}
        assert len(r["produzioni"]) == len(r["flussi_attualizzati"]) == ANNI
        assert r["produzione_totale_kwh"] == pytest.approx(sum(r["produzioni"]))
        assert r["npv"] == pytest.approx(sum(r["flussi_attualizzati"]))
        assert r["produzioni"][0] == pytest.approx(PROD0)

    def test_sconto_riduce_npv(self):
        r0 = fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, 0.0, OEM)
        r5 = fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        assert r5["npv"] < r0["npv"]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_npv_ricavi(PROD0, DEGRADO, -0.1, ANNI, TASSO, OEM)
        with pytest.raises(ValueError):
            fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, -1.0, OEM)
        with pytest.raises(ValueError):
            fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, 0, TASSO, OEM)
        with pytest.raises(ValueError):
            fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, TASSO, -10.0)


class TestFv265Revamping:
    def test_base(self):
        # ripristino 95%: produzione riparte da 95000 kWh
        r = fv265_scenario_revamping(PROD0, 45000.0, 95.0, 0.4, PREZZO, ANNI, TASSO, OEM)
        base = fv265_npv_ricavi(PROD0 * 0.95, 0.4, PREZZO, ANNI, TASSO, OEM)
        assert r["costo_revamping"] == pytest.approx(45000.0)
        assert r["npv"] == pytest.approx(base["npv"] - 45000.0)
        assert r["produzioni"][0] == pytest.approx(PROD0 * 0.95)

    def test_costo_zero_uguale_a_ricavi(self):
        r = fv265_scenario_revamping(PROD0, 0.0, 100.0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        m = fv265_npv_ricavi(PROD0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        assert r["npv"] == pytest.approx(m["npv"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_scenario_revamping(PROD0, -1.0, 95.0, 0.4, PREZZO, ANNI, TASSO, OEM)
        with pytest.raises(ValueError):
            fv265_scenario_revamping(PROD0, 45000.0, 0.0, 0.4, PREZZO, ANNI, TASSO, OEM)
        with pytest.raises(ValueError):
            fv265_scenario_revamping(PROD0, 45000.0, 101.0, 0.4, PREZZO, ANNI, TASSO, OEM)
        with pytest.raises(ValueError):
            fv265_scenario_revamping(PROD0, 45000.0, 95.0, 60.0, PREZZO, ANNI, TASSO, OEM)


class TestFv265Dismissione:
    def test_base(self):
        r = fv265_scenario_dismissione(8000.0, 2000.0)
        assert r["npv"] == pytest.approx(-6000.0)
        assert r["costo_netto"] == pytest.approx(6000.0)

    def test_valore_supera_costo(self):
        r = fv265_scenario_dismissione(1000.0, 5000.0)
        assert r["npv"] == pytest.approx(4000.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_scenario_dismissione(-1.0, 2000.0)
        with pytest.raises(ValueError):
            fv265_scenario_dismissione(8000.0, -5.0)


class TestFv265Confronto:
    def test_vince_revamping(self):
        r = fv265_confronto(100.0, 130.0, -50.0)
        assert r["verdetto"] == "revamping"
        assert r["migliore"] == "revamping"
        assert r["secondo"] == "mantieni"
        assert r["margine_pct"] == pytest.approx(30.0)

    def test_vince_dismissione(self):
        r = fv265_confronto(-100.0, -200.0, 10.0)
        assert r["verdetto"] == "dismissione"
        assert r["margine_pct"] == pytest.approx(110.0)

    def test_indifferente(self):
        r = fv265_confronto(100.0, 103.0, -50.0)
        assert r["verdetto"] == "indifferente"
        assert r["margine_pct"] == pytest.approx(3.0)

    def test_secondo_zero(self):
        r = fv265_confronto(50.0, 0.0, -10.0)
        assert r["verdetto"] == "mantieni"
        assert r["margine_pct"] is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_confronto("100", 130.0, -50.0)


class TestFv265Pareggio:
    def test_costo_zero_pareggio_anno1(self):
        a = fv265_anno_pareggio(PROD0, DEGRADO, 0.0, 100.0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        assert a == 1

    def test_costo_enorme_mai(self):
        a = fv265_anno_pareggio(PROD0, DEGRADO, 1e12, 100.0, DEGRADO, PREZZO, ANNI, TASSO, OEM)
        assert a is None

    def test_pareggio_intermedio(self):
        # revamping ripristino 100% + degrado minore: pareggia entro l'orizzonte
        a = fv265_anno_pareggio(PROD0, 2.0, 5000.0, 100.0, 0.1, PREZZO, ANNI, TASSO, OEM)
        assert a is not None and 1 <= a <= ANNI

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_anno_pareggio(PROD0, DEGRADO, -1.0, 100.0, DEGRADO, PREZZO, ANNI, TASSO, OEM)


class TestFv265Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = fv265_sensibilita_prezzo(PROD0, DEGRADO, 0.4, 95.0, 45000.0, OEM, ANNI, TASSO, 0.2, 0.1)
        assert len(righe) == 3
        assert righe[0]["prezzo_kwh"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_kwh"] == pytest.approx(0.2)
        assert set(righe[0]) == {"prezzo_kwh", "npv_mantieni", "npv_revamping"}

    def test_monotonia_e_coerenza(self):
        righe = fv265_sensibilita_prezzo(PROD0, DEGRADO, 0.4, 95.0, 45000.0, OEM, ANNI, TASSO, 0.2, 0.1)
        nm = [r["npv_mantieni"] for r in righe]
        nr = [r["npv_revamping"] for r in righe]
        assert all(b > a for a, b in zip(nm, nm[1:]))
        assert all(b > a for a, b in zip(nr, nr[1:]))
        assert righe[1]["npv_mantieni"] == pytest.approx(
            fv265_npv_ricavi(PROD0, DEGRADO, 0.1, ANNI, TASSO, OEM)["npv"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fv265_sensibilita_prezzo(PROD0, DEGRADO, 0.4, 95.0, 45000.0, OEM, ANNI, TASSO, 0.0, 0.1)
        with pytest.raises(ValueError):
            fv265_sensibilita_prezzo(PROD0, DEGRADO, 0.4, 95.0, 45000.0, OEM, ANNI, TASSO, 0.2, 0.0)
