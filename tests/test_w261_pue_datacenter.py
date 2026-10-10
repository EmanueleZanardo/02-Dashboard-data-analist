"""Test tab261 'PUE & costo data center': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab261.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pue261_num", "pue261_potenza_totale_kw",
          "pue261_energia_annua_mwh", "pue261_overhead_pct",
          "pue261_costo_annuo_energia", "pue261_costo_totale_annuo",
          "pue261_risparmio_miglioramento", "pue261_emissioni_tco2",
          "pue261_giudizio", "pue261_sensibilita")
pue261_num = _F["pue261_num"]
pue261_potenza_totale_kw = _F["pue261_potenza_totale_kw"]
pue261_energia_annua_mwh = _F["pue261_energia_annua_mwh"]
pue261_overhead_pct = _F["pue261_overhead_pct"]
pue261_costo_annuo_energia = _F["pue261_costo_annuo_energia"]
pue261_costo_totale_annuo = _F["pue261_costo_totale_annuo"]
pue261_risparmio_miglioramento = _F["pue261_risparmio_miglioramento"]
pue261_emissioni_tco2 = _F["pue261_emissioni_tco2"]
pue261_giudizio = _F["pue261_giudizio"]
pue261_sensibilita = _F["pue261_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"

TITLE261 = "🏢 PUE & costo data center"
TITLE262 = "🔌 Gruppo elettrogeno vs blackout"
TITLE263 = "🚗 Flotta aziendale: TCO diesel vs elettrico"
TITLE264 = "📜 Garanzie di origine: costo del 100% rinnovabile"
TITLE265 = "♻️ Fine vita FV: revamping vs dismissione"
TITLE266 = "🌾️ Agrivoltaico: doppio reddito"
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
TITLE260 = "❄️ Pompa di calore vs caldaia"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab261:
    def test_tab261_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 353
        assert TITLE261 in titoli
        assert "tab261" in dvars
        assert "tab261" in withs
        assert titoli[dvars.index("tab261")] == TITLE261
        assert titoli[-1] == TITLE353
        keys = re.findall(r'key="(pue261_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_260_261(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab260")] == TITLE260
        assert titoli[dvars.index("tab261")] == TITLE261
        assert titoli[dvars.index("tab262")] == TITLE262
        assert titoli[dvars.index("tab263")] == TITLE263
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


class TestPue261Num:
    def test_ok(self):
        assert pue261_num(3, "x") == 3.0
        assert pue261_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                pue261_num(bad, "x")


class TestPue261Potenza:
    def test_base(self):
        assert pue261_potenza_totale_kw(500.0, 1.5) == pytest.approx(750.0)

    def test_pue_uno(self):
        assert pue261_potenza_totale_kw(100.0, 1.0) == pytest.approx(100.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pue261_potenza_totale_kw(100.0, 0.9)
        with pytest.raises(ValueError):
            pue261_potenza_totale_kw(-10.0, 1.5)


class TestPue261Energia:
    def test_annua(self):
        # 750 kW * 8760 h / 1000 = 6570 MWh
        assert pue261_energia_annua_mwh(500.0, 1.5) == pytest.approx(6570.0)

    def test_ore_custom(self):
        assert pue261_energia_annua_mwh(500.0, 1.5, 4000.0) == pytest.approx(3000.0)

    def test_ore_zero_errore(self):
        with pytest.raises(ValueError):
            pue261_energia_annua_mwh(500.0, 1.5, 0.0)


class TestPue261Overhead:
    def test_base(self):
        assert pue261_overhead_pct(1.5) == pytest.approx(33.333333)

    def test_pue_uno_zero(self):
        assert pue261_overhead_pct(1.0) == pytest.approx(0.0)

    def test_pue_sotto_uno_errore(self):
        with pytest.raises(ValueError):
            pue261_overhead_pct(0.99)


class TestPue261Costi:
    def test_costo_energia(self):
        assert pue261_costo_annuo_energia(6570.0, 180.0) == pytest.approx(1182600.0)

    def test_costo_totale_con_potenza(self):
        # 6570*180 = 1.182.600 + 750 kW * 50 = 37.500
        assert pue261_costo_totale_annuo(500.0, 1.5, 180.0, 8760.0, 50.0) == pytest.approx(1220100.0)

    def test_costo_totale_senza_potenza(self):
        e = pue261_energia_annua_mwh(500.0, 1.5)
        assert pue261_costo_totale_annuo(500.0, 1.5, 180.0) == pytest.approx(
            pue261_costo_annuo_energia(e, 180.0))

    def test_costo_potenza_negativo_errore(self):
        with pytest.raises(ValueError):
            pue261_costo_totale_annuo(500.0, 1.5, 180.0, 8760.0, -1.0)


class TestPue261Risparmio:
    def test_base(self):
        r = pue261_risparmio_miglioramento(500.0, 1.5, 1.3, 180.0)
        assert r["risparmio_mwh"] == pytest.approx(876.0)
        assert r["risparmio_eur"] == pytest.approx(157680.0)
        assert r["risparmio_pct"] == pytest.approx(876.0 / 6570.0 * 100.0)

    def test_target_uguale_zero(self):
        r = pue261_risparmio_miglioramento(500.0, 1.5, 1.5, 180.0)
        assert r["risparmio_mwh"] == pytest.approx(0.0)
        assert r["risparmio_eur"] == pytest.approx(0.0)

    def test_target_peggiore_errore(self):
        with pytest.raises(ValueError):
            pue261_risparmio_miglioramento(500.0, 1.3, 1.5, 180.0)


class TestPue261EmissioniGiudizio:
    def test_emissioni(self):
        assert pue261_emissioni_tco2(6570.0, 0.35) == pytest.approx(2299.5)

    def test_giudizio_soglie(self):
        assert pue261_giudizio(1.2) == "ottimo"
        assert pue261_giudizio(1.3) == "buono"
        assert pue261_giudizio(1.59) == "buono"
        assert pue261_giudizio(1.6) == "medio"
        assert pue261_giudizio(1.99) == "medio"
        assert pue261_giudizio(2.0) == "critico"
        assert pue261_giudizio(2.5) == "critico"

    def test_giudizio_pue_sotto_uno_errore(self):
        with pytest.raises(ValueError):
            pue261_giudizio(0.9)


class TestPue261Sensibilita:
    def test_lunghezza_e_monotonia(self):
        righe = pue261_sensibilita(500.0, 1.0, 2.0, 0.25, 180.0)
        assert len(righe) == 5
        assert righe[0]["pue"] == pytest.approx(1.0)
        assert righe[-1]["pue"] == pytest.approx(2.0)
        costi = [r["costo_eur"] for r in righe]
        assert all(b > a for a, b in zip(costi, costi[1:]))

    def test_chiavi_e_valore(self):
        r = pue261_sensibilita(500.0, 1.5, 1.5, 0.5, 180.0)[0]
        assert set(r) == {"pue", "energia_mwh", "costo_eur"}
        assert r["energia_mwh"] == pytest.approx(6570.0)
        assert r["costo_eur"] == pytest.approx(6570.0 * 180.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 0.9, 2.0, 0.25, 180.0)
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 2.0, 1.0, 0.25, 180.0)
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 1.0, 2.0, 0.0, 180.0)
