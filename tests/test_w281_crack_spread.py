"""Test tab281 'Crack spread: margine raffinazione 3-2-1': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab281.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cs281_num", "cs281_pos", "cs281_crack_321", "cs281_breakdown",
          "cs281_margine_tonne", "cs281_breakeven_crude",
          "cs281_sensibilita_crude", "cs281_ricavo_annuo_mln", "cs281_verdetto")
cs281_num = _F["cs281_num"]
cs281_pos = _F["cs281_pos"]
cs281_crack_321 = _F["cs281_crack_321"]
cs281_breakdown = _F["cs281_breakdown"]
cs281_margine_tonne = _F["cs281_margine_tonne"]
cs281_breakeven_crude = _F["cs281_breakeven_crude"]
cs281_sensibilita_crude = _F["cs281_sensibilita_crude"]
cs281_ricavo_annuo_mln = _F["cs281_ricavo_annuo_mln"]
cs281_verdetto = _F["cs281_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"

CRUDE, GAS, DIESEL = 80.0, 115.0, 125.0
CRACK_ATTESO = (2 * GAS + DIESEL) / 3 - CRUDE
BE_ATTESO = (2 * GAS + DIESEL) / 3


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab281:
    def test_tab281_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 327
        assert TITLE281 in titoli
        assert "tab281" in dvars
        assert "tab281" in withs
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[-1] == TITLE327
        keys = re.findall(r'key="(cs281_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_279_280_281(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestCs281Validatori:
    def test_num_ok(self):
        assert cs281_num(3, "x") == 3.0
        assert cs281_num(2.5, "x") == 2.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            cs281_num(True, "x")
        with pytest.raises(ValueError):
            cs281_num("3", "x")
        with pytest.raises(ValueError):
            cs281_num(float("nan"), "x")
        with pytest.raises(ValueError):
            cs281_num(float("inf"), "x")

    def test_pos_ok(self):
        assert cs281_pos(0, "x") == 0.0
        assert cs281_pos(200000, "x") == 200000.0

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            cs281_pos(-0.1, "x")


class TestCs281Crack321:
    def test_base(self):
        assert cs281_crack_321(CRUDE, GAS, DIESEL) == pytest.approx(CRACK_ATTESO)

    def test_simmetria_pesi(self):
        # +10 $/bbl sulla benzina alza il crack di 2/3*10, sul gasolio di 1/3*10
        base = cs281_crack_321(CRUDE, GAS, DIESEL)
        assert cs281_crack_321(CRUDE, GAS + 10, DIESEL) == pytest.approx(base + 20 / 3)
        assert cs281_crack_321(CRUDE, GAS, DIESEL + 10) == pytest.approx(base + 10 / 3)

    def test_negativo(self):
        assert cs281_crack_321(200.0, GAS, DIESEL) < 0

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_crack_321(True, GAS, DIESEL)
        with pytest.raises(ValueError):
            cs281_crack_321(CRUDE, float("nan"), DIESEL)


class TestCs281Breakdown:
    def test_somma(self):
        b = cs281_breakdown(CRUDE, GAS, DIESEL)
        assert b["greggio"] == pytest.approx(-CRUDE)
        assert b["benzina"] == pytest.approx(2 * GAS / 3)
        assert b["gasolio"] == pytest.approx(DIESEL / 3)
        assert b["margine"] == pytest.approx(CRACK_ATTESO)
        assert b["margine"] == pytest.approx(b["greggio"] + b["benzina"] + b["gasolio"])


class TestCs281MargineTonne:
    def test_base(self):
        assert cs281_margine_tonne(CRACK_ATTESO, 7.33) == pytest.approx(CRACK_ATTESO * 7.33)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_margine_tonne(CRACK_ATTESO, 0.0)
        with pytest.raises(ValueError):
            cs281_margine_tonne(CRACK_ATTESO, -1.0)


class TestCs281Breakeven:
    def test_base(self):
        assert cs281_breakeven_crude(GAS, DIESEL) == pytest.approx(BE_ATTESO)

    def test_coerente_con_crack(self):
        be = cs281_breakeven_crude(GAS, DIESEL)
        assert cs281_crack_321(be, GAS, DIESEL) == pytest.approx(0.0, abs=1e-9)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_breakeven_crude(0.0, DIESEL)
        with pytest.raises(ValueError):
            cs281_breakeven_crude(GAS, -1.0)


class TestCs281Sensibilita:
    def test_struttura(self):
        righe = cs281_sensibilita_crude(CRUDE, GAS, DIESEL, 5)
        assert len(righe) == 5
        assert righe[0]["crude"] == pytest.approx(40.0)
        assert righe[-1]["crude"] == pytest.approx(120.0)
        assert set(righe[0]) == {"crude", "crack"}

    def test_decrescente_e_centro(self):
        righe = cs281_sensibilita_crude(CRUDE, GAS, DIESEL, 5)
        cracks = [r["crack"] for r in righe]
        assert all(b < a for a, b in zip(cracks, cracks[1:]))
        assert righe[2]["crack"] == pytest.approx(CRACK_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_sensibilita_crude(0.0, GAS, DIESEL)
        with pytest.raises(ValueError):
            cs281_sensibilita_crude(CRUDE, GAS, DIESEL, 2)


class TestCs281RicavoAnnuo:
    def test_base(self):
        atteso = CRACK_ATTESO * 200000 * 0.90 * 365 / 1e6
        assert cs281_ricavo_annuo_mln(CRACK_ATTESO, 200000, 90.0) == pytest.approx(atteso)

    def test_zero(self):
        assert cs281_ricavo_annuo_mln(CRACK_ATTESO, 200000, 0.0) == pytest.approx(0.0)
        assert cs281_ricavo_annuo_mln(0.0, 200000, 90.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_ricavo_annuo_mln(CRACK_ATTESO, -1.0, 90.0)
        with pytest.raises(ValueError):
            cs281_ricavo_annuo_mln(CRACK_ATTESO, 200000, 100.1)


class TestCs281Verdetto:
    def test_positivo(self):
        r = cs281_verdetto(43.33, 1.0)
        assert r["verdetto"] == "positivo"
        assert r["crack"] == pytest.approx(43.33)

    def test_in_linea(self):
        assert cs281_verdetto(0.5, 1.0)["verdetto"] == "in_linea"
        assert cs281_verdetto(-1.0, 1.0)["verdetto"] == "in_linea"

    def test_negativo(self):
        r = cs281_verdetto(-5.0, 1.0)
        assert r["verdetto"] == "negativo"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cs281_verdetto(1.0, -0.5)
