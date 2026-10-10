"""Test tab294 '🧪📉 Backtest del VaR: il modello tiene?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab294.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("bv294_num", "bv294_pos", "bv294_conf", "bv294_parse_pl",
          "bv294_violazioni", "bv294_lrt_pof", "bv294_chi2_sf1",
          "bv294_chi2_inv_sf1", "bv294_pvalue", "bv294_verdetto")
bv294_num = _F["bv294_num"]
bv294_pos = _F["bv294_pos"]
bv294_conf = _F["bv294_conf"]
bv294_parse_pl = _F["bv294_parse_pl"]
bv294_violazioni = _F["bv294_violazioni"]
bv294_lrt_pof = _F["bv294_lrt_pof"]
bv294_chi2_sf1 = _F["bv294_chi2_sf1"]
bv294_chi2_inv_sf1 = _F["bv294_chi2_inv_sf1"]
bv294_pvalue = _F["bv294_pvalue"]
bv294_verdetto = _F["bv294_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"

DEMO = [320, -150, 480, -600, 210, -90, 540, -2600, 130, -320,
        410, -180, 95, -730, 260, -410, 380, -120, 510, -3100,
        -240, 170, -520, 290, -140, 660, -2800, 120, -390, 440,
        -210, 180, -640, 350, -260, 720, -4100, 90, -330, 260,
        -180, 470, -290, 130, -540, 390, -2700, 220, -160, 510,
        -350, 140, -230, 690, -2600, 110, -420, 380, -190, -3300]
DEMO_TXT = "\n".join(str(v) for v in DEMO)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab294:
    def test_tab294_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 358
        assert TITLE294 in titoli
        assert "tab294" in dvars
        assert "tab294" in withs
        assert titoli[dvars.index("tab294")] == TITLE294
        assert titoli[-1] == TITLE358
        keys = re.findall(r'key="(bv294_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_292_293_294(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab292")] == TITLE292
        assert titoli[dvars.index("tab293")] == TITLE293
        assert titoli[dvars.index("tab294")] == TITLE294


class TestBv294Validatori:
    def test_num_ok(self):
        assert bv294_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            bv294_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            bv294_num(float("nan"), "x")

    def test_pos_zero_ko(self):
        with pytest.raises(ValueError):
            bv294_pos(0.0, "x")

    def test_conf_ok(self):
        assert bv294_conf(0.95) == 0.95

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            bv294_conf(1.0)
        with pytest.raises(ValueError):
            bv294_conf(0.0)


class TestBv294Parse:
    def test_ok_virgole_commenti(self):
        vals = bv294_parse_pl("# cmt\n\n1,5\n" + "\n".join(["2"] * 19))
        assert len(vals) == 20
        assert vals[0] == pytest.approx(1.5)

    def test_esattamente_20_ok(self):
        assert len(bv294_parse_pl("\n".join(["1"] * 20))) == 20

    def test_troppo_pochi_ko(self):
        with pytest.raises(ValueError):
            bv294_parse_pl("\n".join(["1"] * 19))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            bv294_parse_pl("\n".join(["1"] * 19 + ["abc"]))


class TestBv294Violazioni:
    def test_conteggio(self):
        r = bv294_violazioni([100, -2500, 50, -2600, 300], 2000.0, 0.95)
        assert r == {"n": 5, "violazioni": 2, "tasso": pytest.approx(0.4),
                     "atteso": pytest.approx(0.05)}

    def test_var_ko(self):
        with pytest.raises(ValueError):
            bv294_violazioni([1.0, 2.0], 0.0, 0.95)


class TestBv294Kupiec:
    def test_lr_zero_se_tasso_esatto(self):
        assert bv294_lrt_pof(100, 5, 0.95) == pytest.approx(0.0, abs=1e-9)

    def test_lr_valore_noto(self):
        # n=100, x=20, conf=0.95: LR = 27.955733336530134
        assert bv294_lrt_pof(100, 20, 0.95) == \
            pytest.approx(27.955733336530134, rel=1e-9)

    def test_lr_cresce_con_violazioni(self):
        assert bv294_lrt_pof(100, 10, 0.95) > bv294_lrt_pof(100, 5, 0.95)

    def test_lr_x_fuori_range_ko(self):
        with pytest.raises(ValueError):
            bv294_lrt_pof(100, 101, 0.95)

    def test_sf_bordo_zero(self):
        assert bv294_chi2_sf1(0.0) == 1.0
        assert bv294_chi2_sf1(-3.0) == 1.0

    def test_sf_valori_noti(self):
        assert bv294_chi2_sf1(3.841458820694124) == pytest.approx(0.05)
        assert bv294_chi2_sf1(6.634896601724987) == \
            pytest.approx(0.01, rel=1e-6)

    def test_inv_sf_valori_noti(self):
        assert bv294_chi2_inv_sf1(0.05) == \
            pytest.approx(3.841458820694124, rel=1e-6)
        assert bv294_chi2_inv_sf1(0.01) == \
            pytest.approx(6.634896601724987, rel=1e-6)

    def test_inv_sf_bordi_ko(self):
        with pytest.raises(ValueError):
            bv294_chi2_inv_sf1(0.0)

    def test_pvalue_uno_se_tasso_esatto(self):
        assert bv294_pvalue(100, 5, 0.95) == pytest.approx(1.0)

    def test_pvalue_demo(self):
        # 60 oss., 7 violazioni, VaR 2000, conf 95%: p = 0.04164242994937847
        assert bv294_pvalue(60, 7, 0.95) == \
            pytest.approx(0.04164242994937847, rel=1e-9)


class TestBv294Verdetto:
    def test_accettato(self):
        assert bv294_verdetto(0.5)["verdetto"] == "modello accettato"

    def test_accettato_bordo(self):
        assert bv294_verdetto(0.05)["verdetto"] == "modello accettato"

    def test_zona_gialla(self):
        assert bv294_verdetto(0.03)["verdetto"] == \
            "zona gialla: rivedere il modello"

    def test_zona_gialla_bordo(self):
        assert bv294_verdetto(0.01)["verdetto"] == \
            "zona gialla: rivedere il modello"

    def test_respinto(self):
        assert bv294_verdetto(0.005)["verdetto"] == "modello respinto"

    def test_pvalue_fuori_range_ko(self):
        with pytest.raises(ValueError):
            bv294_verdetto(1.5)


class TestBv294Integrazione:
    def test_catena_demo_zona_gialla(self):
        pl = bv294_parse_pl(DEMO_TXT)
        assert len(pl) == 60
        r = bv294_violazioni(pl, 2000.0, 0.95)
        assert r["violazioni"] == 7
        assert r["tasso"] == pytest.approx(7 / 60)
        pv = bv294_pvalue(r["n"], r["violazioni"], 0.95)
        assert pv == pytest.approx(0.04164242994937847, rel=1e-9)
        assert bv294_verdetto(pv)["verdetto"] == \
            "zona gialla: rivedere il modello"
