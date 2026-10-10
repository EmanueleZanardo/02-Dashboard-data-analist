"""Test tab292 '🪓📊 Component VaR: quale posizione tagliare per prima?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab292.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cv292_num", "cv292_pos", "cv292_conf", "cv292_norm_cdf",
          "cv292_norm_ppf", "cv292_z", "cv292_parse_posizioni",
          "cv292_sigma_portafoglio", "cv292_var_standalone",
          "cv292_var_portafoglio", "cv292_component_var",
          "cv292_beneficio_diversificazione", "cv292_ranking_taglio",
          "cv292_verdetto")
cv292_num = _F["cv292_num"]
cv292_pos = _F["cv292_pos"]
cv292_conf = _F["cv292_conf"]
cv292_norm_cdf = _F["cv292_norm_cdf"]
cv292_norm_ppf = _F["cv292_norm_ppf"]
cv292_z = _F["cv292_z"]
cv292_parse_posizioni = _F["cv292_parse_posizioni"]
cv292_sigma_portafoglio = _F["cv292_sigma_portafoglio"]
cv292_var_standalone = _F["cv292_var_standalone"]
cv292_var_portafoglio = _F["cv292_var_portafoglio"]
cv292_component_var = _F["cv292_component_var"]
cv292_beneficio_diversificazione = _F["cv292_beneficio_diversificazione"]
cv292_ranking_taglio = _F["cv292_ranking_taglio"]
cv292_verdetto = _F["cv292_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"

POS = [{"nome": "TTF", "valore": 2500000.0, "vol": 0.018},
       {"nome": "PSV", "valore": -1200000.0, "vol": 0.021},
       {"nome": "PowerDE", "valore": 1800000.0, "vol": 0.024}]


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab292:
    def test_tab292_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 359
        assert TITLE292 in titoli
        assert "tab292" in dvars
        assert "tab292" in withs
        assert titoli[dvars.index("tab292")] == TITLE292
        assert titoli[-1] == TITLE359
        keys = re.findall(r'key="(cv292_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_290_291_292(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab290")] == TITLE290
        assert titoli[dvars.index("tab291")] == TITLE291
        assert titoli[dvars.index("tab292")] == TITLE292


class TestCv292Validatori:
    def test_num_ok(self):
        assert cv292_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            cv292_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            cv292_num(float("nan"), "x")

    def test_pos_zero_ko(self):
        with pytest.raises(ValueError):
            cv292_pos(0.0, "x")

    def test_conf_ok(self):
        assert cv292_conf(0.95) == 0.95

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            cv292_conf(0.0)
        with pytest.raises(ValueError):
            cv292_conf(1.0)


class TestCv292Normale:
    def test_cdf_zero(self):
        assert cv292_norm_cdf(0.0) == pytest.approx(0.5)

    def test_cdf_196(self):
        assert cv292_norm_cdf(1.96) == pytest.approx(0.975, abs=1e-3)

    def test_ppf_median(self):
        assert cv292_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)

    def test_ppf_975(self):
        assert cv292_norm_ppf(0.975) == pytest.approx(1.95996398, rel=1e-6)

    def test_ppf_99(self):
        assert cv292_norm_ppf(0.99) == pytest.approx(2.32634787, rel=1e-6)

    def test_ppf_simmetria(self):
        assert cv292_norm_ppf(0.025) == pytest.approx(-1.95996398, rel=1e-6)

    def test_ppf_roundtrip(self):
        for x in (-1.5, -0.2, 0.7, 1.5, 2.5):
            assert cv292_norm_ppf(cv292_norm_cdf(x)) == pytest.approx(x,
                                                                     rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            cv292_norm_ppf(0.0)
        with pytest.raises(ValueError):
            cv292_norm_ppf(1.0)

    def test_z_95(self):
        assert cv292_z(0.95) == pytest.approx(1.64485362, rel=1e-6)


class TestCv292Parse:
    def test_ok(self):
        p = cv292_parse_posizioni("TTF;2500000;1,8\n# cmt\n\nPSV;-1200000;2.1")
        assert [x["nome"] for x in p] == ["TTF", "PSV"]
        assert [x["valore"] for x in p] == [2500000.0, -1200000.0]
        assert [x["vol"] for x in p] == pytest.approx([0.018, 0.021])

    def test_riga_malformata_ko(self):
        with pytest.raises(ValueError):
            cv292_parse_posizioni("TTF;2500000")

    def test_valore_zero_ko(self):
        with pytest.raises(ValueError):
            cv292_parse_posizioni("TTF;0;1.8")

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            cv292_parse_posizioni("TTF;1000;-1.8")

    def test_nomi_duplicati_ko(self):
        with pytest.raises(ValueError):
            cv292_parse_posizioni("TTF;1000;1.0\nTTF;2000;1.0")

    def test_vuoto_ko(self):
        with pytest.raises(ValueError):
            cv292_parse_posizioni("# solo commenti\n")


class TestCv292Sigma:
    def test_singola(self):
        assert cv292_sigma_portafoglio([100.0], 0.3) == pytest.approx(100.0)

    def test_rho_uno(self):
        assert cv292_sigma_portafoglio([100.0, 50.0], 1.0) == \
            pytest.approx(150.0)

    def test_rho_zero(self):
        assert cv292_sigma_portafoglio([100.0, 100.0], 0.0) == \
            pytest.approx(math.sqrt(2.0) * 100.0)

    def test_rho_fuori_range_ko(self):
        with pytest.raises(ValueError):
            cv292_sigma_portafoglio([100.0, 50.0], 1.5)


class TestCv292Var:
    def test_standalone_formula(self):
        att = 1_000_000.0 * 0.02 * math.sqrt(10.0) * 1.64485362
        assert cv292_var_standalone(1_000_000.0, 0.02, 10, 0.95) == \
            pytest.approx(att, rel=1e-6)

    def test_standalone_short_usa_abs(self):
        assert cv292_var_standalone(-500.0, 0.01, 5, 0.9) == \
            pytest.approx(cv292_var_standalone(500.0, 0.01, 5, 0.9))

    def test_portafoglio_singolo_uguale_standalone(self):
        p = [{"nome": "A", "valore": 1e6, "vol": 0.02}]
        assert cv292_var_portafoglio(p, 0.3, 10, 0.95) == pytest.approx(
            cv292_var_standalone(1e6, 0.02, 10, 0.95))

    def test_portafoglio_rho_uno_uguale_somma(self):
        v = cv292_var_portafoglio(POS, 1.0, 10, 0.95)
        s = sum(cv292_var_standalone(p["valore"], p["vol"], 10, 0.95)
                for p in POS)
        assert v == pytest.approx(s)

    def test_diversificazione_positiva(self):
        b = cv292_beneficio_diversificazione(POS, 0.3, 10, 0.95)
        assert b["beneficio"] > 0
        assert b["somma_standalone"] == pytest.approx(
            b["var_portafoglio"] + b["beneficio"])

    def test_componenti_sommano_a_totale(self):
        comp = cv292_component_var(POS, 0.3, 10, 0.95)
        tot = cv292_var_portafoglio(POS, 0.3, 10, 0.95)
        assert sum(c["componente"] for c in comp) == pytest.approx(tot)

    def test_componente_singola_uguale_standalone(self):
        p = [{"nome": "A", "valore": 1e6, "vol": 0.02}]
        comp = cv292_component_var(p, 0.3, 10, 0.95)
        assert comp[0]["componente"] == pytest.approx(
            cv292_var_standalone(1e6, 0.02, 10, 0.95))

    def test_ranking_prima_max(self):
        rank = cv292_ranking_taglio(POS, 0.3, 10, 0.95)
        comp = [c["componente"] for c in
                cv292_component_var(POS, 0.3, 10, 0.95)]
        assert rank[0]["componente"] == pytest.approx(max(comp))
        assert [r["nome"] for r in rank] == sorted(
            [r["nome"] for r in rank],
            key=lambda n: next(c["componente"] for c in rank
                               if c["nome"] == n), reverse=True)

    def test_verdetto(self):
        assert cv292_verdetto(100.0, 200.0)["verdetto"] == "dentro limite"
        assert cv292_verdetto(300.0, 200.0)["verdetto"] == "fuori limite"
        assert cv292_verdetto(100.0, 200.0)["uso_limite"] == \
            pytest.approx(0.5)

    def test_verdetto_limite_non_positivo_ko(self):
        with pytest.raises(ValueError):
            cv292_verdetto(100.0, 0.0)
