"""Test tab287 '🚢⚡ Rigassificazione GNL: margine terminale': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab287.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("rg287_num", "rg287_pos", "rg287_costo_rigass",
          "rg287_costo_sendout", "rg287_margine_mwh", "rg287_pnl_ciclo",
          "rg287_be_des", "rg287_be_hub", "rg287_utilizzo",
          "rg287_breakdown", "rg287_sensibilita_hub", "rg287_verdetto")
rg287_num = _F["rg287_num"]
rg287_pos = _F["rg287_pos"]
rg287_costo_rigass = _F["rg287_costo_rigass"]
rg287_costo_sendout = _F["rg287_costo_sendout"]
rg287_margine_mwh = _F["rg287_margine_mwh"]
rg287_pnl_ciclo = _F["rg287_pnl_ciclo"]
rg287_be_des = _F["rg287_be_des"]
rg287_be_hub = _F["rg287_be_hub"]
rg287_utilizzo = _F["rg287_utilizzo"]
rg287_breakdown = _F["rg287_breakdown"]
rg287_sensibilita_hub = _F["rg287_sensibilita_hub"]
rg287_verdetto = _F["rg287_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE285 = "\U0001F6DB\uFE0F Differenziali greggio: sweet vs sour"
TITLE284 = "\U0001F3ED Unit commitment CCGT: accendere o no?"

DES, HUB, TAR_CAP, TAR_COMM, PERD, EXTRA = 30.0, 38.0, 0.45, 0.25, 1.2, 0.20
RIG_ATT = TAR_CAP + TAR_COMM + HUB * PERD / 100.0                 # 1.156
SEND_ATT = DES + RIG_ATT + EXTRA                                 # 31.356
VOL, FISSI, SOGLIA = 900000.0, 250000.0, 0.50
MARG_ATT = HUB - SEND_ATT - FISSI / VOL                          # ~6.3662
PNL_ATT = (HUB - SEND_ATT) * VOL - FISSI                         # ~5729600
BE_DES_ATT = HUB - RIG_ATT - EXTRA - FISSI / VOL                 # ~36.3662
BE_HUB_ATT = (DES + TAR_CAP + TAR_COMM + EXTRA + FISSI / VOL) / 0.988


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab287:
    def test_tab287_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 373
        assert TITLE287 in titoli
        assert "tab287" in dvars
        assert "tab287" in withs
        assert titoli[dvars.index("tab287")] == TITLE287
        assert titoli[-1] == TITLE373
        keys = re.findall(r'key="(rg287_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_285_286_287(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab285")] == TITLE285
        assert titoli[dvars.index("tab286")] == TITLE286
        assert titoli[dvars.index("tab287")] == TITLE287


class TestRg287Validatori:
    def test_num_ok(self):
        assert rg287_num(1.5, "x") == 1.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            rg287_num(True, "x")
        with pytest.raises(ValueError):
            rg287_num(float("nan"), "x")

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            rg287_pos(-0.1, "x")

    def test_pos_zero_ok(self):
        assert rg287_pos(0.0, "x") == 0.0


class TestRg287CostoRigass:
    def test_base(self):
        assert rg287_costo_rigass(TAR_CAP, TAR_COMM, PERD, HUB) == \
            pytest.approx(RIG_ATT)

    def test_zero_perdite(self):
        assert rg287_costo_rigass(0.5, 0.2, 0.0, 40.0) == pytest.approx(0.7)

    def test_perdite_scalano_con_hub(self):
        c1 = rg287_costo_rigass(0.0, 0.0, 1.0, 40.0)
        c2 = rg287_costo_rigass(0.0, 0.0, 1.0, 80.0)
        assert c2 == pytest.approx(2.0 * c1)


class TestRg287SendoutMargine:
    def test_sendout(self):
        assert rg287_costo_sendout(DES, RIG_ATT, EXTRA) == \
            pytest.approx(SEND_ATT)

    def test_margine(self):
        assert rg287_margine_mwh(HUB, SEND_ATT, FISSI, VOL) == \
            pytest.approx(MARG_ATT)

    def test_margine_volume_zero_ko(self):
        with pytest.raises(ValueError):
            rg287_margine_mwh(HUB, SEND_ATT, FISSI, 0.0)

    def test_margine_pesante_con_fissi(self):
        # con fissi enormi il margine diventa negativo
        assert rg287_margine_mwh(HUB, SEND_ATT, 1e9, VOL) < 0

    def test_pnl(self):
        assert rg287_pnl_ciclo(HUB, SEND_ATT, VOL, FISSI) == \
            pytest.approx(PNL_ATT, rel=1e-9)

    def test_pnl_coerente_margine(self):
        m = rg287_margine_mwh(HUB, SEND_ATT, FISSI, VOL)
        p = rg287_pnl_ciclo(HUB, SEND_ATT, VOL, FISSI)
        assert p == pytest.approx(m * VOL)


class TestRg287BreakEven:
    def test_be_des(self):
        assert rg287_be_des(HUB, RIG_ATT, EXTRA, FISSI, VOL) == \
            pytest.approx(BE_DES_ATT)

    def test_be_des_azzera_margine(self):
        bd = rg287_be_des(HUB, RIG_ATT, EXTRA, FISSI, VOL)
        send = rg287_costo_sendout(bd, RIG_ATT, EXTRA)
        assert rg287_margine_mwh(HUB, send, FISSI, VOL) == pytest.approx(0.0)

    def test_be_hub(self):
        assert rg287_be_hub(DES, TAR_CAP, TAR_COMM, PERD, EXTRA,
                            FISSI, VOL) == pytest.approx(BE_HUB_ATT)

    def test_be_hub_azzera_margine(self):
        bh = rg287_be_hub(DES, TAR_CAP, TAR_COMM, PERD, EXTRA,
                          FISSI, VOL)
        rig = rg287_costo_rigass(TAR_CAP, TAR_COMM, PERD, bh)
        send = rg287_costo_sendout(DES, rig, EXTRA)
        assert rg287_margine_mwh(bh, send, FISSI, VOL) == pytest.approx(0.0)


class TestRg287Utilizzo:
    def test_pieno(self):
        assert rg287_utilizzo(900000.0, 900000.0) == pytest.approx(1.0)

    def test_meta(self):
        assert rg287_utilizzo(450000.0, 900000.0) == pytest.approx(0.5)

    def test_capacita_zero_ko(self):
        with pytest.raises(ValueError):
            rg287_utilizzo(100.0, 0.0)


class TestRg287BreakdownSensibilita:
    def test_breakdown_chiavi(self):
        b = rg287_breakdown(DES, TAR_CAP, TAR_COMM, HUB * PERD / 100.0, EXTRA,
                            RIG_ATT, SEND_ATT, MARG_ATT)
        assert set(b) == {"des", "tariffa_capacita", "tariffa_commodity",
                          "perdite", "oneri_extra", "costo_rigassificazione",
                          "costo_sendout", "margine_mwh"}
        assert b["des"] == pytest.approx(DES)
        assert b["margine_mwh"] == pytest.approx(MARG_ATT)

    def test_sensibilita_shape(self):
        r = rg287_sensibilita_hub(HUB, DES, TAR_CAP, TAR_COMM, PERD, EXTRA,
                                  FISSI, VOL)
        assert len(r) == 9
        assert r[0]["hub"] < HUB < r[-1]["hub"]
        marg = [x["margine"] for x in r]
        assert marg == sorted(marg)

    def test_sensibilita_trascurabile(self):
        r = rg287_sensibilita_hub(0.0, DES, TAR_CAP, TAR_COMM, PERD, EXTRA,
                                  FISSI, VOL)
        assert all(x["hub"] == 0.0 for x in r)
        assert all(x["margine"] < 0 for x in r)

    def test_sensibilita_n_punti_ko(self):
        with pytest.raises(ValueError):
            rg287_sensibilita_hub(HUB, DES, TAR_CAP, TAR_COMM, PERD, EXTRA,
                                  FISSI, VOL, n_punti=2)


class TestRg287Verdetto:
    def test_positivo(self):
        assert rg287_verdetto(1.2, 0.5)["verdetto"] == "positivo"

    def test_in_linea(self):
        assert rg287_verdetto(0.2, 0.5)["verdetto"] == "in_linea"

    def test_negativo(self):
        assert rg287_verdetto(-0.1, 0.5)["verdetto"] == "negativo"

    def test_soglia_negativa_ko(self):
        with pytest.raises(ValueError):
            rg287_verdetto(0.2, -0.5)


class TestRg287BeHubEdge:
    def test_perdite_100_ko(self):
        import pytest
        with pytest.raises(ValueError):
            rg287_be_hub(DES, TAR_CAP, TAR_COMM, 100.0, EXTRA, FISSI, VOL)

    def test_perdite_zero(self):
        assert rg287_be_hub(DES, TAR_CAP, TAR_COMM, 0.0, EXTRA, FISSI,
                            VOL) == pytest.approx(DES + TAR_CAP + TAR_COMM +
                                                  EXTRA + FISSI / VOL)
