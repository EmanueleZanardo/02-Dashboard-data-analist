"""Test tab263 'Flotta aziendale: TCO diesel vs elettrico': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab263.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("fl263_num", "fl263_quota_annua", "fl263_costo_annuo_veicolo",
          "fl263_emissioni_annue", "fl263_confronto", "fl263_break_even_km",
          "fl263_van", "fl263_sensibilita_km")
fl263_num = _F["fl263_num"]
fl263_quota_annua = _F["fl263_quota_annua"]
fl263_costo_annuo_veicolo = _F["fl263_costo_annuo_veicolo"]
fl263_emissioni_annue = _F["fl263_emissioni_annue"]
fl263_confronto = _F["fl263_confronto"]
fl263_break_even_km = _F["fl263_break_even_km"]
fl263_van = _F["fl263_van"]
fl263_sensibilita_km = _F["fl263_sensibilita_km"]

APP = Path(__file__).parent.parent / "app.py"

TITLE263 = "\U0001F697 Flotta aziendale: TCO diesel vs elettrico"
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
TITLE262 = "\U0001F50C Gruppo elettrogeno vs blackout"

# Parametri di riferimento usati nei test
D = dict(capex=28000.0, valore_residuo_pct=30.0, anni=5.0, km_anno=30000.0,
         consumo_100km=6.5, prezzo_unitario=1.75, manut_eur_km=0.06,
         costi_fissi_annui=900.0)
E = dict(capex=42000.0, valore_residuo_pct=30.0, anni=5.0, km_anno=30000.0,
         consumo_100km=18.0, prezzo_unitario=0.25, manut_eur_km=0.04,
         costi_fissi_annui=700.0)
P = dict(n_veicoli=10.0, km_anno=30000.0, anni=5.0, tasso_pct=4.0,
         d_capex=28000.0, d_residuo_pct=30.0, d_consumo=6.5, d_prezzo=1.75,
         d_manut_km=0.06, d_fissi=900.0,
         e_capex=42000.0, e_residuo_pct=30.0, e_consumo=18.0, e_prezzo=0.25,
         e_manut_km=0.04, e_fissi=700.0)
P_BE = {k: v for k, v in P.items()
        if k not in ("n_veicoli", "km_anno", "tasso_pct")}


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab263:
    def test_tab263_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 370
        assert TITLE263 in titoli
        assert "tab263" in dvars
        assert "tab263" in withs
        assert titoli[dvars.index("tab263")] == TITLE263
        assert titoli[-1] == TITLE370
        keys = re.findall(r'key="(fl263_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 16

    def test_titoli_allineati_262_263(self):
        _, titoli, dvars, _ = _registry()
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


class TestFl263Num:
    def test_ok(self):
        assert fl263_num(3, "x") == 3.0
        assert fl263_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                fl263_num(bad, "x")


class TestFl263Quota:
    def test_base(self):
        # (28000 - 30%) / 5 = 19600 / 5 = 3920
        assert fl263_quota_annua(28000.0, 30.0, 5.0) == pytest.approx(3920.0)

    def test_residuo_zero(self):
        assert fl263_quota_annua(28000.0, 0.0, 5.0) == pytest.approx(5600.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fl263_quota_annua(-100.0, 30.0, 5.0)
        with pytest.raises(ValueError):
            fl263_quota_annua(28000.0, 101.0, 5.0)
        with pytest.raises(ValueError):
            fl263_quota_annua(28000.0, 30.0, 0.0)


class TestFl263CostoVeicolo:
    def test_diesel(self):
        v = fl263_costo_annuo_veicolo(**D)
        assert set(v) == {"quota_annua", "costo_carburante",
                          "costo_manutenzione", "costi_fissi",
                          "costo_totale", "costo_per_km"}
        assert v["quota_annua"] == pytest.approx(3920.0)
        # 30000 * 6,5/100 * 1,75 = 3412,50
        assert v["costo_carburante"] == pytest.approx(3412.5)
        assert v["costo_manutenzione"] == pytest.approx(1800.0)
        assert v["costi_fissi"] == pytest.approx(900.0)
        assert v["costo_totale"] == pytest.approx(10032.5)
        assert v["costo_per_km"] == pytest.approx(10032.5 / 30000.0)

    def test_elettrico(self):
        v = fl263_costo_annuo_veicolo(**E)
        assert v["quota_annua"] == pytest.approx(5880.0)
        # 30000 * 18/100 * 0,25 = 1350
        assert v["costo_carburante"] == pytest.approx(1350.0)
        assert v["costo_manutenzione"] == pytest.approx(1200.0)
        assert v["costo_totale"] == pytest.approx(9130.0)

    def test_km_zero(self):
        v = fl263_costo_annuo_veicolo(**{**D, "km_anno": 0.0})
        assert v["costo_totale"] == pytest.approx(3920.0 + 900.0)
        assert v["costo_per_km"] == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fl263_costo_annuo_veicolo(**{**D, "km_anno": -1.0})
        with pytest.raises(ValueError):
            fl263_costo_annuo_veicolo(**{**D, "prezzo_unitario": -0.5})


class TestFl263Confronto:
    def test_conviene_elettrico(self):
        c = fl263_confronto(**P)
        assert c["tco_diesel_flotta"] == pytest.approx(100325.0)
        assert c["tco_elettrico_flotta"] == pytest.approx(91300.0)
        assert c["risparmio_annuo"] == pytest.approx(9025.0)
        assert c["risparmio_pct"] == pytest.approx(9025.0 / 100325.0 * 100.0)
        assert c["verdetto"] == "elettrico"
        assert c["delta_capex"] == pytest.approx(140000.0)
        # 140000 / 9025 = 15,51 anni
        assert c["payback_anni"] == pytest.approx(15.51, rel=1e-2)
        # -140000 + 9025 * (1-1,04^-5)/0,04 = -99822
        assert c["van"] == pytest.approx(-99822.0, rel=1e-3)

    def test_conviene_diesel(self):
        q = dict(P)
        q["km_anno"] = 5000.0
        c = fl263_confronto(**q)
        assert c["verdetto"] == "diesel"
        assert c["risparmio_annuo"] < 0
        assert c["payback_anni"] is None

    def test_indifferente(self):
        # ai km di pareggio il risparmio e' nullo
        be = fl263_break_even_km(**P_BE)
        q = dict(P)
        q["km_anno"] = be
        c = fl263_confronto(**q)
        assert c["verdetto"] == "indifferente"
        assert abs(c["risparmio_annuo"]) <= 0.05 * c["tco_diesel_flotta"]

    def test_n_veicoli_invalido(self):
        with pytest.raises(ValueError):
            fl263_confronto(**{**P, "n_veicoli": 0.0})


class TestFl263BreakEven:
    def test_forma_chiusa(self):
        be = fl263_break_even_km(**P_BE)
        fixed = (5880.0 - 3920.0) + (700.0 - 900.0)  # 1760
        marg = (0.065 * 1.75 + 0.06) - (0.18 * 0.25 + 0.04)  # 0,08875
        assert be == pytest.approx(fixed / marg)
        assert be == pytest.approx(19831.0, rel=1e-3)

    def test_mai_conveniente(self):
        # elettricita' a 1 €/kWh: costo variabile elettrico > diesel
        q = dict(P_BE)
        q["e_prezzo"] = 1.0
        assert fl263_break_even_km(**q) is None


class TestFl263Van:
    def test_base(self):
        # -140000 + 9025 * 4,4518 = -99822
        assert fl263_van(140000.0, 9025.0, 5.0, 4.0) == pytest.approx(-99822.0, rel=1e-3)

    def test_tasso_zero(self):
        assert fl263_van(140000.0, 9025.0, 5.0, 0.0) == pytest.approx(-94875.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fl263_van(140000.0, 9025.0, 0.0, 4.0)
        with pytest.raises(ValueError):
            fl263_van(140000.0, 9025.0, 5.0, -1.0)


class TestFl263Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = fl263_sensibilita_km(60000.0, 30000.0, **P_BE)
        assert len(righe) == 3
        assert righe[0]["km"] == pytest.approx(0.0)
        assert righe[-1]["km"] == pytest.approx(60000.0)
        assert set(righe[0]) == {"km", "tco_diesel", "tco_elettrico"}

    def test_monotonia_e_coerenza(self):
        righe = fl263_sensibilita_km(60000.0, 30000.0, **P_BE)
        td = [r["tco_diesel"] for r in righe]
        te = [r["tco_elettrico"] for r in righe]
        assert all(b > a for a, b in zip(td, td[1:]))
        assert all(b > a for a, b in zip(te, te[1:]))
        vd = fl263_costo_annuo_veicolo(**{**D, "km_anno": 30000.0})
        ve = fl263_costo_annuo_veicolo(**{**E, "km_anno": 30000.0})
        assert righe[1]["tco_diesel"] == pytest.approx(vd["costo_totale"])
        assert righe[1]["tco_elettrico"] == pytest.approx(ve["costo_totale"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fl263_sensibilita_km(0.0, 30000.0, **P_BE)
        with pytest.raises(ValueError):
            fl263_sensibilita_km(60000.0, 0.0, **P_BE)


class TestFl263Emissioni:
    def test_diesel(self):
        # 30000 * 6,5/100 * 2,68 = 5226 kg
        assert fl263_emissioni_annue(30000.0, 6.5, 2.68) == pytest.approx(5226.0)

    def test_elettrico(self):
        # 30000 * 18/100 * 0,10 = 540 kg
        assert fl263_emissioni_annue(30000.0, 18.0, 0.10) == pytest.approx(540.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            fl263_emissioni_annue(-1.0, 6.5, 2.68)
        with pytest.raises(ValueError):
            fl263_emissioni_annue(30000.0, 6.5, -0.5)
