"""Test tab285 'Differenziali greggio: sweet vs sour': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab285.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("gd285_num", "gd285_pos", "gd285_frazioni",
          "gd285_costo_delivered", "gd285_valore_prodotti",
          "gd285_penalita_zolfo", "gd285_margine_netto",
          "gd285_margine_tonnellata", "gd285_breakeven_differenziale",
          "gd285_confronto", "gd285_sensibilita_differenziale",
          "gd285_verdetto")
gd285_num = _F["gd285_num"]
gd285_pos = _F["gd285_pos"]
gd285_frazioni = _F["gd285_frazioni"]
gd285_costo_delivered = _F["gd285_costo_delivered"]
gd285_valore_prodotti = _F["gd285_valore_prodotti"]
gd285_penalita_zolfo = _F["gd285_penalita_zolfo"]
gd285_margine_netto = _F["gd285_margine_netto"]
gd285_margine_tonnellata = _F["gd285_margine_tonnellata"]
gd285_breakeven_differenziale = _F["gd285_breakeven_differenziale"]
gd285_confronto = _F["gd285_confronto"]
gd285_sensibilita_differenziale = _F["gd285_sensibilita_differenziale"]
gd285_verdetto = _F["gd285_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE285 = "\U0001F6DB\uFE0F Differenziali greggio: sweet vs sour"
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
TITLE284 = "\U0001F3ED Unit commitment CCGT: accendere o no?"
TITLE283 = "\U0001F6E2\uFE0F Carry petrolio: contango & stoccaggio fisico"

BRENT, DIFF, NOLO, ASSIC = 82.0, -3.5, 2.2, 0.15
ZOLFO, PENZ, RAFF, MARGRIF = 1.8, 0.9, 4.5, 6.0
YIELDS = [0.22, 0.34, 0.12, 0.18]
PREZZI = [105.0, 98.0, 100.0, 62.0]
DELIV_ATTESO = BRENT + DIFF + NOLO + ASSIC
VALORE_ATTESO = (0.22 * 105.0 + 0.34 * 98.0 + 0.12 * 100.0 + 0.18 * 62.0
                 + 0.14 * 62.0)
PEN_ATTESA = ZOLFO * PENZ
MARG_ATTESO = VALORE_ATTESO - DELIV_ATTESO - RAFF - PEN_ATTESA
MARGT_ATTESO = MARG_ATTESO * 7.33
BE_ATTESO = VALORE_ATTESO - NOLO - ASSIC - RAFF - PEN_ATTESA - BRENT - MARGRIF


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab285:
    def test_tab285_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 327
        assert TITLE285 in titoli
        assert "tab285" in dvars
        assert "tab285" in withs
        assert titoli[dvars.index("tab285")] == TITLE285
        assert titoli[-1] == TITLE327
        keys = re.findall(r'key="(gd285_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_283_284_285(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestGd285Validatori:
    def test_num_ok(self):
        assert gd285_num(-3.5, "x") == -3.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            gd285_num(True, "x")
        with pytest.raises(ValueError):
            gd285_num(float("nan"), "x")

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            gd285_pos(-0.1, "x")

    def test_frazioni_ok(self):
        assert gd285_frazioni(YIELDS) == YIELDS

    def test_frazioni_somma_uno(self):
        assert gd285_frazioni([0.25, 0.25, 0.25, 0.25]) == [0.25] * 4

    def test_frazioni_ko(self):
        with pytest.raises(ValueError):
            gd285_frazioni([0.5, 0.5, 0.5, 0.5])
        with pytest.raises(ValueError):
            gd285_frazioni([0.5, 0.5, 0.5])
        with pytest.raises(ValueError):
            gd285_frazioni([-0.1, 0.5, 0.3, 0.3])
        with pytest.raises(ValueError):
            gd285_frazioni([1.1, 0.0, 0.0, 0.0])


class TestGd285Delivered:
    def test_base(self):
        assert gd285_costo_delivered(BRENT, DIFF, NOLO, ASSIC) == pytest.approx(
            DELIV_ATTESO)

    def test_formula(self):
        assert gd285_costo_delivered(80.0, -2.0, 1.5, 0.1) == pytest.approx(79.6)

    def test_premio_positivo(self):
        assert gd285_costo_delivered(80.0, 1.0, 1.5, 0.1) == pytest.approx(82.6)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_costo_delivered(-1.0, DIFF, NOLO, ASSIC)
        with pytest.raises(ValueError):
            gd285_costo_delivered(BRENT, DIFF, -0.5, ASSIC)


class TestGd285ValoreProdotti:
    def test_base(self):
        assert gd285_valore_prodotti(YIELDS, PREZZI) == pytest.approx(
            VALORE_ATTESO)

    def test_residuo_a_prezzo_fo(self):
        # rese nulle: tutto il bbl e' residuo valorizzato a prezzo fuel oil
        assert gd285_valore_prodotti([0, 0, 0, 0], PREZZI) == pytest.approx(62.0)

    def test_somma_uno_nessun_residuo(self):
        assert gd285_valore_prodotti([0.25] * 4, [100.0] * 4) == pytest.approx(
            100.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_valore_prodotti([0.5, 0.5], PREZZI)
        with pytest.raises(ValueError):
            gd285_valore_prodotti(YIELDS, [100.0, 100.0, 100.0])
        with pytest.raises(ValueError):
            gd285_valore_prodotti(YIELDS, [-1.0, 98.0, 100.0, 62.0])


class TestGd285Penalita:
    def test_base(self):
        assert gd285_penalita_zolfo(ZOLFO, PENZ) == pytest.approx(PEN_ATTESA)

    def test_zero(self):
        assert gd285_penalita_zolfo(0.0, PENZ) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_penalita_zolfo(-0.5, PENZ)


class TestGd285Margine:
    def test_base(self):
        assert gd285_margine_netto(VALORE_ATTESO, DELIV_ATTESO, RAFF,
                                   PEN_ATTESA) == pytest.approx(MARG_ATTESO)

    def test_formula(self):
        assert gd285_margine_netto(90.0, 80.0, 4.0, 1.0) == pytest.approx(5.0)

    def test_negativo_ammesso(self):
        assert gd285_margine_netto(70.0, 80.0, 4.0, 1.0) == pytest.approx(-15.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_margine_netto(-1.0, DELIV_ATTESO, RAFF, PEN_ATTESA)
        with pytest.raises(ValueError):
            gd285_margine_netto(VALORE_ATTESO, DELIV_ATTESO, -1.0, PEN_ATTESA)


class TestGd285Tonnellata:
    def test_base(self):
        assert gd285_margine_tonnellata(MARG_ATTESO) == pytest.approx(
            MARGT_ATTESO)

    def test_fattore_custom(self):
        assert gd285_margine_tonnellata(2.0, 7.0) == pytest.approx(14.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_margine_tonnellata(1.0, 0.0)


class TestGd285Breakeven:
    def test_base(self):
        assert gd285_breakeven_differenziale(VALORE_ATTESO, NOLO, ASSIC, RAFF,
                                             PEN_ATTESA, BRENT,
                                             MARGRIF) == pytest.approx(BE_ATTESO)

    def test_coerente_con_margine(self):
        be = gd285_breakeven_differenziale(VALORE_ATTESO, NOLO, ASSIC, RAFF,
                                           PEN_ATTESA, BRENT, MARGRIF)
        deliv = gd285_costo_delivered(BRENT, be, NOLO, ASSIC)
        assert gd285_margine_netto(VALORE_ATTESO, deliv, RAFF,
                                   PEN_ATTESA) == pytest.approx(MARGRIF)

    def test_piu_valore_meno_sconto_richiesto(self):
        be_alto = gd285_breakeven_differenziale(VALORE_ATTESO + 5.0, NOLO,
                                                ASSIC, RAFF, PEN_ATTESA, BRENT,
                                                MARGRIF)
        assert be_alto > BE_ATTESO

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_breakeven_differenziale(-1.0, NOLO, ASSIC, RAFF, PEN_ATTESA,
                                          BRENT, MARGRIF)


class TestGd285Confronto:
    def test_meglio(self):
        r = gd285_confronto(7.0, MARGRIF)
        assert r["esito"] == "meglio"
        assert r["delta"] == pytest.approx(1.0)

    def test_peggio(self):
        r = gd285_confronto(MARG_ATTESO, MARGRIF)
        assert r["esito"] == "peggio"
        assert r["delta"] == pytest.approx(MARG_ATTESO - MARGRIF)

    def test_pari(self):
        r = gd285_confronto(MARGRIF, MARGRIF)
        assert r["esito"] == "pari"
        assert r["delta"] == pytest.approx(0.0)


class TestGd285Sensibilita:
    def test_struttura(self):
        righe = gd285_sensibilita_differenziale(VALORE_ATTESO, BRENT, NOLO,
                                                ASSIC, RAFF, PEN_ATTESA, DIFF,
                                                5, 5.0)
        assert len(righe) == 5
        assert righe[0]["differenziale"] == pytest.approx(DIFF - 5.0)
        assert righe[-1]["differenziale"] == pytest.approx(DIFF + 5.0)
        assert set(righe[0]) == {"differenziale", "margine"}

    def test_decrescente_e_centro(self):
        righe = gd285_sensibilita_differenziale(VALORE_ATTESO, BRENT, NOLO,
                                                ASSIC, RAFF, PEN_ATTESA, DIFF,
                                                9, 5.0)
        marg = [r["margine"] for r in righe]
        assert all(b < a for a, b in zip(marg, marg[1:]))
        assert righe[4]["margine"] == pytest.approx(MARG_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_sensibilita_differenziale(VALORE_ATTESO, BRENT, NOLO, ASSIC,
                                            RAFF, PEN_ATTESA, DIFF, 2)
        with pytest.raises(ValueError):
            gd285_sensibilita_differenziale(VALORE_ATTESO, BRENT, NOLO, ASSIC,
                                            RAFF, PEN_ATTESA, DIFF, 9, 0.0)


class TestGd285Verdetto:
    def test_conveniente(self):
        r = gd285_verdetto(3.0, 2.0)
        assert r["verdetto"] == "conveniente"

    def test_marginale(self):
        assert gd285_verdetto(1.29, 2.0)["verdetto"] == "marginale"
        assert gd285_verdetto(0.0, 2.0)["verdetto"] == "marginale"

    def test_non_conveniente(self):
        assert gd285_verdetto(-0.5, 2.0)["verdetto"] == "non_conveniente"

    def test_soglia_zero(self):
        assert gd285_verdetto(0.0, 0.0)["verdetto"] == "conveniente"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            gd285_verdetto(1.0, -0.5)
