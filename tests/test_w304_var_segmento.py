"""Test tab304 '🗂️📊 VaR per segmento: dove si concentra il rischio?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab304. VaR per segmento: i component VaR di Eulero
(tab292) aggregati per segmento (power, gas, carbon, flex) con quote %, HHI di
concentrazione e semaforo diversificato/attenzionato/concentrato.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("sv304_num", "sv304_conf", "sv304_corr", "sv304_parse_book",
          "sv304_norm_cdf", "sv304_norm_ppf", "sv304_sigmas",
          "sv304_var_book", "sv304_componenti", "sv304_segmenti",
          "sv304_hhi", "sv304_standalone", "sv304_verdetto")
sv304_num = _F["sv304_num"]
sv304_conf = _F["sv304_conf"]
sv304_corr = _F["sv304_corr"]
sv304_parse_book = _F["sv304_parse_book"]
sv304_norm_cdf = _F["sv304_norm_cdf"]
sv304_norm_ppf = _F["sv304_norm_ppf"]
sv304_sigmas = _F["sv304_sigmas"]
sv304_var_book = _F["sv304_var_book"]
sv304_componenti = _F["sv304_componenti"]
sv304_segmenti = _F["sv304_segmenti"]
sv304_hhi = _F["sv304_hhi"]
sv304_standalone = _F["sv304_standalone"]
sv304_verdetto = _F["sv304_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"

BOOK_TXT = ("Cal-28 Baseload power;2500000;18,5;power\n"
            "Q3-28 Peak power;1200000;26,0;power\n"
            "TTF Gas Cal-28;1800000;22,0;gas\n"
            "EUA Carbon Dec-28;700000;31,0;carbon\n"
            "Batteria arbitrage;500000;28,0;flex")
BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185, "power"),
        ("Q3-28 Peak power", 1200000.0, 0.26, "power"),
        ("TTF Gas Cal-28", 1800000.0, 0.22, "gas"),
        ("EUA Carbon Dec-28", 700000.0, 0.31, "carbon"),
        ("Batteria arbitrage", 500000.0, 0.28, "flex")]
RHO = 0.35
CONF = 95
VAR_TOT = 1774789.1364575038
SEG_EUR = {'power': 939628.3175022749, 'gas': 478125.4133484301, 'carbon': 223514.3115130074, 'flex': 133521.09409379173}
SEG_QUOTE = {'power': 52.94309606705063, 'gas': 26.939843360928663, 'carbon': 12.593851681960599, 'flex': 7.5232088900600935}
HHI = 3743.9303536670254
STANDALONE = 2512513.915168373
TOP_SEG = 'power'
QUOTA_TOP = 52.94309606705063
N_SEG = 4
VERDETTO = "rischio attenzionato: 'power' pesa 52.9 % del VaR (HHI 3744): la concentrazione comincia a pesare, valuta un hedge mirato"
Z95 = 1.6448536269514715


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab304:
    def test_tab304_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 373
        assert TITLE304 in titoli
        assert "tab304" in dvars
        assert "tab304" in withs
        assert titoli[dvars.index("tab304")] == TITLE304
        assert titoli[-1] == TITLE373
        assert dvars[-1] == "tab373"
        keys = re.findall(r'key="(st304_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_302_303_304(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab302")] == TITLE302
        assert titoli[dvars.index("tab303")] == TITLE303
        assert titoli[dvars.index("tab304")] == TITLE304


class TestSv304Validatori:
    def test_num_ok(self):
        assert sv304_num(3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                sv304_num(bad, "x")

    def test_conf(self):
        assert sv304_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                sv304_conf(bad)

    def test_corr(self):
        assert sv304_corr(1.0) == 1.0
        assert sv304_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                sv304_corr(bad)


class TestSv304Parse:
    def test_demo(self):
        book = sv304_parse_book(BOOK_TXT)
        assert book == BOOK

    def test_righe_vuote(self):
        assert len(sv304_parse_book("\n" + BOOK_TXT + "\n")) == 5

    def test_formato_ko(self):
        for bad in ("", "   ", "a;b;c", "a;b;c;d;e", ";100;10;s",
                    "x;-100;10;s", "x;100;-5;s", "x;100;10;", "x;100;10; ",
                    "x;abc;10;s", 123):
            with pytest.raises(ValueError):
                sv304_parse_book(bad)


class TestSv304Norm:
    def test_ppf95(self):
        assert sv304_norm_ppf(0.95) == pytest.approx(1.6448536, abs=1e-6)
        assert sv304_norm_ppf(0.95) == pytest.approx(Z95, abs=1e-9)

    def test_cdf(self):
        assert sv304_norm_cdf(0.0) == 0.5
        assert sv304_norm_cdf(Z95) == pytest.approx(0.95, abs=1e-9)

    def test_ppf_ko(self):
        for bad in (0.0, 1.0):
            with pytest.raises(ValueError):
                sv304_norm_ppf(bad)


class TestSv304Componenti:
    def test_somma_uguale_var(self):
        varb = sv304_var_book(BOOK, RHO, CONF)
        comps = sv304_componenti(BOOK, RHO, CONF)
        assert len(comps) == 5
        assert sum(comps) == pytest.approx(varb, rel=1e-9)
        assert varb == pytest.approx(VAR_TOT)

    def test_singola_posizione(self):
        b = [("A", 1000.0, 0.2, "x")]
        assert sv304_componenti(b, 0.5, 95) == pytest.approx(
            [sv304_norm_ppf(0.95) * 200.0])

    def test_rho1_somma_lineare(self):
        b = [("A", 1000.0, 0.2, "x"), ("B", 500.0, 0.3, "y")]
        z = sv304_norm_ppf(0.95)
        comps = sv304_componenti(b, 1.0, 95)
        assert sum(comps) == pytest.approx(z * (200.0 + 150.0))
        assert comps[0] / comps[1] == pytest.approx(200.0 / 150.0)


class TestSv304Segmenti:
    def test_demo(self):
        comps = sv304_componenti(BOOK, RHO, CONF)
        segs = sv304_segmenti(BOOK, comps)
        assert [r["segmento"] for r in segs] == ["power", "gas", "carbon",
                                                "flex"]
        for r in segs:
            assert r["var_eur"] == pytest.approx(SEG_EUR[r["segmento"]])
            assert r["quota_pct"] == pytest.approx(SEG_QUOTE[r["segmento"]])
        assert sum(r["quota_pct"] for r in segs) == pytest.approx(100.0)
        assert len(segs) == N_SEG
        assert segs[0]["segmento"] == TOP_SEG

    def test_quote_non_negative_in_demo(self):
        comps = sv304_componenti(BOOK, RHO, CONF)
        segs = sv304_segmenti(BOOK, comps)
        assert all(r["quota_pct"] >= 0.0 for r in segs)

    def test_lunghezze_diverse_ko(self):
        with pytest.raises(ValueError):
            sv304_segmenti(BOOK, [1.0, 2.0])


class TestSv304Hhi:
    def test_demo(self):
        comps = sv304_componenti(BOOK, RHO, CONF)
        assert sv304_hhi(sv304_segmenti(BOOK, comps)) == pytest.approx(HHI)

    def test_due_uguali(self):
        segs = [{"segmento": "a", "var_eur": 50.0, "quota_pct": 50.0},
                {"segmento": "b", "var_eur": 50.0, "quota_pct": 50.0}]
        assert sv304_hhi(segs) == pytest.approx(5000.0)

    def test_monopolio(self):
        segs = [{"segmento": "a", "var_eur": 100.0, "quota_pct": 100.0}]
        assert sv304_hhi(segs) == pytest.approx(10000.0)


class TestSv304Standalone:
    def test_diversificazione(self):
        solo = sv304_standalone(BOOK, CONF)
        varb = sv304_var_book(BOOK, RHO, CONF)
        assert solo == pytest.approx(STANDALONE)
        assert solo > varb


class TestSv304Verdetto:
    def test_demo(self):
        comps = sv304_componenti(BOOK, RHO, CONF)
        segs = sv304_segmenti(BOOK, comps)
        h = sv304_hhi(segs)
        assert sv304_verdetto(TOP_SEG, QUOTA_TOP, h) == VERDETTO
        assert TOP_SEG in VERDETTO

    def test_concentrato(self):
        v = sv304_verdetto("gas", 75.0, 6000.0)
        assert v.startswith("rischio concentrato")

    def test_attenzionato(self):
        v = sv304_verdetto("power", 45.0, 3500.0)
        assert v.startswith("rischio attenzionato")

    def test_diversificato(self):
        v = sv304_verdetto("power", 25.0, 2500.0)
        assert v.startswith("rischio diversificato")

    def test_hhi_negativo_ko(self):
        with pytest.raises(ValueError):
            sv304_verdetto("x", 10.0, -1.0)
