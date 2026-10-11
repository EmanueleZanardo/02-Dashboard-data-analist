"""Test tab288 '⚡🔥 Clean spark spread: margine centrale a gas': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab288.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("css288_num", "css288_pos", "css288_frac", "css288_spark",
          "css288_emissioni", "css288_costo_co2", "css288_clean_spark",
          "css288_margine_ora", "css288_fissi_unitari", "css288_pnl",
          "css288_be_power", "css288_breakdown", "css288_sensibilita_power",
          "css288_verdetto")
css288_num = _F["css288_num"]
css288_pos = _F["css288_pos"]
css288_frac = _F["css288_frac"]
css288_spark = _F["css288_spark"]
css288_emissioni = _F["css288_emissioni"]
css288_costo_co2 = _F["css288_costo_co2"]
css288_clean_spark = _F["css288_clean_spark"]
css288_margine_ora = _F["css288_margine_ora"]
css288_fissi_unitari = _F["css288_fissi_unitari"]
css288_pnl = _F["css288_pnl"]
css288_be_power = _F["css288_be_power"]
css288_breakdown = _F["css288_breakdown"]
css288_sensibilita_power = _F["css288_sensibilita_power"]
css288_verdetto = _F["css288_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE285 = "\U0001F6DB\uFE0F Differenziali greggio: sweet vs sour"

POWER, GAS, EFF, CO2P, CO2F = 110.0, 38.0, 0.58, 85.0, 0.201
ORE, CAP, FISSI, SOGLIA = 6000.0, 450.0, 12000000.0, 5.0

SPARK_ATT = POWER - GAS / EFF
EMIS_ATT = CO2F / EFF
CO2C_ATT = CO2P * EMIS_ATT
CLEAN_ATT = SPARK_ATT - CO2C_ATT
FU_ATT = FISSI / (ORE * CAP)
MARG_ATT = CLEAN_ATT - FU_ATT
PNL_ATT = CLEAN_ATT * ORE * CAP - FISSI
BE_ATT = GAS / EFF + CO2P * CO2F / EFF + FU_ATT


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab288:
    def test_tab288_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert TITLE288 in titoli
        assert "tab288" in dvars
        assert "tab288" in withs
        assert titoli[dvars.index("tab288")] == TITLE288
        assert titoli[-1] == TITLE372
        keys = re.findall(r'key="(css288_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_286_287_288(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab286")] == TITLE286
        assert titoli[dvars.index("tab287")] == TITLE287
        assert titoli[dvars.index("tab288")] == TITLE288


class TestCss288Validatori:
    def test_num_ok(self):
        assert css288_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            css288_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            css288_num(float("nan"), "x")

    def test_pos_negativo_ko(self):
        with pytest.raises(ValueError):
            css288_pos(-0.1, "x")

    def test_frac_ok(self):
        assert css288_frac(0.58, "e") == pytest.approx(0.58)

    def test_frac_zero_ko(self):
        with pytest.raises(ValueError):
            css288_frac(0.0, "e")

    def test_frac_sopra_uno_ko(self):
        with pytest.raises(ValueError):
            css288_frac(1.2, "e")


class TestCss288Spark:
    def test_spark(self):
        assert css288_spark(POWER, GAS, EFF) == pytest.approx(SPARK_ATT)

    def test_spark_gas_gratis(self):
        assert css288_spark(80.0, 0.0, 0.5) == pytest.approx(80.0)

    def test_emissioni(self):
        assert css288_emissioni(CO2F, EFF) == pytest.approx(EMIS_ATT)

    def test_costo_co2(self):
        assert css288_costo_co2(CO2P, EMIS_ATT) == pytest.approx(CO2C_ATT)

    def test_clean_spark(self):
        assert css288_clean_spark(POWER, GAS, EFF, CO2P,
                                  CO2F) == pytest.approx(CLEAN_ATT)

    def test_clean_spark_coerenza(self):
        assert css288_clean_spark(POWER, GAS, EFF, CO2P, CO2F) == pytest.approx(
            css288_spark(POWER, GAS, EFF) -
            css288_costo_co2(CO2P, css288_emissioni(CO2F, EFF)))


class TestCss288MarginePnl:
    def test_fissi_unitari(self):
        assert css288_fissi_unitari(FISSI, ORE, CAP) == pytest.approx(FU_ATT)

    def test_fissi_unitari_ore_zero_ko(self):
        with pytest.raises(ValueError):
            css288_fissi_unitari(FISSI, 0.0, CAP)

    def test_margine_ora(self):
        assert css288_margine_ora(CLEAN_ATT, FU_ATT) == pytest.approx(MARG_ATT)

    def test_pnl(self):
        assert css288_pnl(CLEAN_ATT, ORE, CAP,
                         FISSI) == pytest.approx(PNL_ATT)

    def test_be_power(self):
        assert css288_be_power(GAS, EFF, CO2P, CO2F,
                               FU_ATT) == pytest.approx(BE_ATT)

    def test_be_power_annulla_margine(self):
        assert css288_margine_ora(
            css288_clean_spark(BE_ATT, GAS, EFF, CO2P, CO2F),
            FU_ATT) == pytest.approx(0.0)


class TestCss288Breakdown:
    def test_chiavi_e_somma(self):
        b = css288_breakdown(POWER, GAS / EFF, CO2C_ATT, FU_ATT, MARG_ATT)
        assert set(b) == {"prezzo_power", "costo_gas", "costo_co2",
                          "quota_fissa", "margine_ora"}
        assert b["prezzo_power"] - b["costo_gas"] - b["costo_co2"] - \
            b["quota_fissa"] == pytest.approx(b["margine_ora"])

    def test_breakdown_costo_negativo_ko(self):
        with pytest.raises(ValueError):
            css288_breakdown(POWER, -1.0, CO2C_ATT, FU_ATT, MARG_ATT)


class TestCss288Sensibilita:
    def test_struttura(self):
        righe = css288_sensibilita_power(POWER, GAS, EFF, CO2P, CO2F, FU_ATT)
        assert len(righe) == 9
        assert righe[4]["power"] == pytest.approx(POWER)
        assert righe[4]["margine"] == pytest.approx(MARG_ATT)
        assert righe[0]["power"] == pytest.approx(POWER * 0.85)
        assert righe[-1]["power"] == pytest.approx(POWER * 1.15)
        for r in righe:
            assert r["margine"] == pytest.approx(r["clean_spark"] - FU_ATT)

    def test_n_punti_ko(self):
        with pytest.raises(ValueError):
            css288_sensibilita_power(POWER, GAS, EFF, CO2P, CO2F, FU_ATT,
                                     n_punti=2)

    def test_ampiezza_ko(self):
        with pytest.raises(ValueError):
            css288_sensibilita_power(POWER, GAS, EFF, CO2P, CO2F, FU_ATT,
                                     ampiezza=0.0)


class TestCss288Verdetto:
    def test_profittevole(self):
        assert css288_verdetto(8.0, SOGLIA)["verdetto"] == "profittevole"

    def test_copre_i_costi(self):
        assert css288_verdetto(2.0, SOGLIA)["verdetto"] == "copre_i_costi"

    def test_in_perdita(self):
        assert css288_verdetto(-0.5, SOGLIA)["verdetto"] == "in_perdita"

    def test_soglia_negativa_ko(self):
        with pytest.raises(ValueError):
            css288_verdetto(2.0, -1.0)
