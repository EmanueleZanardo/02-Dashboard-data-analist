"""Test tab283 'Carry petrolio: contango & stoccaggio fisico': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab283.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("po283_num", "po283_pos", "po283_spread", "po283_costo_carry",
          "po283_margine_carry", "po283_breakdown", "po283_be_tasso",
          "po283_sensibilita_tasso", "po283_pnl_ciclo_mln", "po283_verdetto")
po283_num = _F["po283_num"]
po283_pos = _F["po283_pos"]
po283_spread = _F["po283_spread"]
po283_costo_carry = _F["po283_costo_carry"]
po283_margine_carry = _F["po283_margine_carry"]
po283_breakdown = _F["po283_breakdown"]
po283_be_tasso = _F["po283_be_tasso"]
po283_sensibilita_tasso = _F["po283_sensibilita_tasso"]
po283_pnl_ciclo_mln = _F["po283_pnl_ciclo_mln"]
po283_verdetto = _F["po283_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE282 = "🧪 Margine petrolchimico: nafta \u2192 etilene"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"

M1, M2, SPOT = 75.0, 76.20, 75.0
MESI, TASSO = 1.0, 4.5
STOCC, ASSIC = 0.35, 0.05
SPREAD_ATTESO = M2 - M1
FIN_ATTESO = SPOT * (TASSO / 100.0) * (MESI / 12.0)
CARRY_ATTESO = FIN_ATTESO + (STOCC + ASSIC) * MESI
MARGINE_ATTESO = SPREAD_ATTESO - CARRY_ATTESO
BE_ATTESO = (SPREAD_ATTESO - (STOCC + ASSIC) * MESI) / (SPOT * (MESI / 12.0)) * 100.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab283:
    def test_tab283_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 358
        assert TITLE283 in titoli
        assert "tab283" in dvars
        assert "tab283" in withs
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[-1] == TITLE358
        keys = re.findall(r'key="(po283_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_281_282_283(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestPo283Validatori:
    def test_num_ok(self):
        assert po283_num(3, "x") == 3.0
        assert po283_num(2.5, "x") == 2.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            po283_num(True, "x")
        with pytest.raises(ValueError):
            po283_num("3", "x")
        with pytest.raises(ValueError):
            po283_num(float("nan"), "x")
        with pytest.raises(ValueError):
            po283_num(float("inf"), "x")

    def test_pos_ok(self):
        assert po283_pos(0, "x") == 0.0
        assert po283_pos(75, "x") == 75.0

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            po283_pos(-0.1, "x")


class TestPo283Spread:
    def test_contango(self):
        assert po283_spread(M1, M2) == pytest.approx(SPREAD_ATTESO)

    def test_backwardation(self):
        assert po283_spread(M2, M1) == pytest.approx(-SPREAD_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_spread(-1.0, M2)


class TestPo283CostoCarry:
    def test_base(self):
        assert po283_costo_carry(SPOT, TASSO, MESI, STOCC, ASSIC) == pytest.approx(CARRY_ATTESO)

    def test_scomposizione(self):
        assert po283_costo_carry(SPOT, TASSO, MESI, STOCC, ASSIC) == pytest.approx(
            FIN_ATTESO + STOCC * MESI + ASSIC * MESI)

    def test_lineare_mesi(self):
        assert po283_costo_carry(SPOT, TASSO, 2 * MESI, STOCC, ASSIC) == pytest.approx(
            2 * FIN_ATTESO + 2 * (STOCC + ASSIC) * MESI)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_costo_carry(SPOT, TASSO, 0.0, STOCC, ASSIC)
        with pytest.raises(ValueError):
            po283_costo_carry(-1.0, TASSO, MESI, STOCC, ASSIC)


class TestPo283Margine:
    def test_base(self):
        assert po283_margine_carry(SPREAD_ATTESO, CARRY_ATTESO) == pytest.approx(MARGINE_ATTESO)

    def test_formula(self):
        assert po283_margine_carry(1.2, 0.68) == pytest.approx(0.52)
        assert po283_margine_carry(-0.5, 0.68) == pytest.approx(-1.18)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_margine_carry(SPREAD_ATTESO, -0.1)


class TestPo283Breakdown:
    def test_somma(self):
        b = po283_breakdown(SPREAD_ATTESO, FIN_ATTESO, STOCC * MESI, ASSIC * MESI)
        assert b["spread_contango"] == pytest.approx(SPREAD_ATTESO)
        assert b["finanziamento"] == pytest.approx(-FIN_ATTESO)
        assert b["stoccaggio"] == pytest.approx(-STOCC * MESI)
        assert b["assicurazione"] == pytest.approx(-ASSIC * MESI)
        assert b["margine"] == pytest.approx(
            SPREAD_ATTESO - FIN_ATTESO - STOCC * MESI - ASSIC * MESI)
        assert b["margine"] == pytest.approx(MARGINE_ATTESO)


class TestPo283BeTasso:
    def test_base(self):
        assert po283_be_tasso(SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC) == pytest.approx(BE_ATTESO)

    def test_coerente_con_margine(self):
        be = po283_be_tasso(SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC)
        carry = po283_costo_carry(SPOT, be, MESI, STOCC, ASSIC)
        assert po283_margine_carry(SPREAD_ATTESO, carry) == pytest.approx(0.0, abs=1e-9)

    def test_backwardation_negativo(self):
        assert po283_be_tasso(SPOT, -1.0, MESI, STOCC, ASSIC) < 0.0

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_be_tasso(0.0, SPREAD_ATTESO, MESI, STOCC, ASSIC)
        with pytest.raises(ValueError):
            po283_be_tasso(SPOT, SPREAD_ATTESO, 0.0, STOCC, ASSIC)


class TestPo283Sensibilita:
    def test_struttura(self):
        righe = po283_sensibilita_tasso(TASSO, SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC, 5)
        assert len(righe) == 5
        assert righe[0]["tasso"] == pytest.approx(0.0)
        assert righe[-1]["tasso"] == pytest.approx(9.0)
        assert set(righe[0]) == {"tasso", "margine"}

    def test_decrescente_e_centro(self):
        righe = po283_sensibilita_tasso(TASSO, SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC, 5)
        margini = [r["margine"] for r in righe]
        assert all(b < a for a, b in zip(margini, margini[1:]))
        assert righe[2]["margine"] == pytest.approx(MARGINE_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_sensibilita_tasso(-1.0, SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC)
        with pytest.raises(ValueError):
            po283_sensibilita_tasso(TASSO, 0.0, SPREAD_ATTESO, MESI, STOCC, ASSIC)
        with pytest.raises(ValueError):
            po283_sensibilita_tasso(TASSO, SPOT, SPREAD_ATTESO, MESI, STOCC, ASSIC, 2)


class TestPo283Pnl:
    def test_base(self):
        assert po283_pnl_ciclo_mln(MARGINE_ATTESO, 500000) == pytest.approx(
            MARGINE_ATTESO * 500000 / 1e6)

    def test_zero(self):
        assert po283_pnl_ciclo_mln(MARGINE_ATTESO, 0.0) == pytest.approx(0.0)
        assert po283_pnl_ciclo_mln(0.0, 500000) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_pnl_ciclo_mln(MARGINE_ATTESO, -1.0)


class TestPo283Verdetto:
    def test_positivo(self):
        r = po283_verdetto(0.52, 0.10)
        assert r["verdetto"] == "positivo"
        assert r["margine"] == pytest.approx(0.52)

    def test_in_linea(self):
        assert po283_verdetto(0.05, 0.10)["verdetto"] == "in_linea"
        assert po283_verdetto(-0.10, 0.10)["verdetto"] == "in_linea"

    def test_negativo(self):
        r = po283_verdetto(-1.18, 0.10)
        assert r["verdetto"] == "negativo"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            po283_verdetto(1.0, -0.5)
