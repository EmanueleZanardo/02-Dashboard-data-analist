"""Test tab290 '🔀💰 PTR transfrontaliero: vale il prezzo d'asta?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab290.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ptr290_num", "ptr290_pos", "ptr290_norm_cdf", "ptr290_norm_pdf",
          "ptr290_bachelier_call", "ptr290_valore_ptr", "ptr290_valore_ftr",
          "ptr290_premio", "ptr290_be_asta", "ptr290_pnl",
          "ptr290_sensibilita_vol", "ptr290_breakdown", "ptr290_verdetto")
ptr290_num = _F["ptr290_num"]
ptr290_pos = _F["ptr290_pos"]
ptr290_norm_cdf = _F["ptr290_norm_cdf"]
ptr290_norm_pdf = _F["ptr290_norm_pdf"]
ptr290_bachelier_call = _F["ptr290_bachelier_call"]
ptr290_valore_ptr = _F["ptr290_valore_ptr"]
ptr290_valore_ftr = _F["ptr290_valore_ftr"]
ptr290_premio = _F["ptr290_premio"]
ptr290_be_asta = _F["ptr290_be_asta"]
ptr290_pnl = _F["ptr290_pnl"]
ptr290_sensibilita_vol = _F["ptr290_sensibilita_vol"]
ptr290_breakdown = _F["ptr290_breakdown"]
ptr290_verdetto = _F["ptr290_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"

SPREAD, SIGMA, T = 4.0, 12.0, 1.0
ASTA, MW, ORE, SOGLIA = 3.0, 100.0, 8760.0, 0.50

# Bachelier ATM: C = sigma*sqrt(T)/sqrt(2*pi)
BACH_ATM_ATT = SIGMA / math.sqrt(2.0 * math.pi)
VAL_PTR_ATT = ptr290_bachelier_call(SPREAD, 0.0, SIGMA, T)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab290:
    def test_tab290_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 352
        assert TITLE290 in titoli
        assert "tab290" in dvars
        assert "tab290" in withs
        assert titoli[dvars.index("tab290")] == TITLE290
        assert titoli[-1] == TITLE352
        keys = re.findall(r'key="(ptr290_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_288_289_290(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab288")] == TITLE288
        assert titoli[dvars.index("tab289")] == TITLE289
        assert titoli[dvars.index("tab290")] == TITLE290


class TestPtr290Validatori:
    def test_num_ok(self):
        assert ptr290_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            ptr290_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            ptr290_num(float("nan"), "x")

    def test_pos_negativo_ko(self):
        with pytest.raises(ValueError):
            ptr290_pos(-0.1, "x")

    def test_norm_cdf_pdf(self):
        assert ptr290_norm_cdf(0.0) == pytest.approx(0.5)
        assert ptr290_norm_pdf(0.0) == pytest.approx(1.0 / math.sqrt(2.0 * math.pi))


class TestPtr290Bachelier:
    def test_atm_noto(self):
        assert ptr290_bachelier_call(0.0, 0.0, SIGMA, T) == pytest.approx(
            BACH_ATM_ATT)

    def test_deep_itm(self):
        assert ptr290_bachelier_call(100.0, 0.0, SIGMA, T) == pytest.approx(
            100.0, rel=1e-6)

    def test_sigma_zero_intrinseco(self):
        assert ptr290_bachelier_call(5.0, 10.0, 0.0, T) == pytest.approx(0.0)
        assert ptr290_bachelier_call(12.0, 10.0, 0.0, T) == pytest.approx(2.0)

    def test_sigma_negativa_ko(self):
        with pytest.raises(ValueError):
            ptr290_bachelier_call(SPREAD, 0.0, -1.0, T)

    def test_tempo_zero_ko(self):
        with pytest.raises(ValueError):
            ptr290_bachelier_call(SPREAD, 0.0, SIGMA, 0.0)


class TestPtr290Valore:
    def test_valore_ptr_e_call_strike_zero(self):
        assert ptr290_valore_ptr(SPREAD, SIGMA, T) == pytest.approx(
            ptr290_bachelier_call(SPREAD, 0.0, SIGMA, T))

    def test_valore_ptr_maggiore_spread(self):
        # opzione >= intrinseco
        assert ptr290_valore_ptr(SPREAD, SIGMA, T) >= max(SPREAD, 0.0)

    def test_valore_ptr_spread_negativo(self):
        v = ptr290_valore_ptr(-8.0, SIGMA, T)
        assert v > 0.0
        assert v < SIGMA  # solo valore temporale, limitato

    def test_valore_ftr(self):
        assert ptr290_valore_ftr(-2.5) == pytest.approx(-2.5)
        assert ptr290_valore_ftr(SPREAD) == pytest.approx(SPREAD)


class TestPtr290PremioPnl:
    def test_premio(self):
        assert ptr290_premio(7.0, ASTA) == pytest.approx(4.0)

    def test_be_asta(self):
        assert ptr290_be_asta(7.0) == pytest.approx(7.0)

    def test_be_asta_annulla_premio(self):
        assert ptr290_premio(7.0, ptr290_be_asta(7.0)) == pytest.approx(0.0)

    def test_pnl(self):
        assert ptr290_pnl(4.0, MW, ORE) == pytest.approx(4.0 * MW * ORE)

    def test_pnl_mw_negativi_ko(self):
        with pytest.raises(ValueError):
            ptr290_pnl(4.0, -1.0, ORE)


class TestPtr290Sensibilita:
    def test_struttura(self):
        righe = ptr290_sensibilita_vol(SPREAD, SIGMA, T, ASTA)
        assert len(righe) == 9
        assert righe[4]["sigma"] == pytest.approx(SIGMA)
        assert righe[4]["valore_ptr"] == pytest.approx(VAL_PTR_ATT)
        assert righe[4]["premio"] == pytest.approx(VAL_PTR_ATT - ASTA)
        assert righe[0]["sigma"] == pytest.approx(SIGMA * 0.5)
        assert righe[-1]["sigma"] == pytest.approx(SIGMA * 1.5)

    def test_monotona_in_vol(self):
        righe = ptr290_sensibilita_vol(SPREAD, SIGMA, T, ASTA)
        vals = [r["valore_ptr"] for r in righe]
        assert all(b >= a for a, b in zip(vals, vals[1:]))

    def test_premio_coerente(self):
        righe = ptr290_sensibilita_vol(SPREAD, SIGMA, T, ASTA)
        for r in righe:
            assert r["premio"] == pytest.approx(r["valore_ptr"] - ASTA)

    def test_n_punti_ko(self):
        with pytest.raises(ValueError):
            ptr290_sensibilita_vol(SPREAD, SIGMA, T, ASTA, n_punti=2)

    def test_ampiezza_ko(self):
        with pytest.raises(ValueError):
            ptr290_sensibilita_vol(SPREAD, SIGMA, T, ASTA, ampiezza=0.0)


class TestPtr290Breakdown:
    def test_chiavi_e_premio(self):
        b = ptr290_breakdown(7.0, ASTA)
        assert set(b) == {"valore_modello", "prezzo_asta", "premio"}
        assert b["premio"] == pytest.approx(b["valore_modello"] - b["prezzo_asta"])


class TestPtr290Verdetto:
    def test_sottoprezzato(self):
        assert ptr290_verdetto(1.0, SOGLIA)["verdetto"] == "sottoprezzato"

    def test_equo(self):
        assert ptr290_verdetto(0.2, SOGLIA)["verdetto"] == "equo"

    def test_sovrapprezzato(self):
        assert ptr290_verdetto(-0.1, SOGLIA)["verdetto"] == "sovrapprezzato"

    def test_soglia_negativa_ko(self):
        with pytest.raises(ValueError):
            ptr290_verdetto(0.2, -1.0)
