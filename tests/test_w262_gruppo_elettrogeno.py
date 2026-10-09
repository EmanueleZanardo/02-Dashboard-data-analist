"""Test tab262 'Gruppo elettrogeno vs blackout': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab262.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("gen262_num", "gen262_costo_blackout_atteso", "gen262_consumo_lh",
          "gen262_costo_fuel_annuo", "gen262_quota_annua",
          "gen262_costo_annuo_gruppo", "gen262_confronto",
          "gen262_break_even_ore", "gen262_sensibilita_ore")
gen262_num = _F["gen262_num"]
gen262_costo_blackout_atteso = _F["gen262_costo_blackout_atteso"]
gen262_consumo_lh = _F["gen262_consumo_lh"]
gen262_costo_fuel_annuo = _F["gen262_costo_fuel_annuo"]
gen262_quota_annua = _F["gen262_quota_annua"]
gen262_costo_annuo_gruppo = _F["gen262_costo_annuo_gruppo"]
gen262_confronto = _F["gen262_confronto"]
gen262_break_even_ore = _F["gen262_break_even_ore"]
gen262_sensibilita_ore = _F["gen262_sensibilita_ore"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE261 = "🏢 PUE & costo data center"

# Parametri di riferimento usati nei test
P = dict(potenza_nom_kw=250.0, carico_kw=200.0, capex=45000.0, anni=15.0,
         tasso_pct=4.0, om_annuo=1500.0, prezzo_diesel_l=1.70,
         costo_kwh_non_fornito=5.0, ore_test_mese=1.0)
# Sottoinsieme senza VoLL per gen262_costo_annuo_gruppo
P_G = {k: v for k, v in P.items() if k != "costo_kwh_non_fornito"}


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab262:
    def test_tab262_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 323
        assert TITLE262 in titoli
        assert "tab262" in dvars
        assert "tab262" in withs
        assert titoli[dvars.index("tab262")] == TITLE262
        assert titoli[-1] == TITLE323
        keys = re.findall(r'key="(gen262_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_261_262(self):
        _, titoli, dvars, _ = _registry()
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


class TestGen262Num:
    def test_ok(self):
        assert gen262_num(3, "x") == 3.0
        assert gen262_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                gen262_num(bad, "x")


class TestGen262Blackout:
    def test_base(self):
        # 8 h * 200 kW * 5 €/kWh = 8000 €
        assert gen262_costo_blackout_atteso(8.0, 200.0, 5.0) == pytest.approx(8000.0)

    def test_zero_ore(self):
        assert gen262_costo_blackout_atteso(0.0, 200.0, 5.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gen262_costo_blackout_atteso(-1.0, 200.0, 5.0)
        with pytest.raises(ValueError):
            gen262_costo_blackout_atteso(8.0, -5.0, 5.0)
        with pytest.raises(ValueError):
            gen262_costo_blackout_atteso(8.0, 200.0, -1.0)


class TestGen262Consumo:
    def test_base(self):
        # 200*0,27 + 250*0,04 = 54 + 10 = 64 l/h
        assert gen262_consumo_lh(250.0, 200.0) == pytest.approx(64.0)

    def test_a_vuoto(self):
        assert gen262_consumo_lh(250.0, 0.0) == pytest.approx(10.0)

    def test_sovraccarico_errore(self):
        with pytest.raises(ValueError):
            gen262_consumo_lh(250.0, 251.0)

    def test_potenza_zero_errore(self):
        with pytest.raises(ValueError):
            gen262_consumo_lh(0.0, 0.0)


class TestGen262FuelQuota:
    def test_fuel_annuo(self):
        # 8 h * 64 l/h * 1,70 €/l = 870,40 €
        assert gen262_costo_fuel_annuo(8.0, 250.0, 200.0, 1.70) == pytest.approx(870.4)

    def test_quota_tasso_zero(self):
        assert gen262_quota_annua(45000.0, 15.0, 0.0) == pytest.approx(3000.0)

    def test_quota_annuity(self):
        # 45000 * 0,04 / (1 - 1,04^-15) ≈ 4047,33
        assert gen262_quota_annua(45000.0, 15.0, 4.0) == pytest.approx(4047.33, rel=1e-3)

    def test_quota_invalidi(self):
        with pytest.raises(ValueError):
            gen262_quota_annua(-100.0, 15.0, 4.0)
        with pytest.raises(ValueError):
            gen262_quota_annua(45000.0, 0.0, 4.0)
        with pytest.raises(ValueError):
            gen262_quota_annua(45000.0, 15.0, -1.0)


class TestGen262CostoGruppo:
    def test_breakdown(self):
        g = gen262_costo_annuo_gruppo(ore_blackout_anno=8.0, **P_G)
        assert set(g) == {"quota_annua", "om_annuo", "fuel_test_annuo",
                          "fuel_blackout_annuo", "fuel_totale", "costo_totale"}
        assert g["quota_annua"] == pytest.approx(4047.33, rel=1e-3)
        assert g["om_annuo"] == pytest.approx(1500.0)
        # test: 12*1 h * 64 l/h * 1,70 = 1305,60 €
        assert g["fuel_test_annuo"] == pytest.approx(1305.6)
        assert g["fuel_blackout_annuo"] == pytest.approx(870.4)
        assert g["fuel_totale"] == pytest.approx(2176.0)
        assert g["costo_totale"] == pytest.approx(
            g["quota_annua"] + g["om_annuo"] + g["fuel_totale"])

    def test_om_negativo_errore(self):
        with pytest.raises(ValueError):
            gen262_costo_annuo_gruppo(ore_blackout_anno=-2.0, **P_G)


class TestGen262Confronto:
    def test_conviene_gruppo(self):
        c = gen262_confronto(ore_blackout_anno=12.0, **P)
        assert c["verdetto"] == "gruppo"
        assert c["risparmio_annuo"] > 0
        assert c["costo_blackout_atteso"] == pytest.approx(12000.0)

    def test_conviene_blackout(self):
        c = gen262_confronto(ore_blackout_anno=0.0, **P)
        assert c["verdetto"] == "blackout"
        assert c["risparmio_annuo"] < 0
        assert c["risparmio_pct"] == pytest.approx(0.0)

    def test_indifferente(self):
        # 8 h: blackout 8000, gruppo ~7723 -> risparmio 277 < 5% di 8000
        c = gen262_confronto(ore_blackout_anno=8.0, **P)
        assert c["verdetto"] == "indifferente"
        assert abs(c["risparmio_annuo"]) <= 0.05 * c["costo_blackout_atteso"]


class TestGen262BreakEven:
    def test_forma_chiusa(self):
        be = gen262_break_even_ore(**P)
        quota = gen262_quota_annua(P["capex"], P["anni"], P["tasso_pct"])
        fixed = quota + P["om_annuo"] + 12.0 * P["ore_test_mese"] * 64.0 * P["prezzo_diesel_l"]
        atteso = fixed / (P["carico_kw"] * P["costo_kwh_non_fornito"] - 64.0 * P["prezzo_diesel_l"])
        assert be == pytest.approx(atteso)
        assert be == pytest.approx(7.69, rel=1e-2)

    def test_mai_conveniente(self):
        # VoLL 0,40: danno orario 80 €/h < fuel orario 108,80 €/h
        q = dict(P)
        q["costo_kwh_non_fornito"] = 0.40
        assert gen262_break_even_ore(**q) is None


class TestGen262Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = gen262_sensibilita_ore(20.0, 5.0, **P)
        assert len(righe) == 5
        assert righe[0]["ore"] == pytest.approx(0.0)
        assert righe[-1]["ore"] == pytest.approx(20.0)
        assert set(righe[0]) == {"ore", "costo_blackout", "costo_gruppo"}

    def test_monotonia_e_coerenza(self):
        righe = gen262_sensibilita_ore(20.0, 5.0, **P)
        bo = [r["costo_blackout"] for r in righe]
        gr = [r["costo_gruppo"] for r in righe]
        assert all(b > a for a, b in zip(bo, bo[1:]))
        assert all(b > a for a, b in zip(gr, gr[1:]))
        assert righe[2]["costo_blackout"] == pytest.approx(10.0 * 200.0 * 5.0)
        g0 = gen262_costo_annuo_gruppo(ore_blackout_anno=0.0, **P_G)
        assert righe[0]["costo_gruppo"] == pytest.approx(g0["costo_totale"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gen262_sensibilita_ore(0.0, 5.0, **P)
        with pytest.raises(ValueError):
            gen262_sensibilita_ore(20.0, 0.0, **P)
