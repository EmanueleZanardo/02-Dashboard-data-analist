"""Test tab307 '🌊📉 Expected Shortfall: la perdita oltre il VaR': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab307. Expected Shortfall parametrico sotto
normale equi-correlata: ES = sigma*phi(z)/(1-alpha), decomposizione di Eulero
per posizione e segmento, rapporto ES/VaR costante nel modello normale,
semaforo coda grassa/moderata/sotto controllo contro la soglia del desk.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("es307_num", "es307_conf", "es307_corr", "es307_parse_book",
          "es307_norm_cdf", "es307_norm_ppf", "es307_norm_pdf",
          "es307_sigmas", "es307_es_book", "es307_var_book",
          "es307_componenti_es", "es307_componenti_var", "es307_seg",
          "es307_ratio", "es307_verdetto")
es307_num = _F["es307_num"]
es307_conf = _F["es307_conf"]
es307_corr = _F["es307_corr"]
es307_parse_book = _F["es307_parse_book"]
es307_norm_cdf = _F["es307_norm_cdf"]
es307_norm_ppf = _F["es307_norm_ppf"]
es307_norm_pdf = _F["es307_norm_pdf"]
es307_sigmas = _F["es307_sigmas"]
es307_es_book = _F["es307_es_book"]
es307_var_book = _F["es307_var_book"]
es307_componenti_es = _F["es307_componenti_es"]
es307_componenti_var = _F["es307_componenti_var"]
es307_seg = _F["es307_seg"]
es307_ratio = _F["es307_ratio"]
es307_verdetto = _F["es307_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"

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
SOGLIA = 1.25
VAR_TOT = 1774789.1364575038
ES_TOT = 2225657.178493701
RATIO_BOOK = 1.2540403435960477
SEG_ES = {'power': 1178331.8181331288, 'gas': 599588.5576374677, 'carbon': 280295.96400840586, 'flex': 167440.83871469882}
SEG_VAR = {'power': 939628.3175022749, 'gas': 478125.4133484301, 'carbon': 223514.3115130074, 'flex': 133521.09409379173}
RATIO_SEG = {'power': 1.2540403435960474, 'carbon': 1.2540403435960479, 'gas': 1.2540403435960479, 'flex': 1.2540403435960479}
VERDETTO = "coda grassa: ES/VaR 1.25 sopra la soglia 1.25: la perdita attesa oltre il VaR e' severa, ridurre l'esposizione di coda o aumentare il buffer di capitale"
Z95 = 1.6448536269514715
PHI_Z95 = 0.10313564037537153


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab307:
    def test_tab307_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 351
        assert TITLE307 in titoli
        assert "tab307" in dvars
        assert "tab307" in withs
        assert titoli[dvars.index("tab307")] == TITLE307
        assert titoli[-1] == TITLE351
        assert dvars[-1] == "tab351"
        keys = re.findall(r'key="(st307_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_305_306_307(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab305")] == TITLE305
        assert titoli[dvars.index("tab306")] == TITLE306
        assert titoli[dvars.index("tab307")] == TITLE307


class TestEs307Validatori:
    def test_num_ok(self):
        assert es307_num(3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                es307_num(bad, "x")

    def test_conf(self):
        assert es307_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                es307_conf(bad)

    def test_corr(self):
        assert es307_corr(1.0) == 1.0
        assert es307_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                es307_corr(bad)


class TestEs307Parse:
    def test_demo_book(self):
        assert es307_parse_book(BOOK_TXT) == BOOK

    def test_book_ko(self):
        for bad in ("solo;tre", "x;abc;10;power", "x;10;-5;power",
                    "x;0;10;power", ""):
            with pytest.raises(ValueError):
                es307_parse_book(bad)


class TestEs307Model:
    def test_ppf_pdf_95(self):
        z = es307_norm_ppf(0.95)
        assert z == pytest.approx(Z95)
        assert es307_norm_pdf(z) == pytest.approx(PHI_Z95)

    def test_es_totale(self):
        assert es307_es_book(BOOK, RHO, CONF) == pytest.approx(ES_TOT)

    def test_var_totale(self):
        assert es307_var_book(BOOK, RHO, CONF) == pytest.approx(VAR_TOT)

    def test_es_supera_var(self):
        assert es307_es_book(BOOK, RHO, CONF) > es307_var_book(BOOK, RHO, CONF)

    def test_eulero_es_somma(self):
        comp = es307_componenti_es(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(es307_es_book(BOOK, RHO, CONF))

    def test_eulero_var_somma(self):
        comp = es307_componenti_var(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(es307_var_book(BOOK, RHO, CONF))

    def test_seg_es_valori(self):
        seg = es307_seg(BOOK, es307_componenti_es(BOOK, RHO, CONF))
        assert set(seg) == set(SEG_ES)
        for s, v in SEG_ES.items():
            assert seg[s] == pytest.approx(v)

    def test_seg_var_somma(self):
        segv = es307_seg(BOOK, es307_componenti_var(BOOK, RHO, CONF))
        assert sum(segv.values()) == pytest.approx(es307_var_book(BOOK, RHO, CONF))

    def test_componenti_degeneri(self):
        book0 = [("Zero", 1000000.0, 0.0, "zero")]
        assert es307_componenti_es(book0, RHO, CONF) == [0.0]
        assert es307_componenti_var(book0, RHO, CONF) == [0.0]
        assert es307_es_book(book0, RHO, CONF) == 0.0
        assert es307_var_book(book0, RHO, CONF) == 0.0

    def test_seg_lunghezza_ko(self):
        with pytest.raises(ValueError):
            es307_seg(BOOK, [1.0])


class TestEs307Ratio:
    def _seg(self):
        segv = es307_seg(BOOK, es307_componenti_var(BOOK, RHO, CONF))
        sege = es307_seg(BOOK, es307_componenti_es(BOOK, RHO, CONF))
        return segv, sege

    def test_ratio_valori(self):
        segv, sege = self._seg()
        got = es307_ratio(segv, sege)
        assert set(got) == set(RATIO_SEG)
        for s, r in RATIO_SEG.items():
            assert got[s] == pytest.approx(r)

    def test_ratio_costante_normale(self):
        segv, sege = self._seg()
        got = es307_ratio(segv, sege)
        for r in got.values():
            assert r == pytest.approx(RATIO_BOOK)

    def test_ratio_book(self):
        assert es307_es_book(BOOK, RHO, CONF) / es307_var_book(BOOK, RHO, CONF) \
            == pytest.approx(RATIO_BOOK)

    def test_var_zero_none(self):
        assert es307_ratio({"s": 0.0}, {"s": 100.0}) == {"s": None}

    def test_var_negativo_ko(self):
        with pytest.raises(ValueError):
            es307_ratio({"s": -1.0}, {"s": 10.0})


class TestEs307Verdetto:
    def test_coda_grassa(self):
        assert es307_verdetto(1.30, 1.25).startswith("coda grassa")
        assert es307_verdetto(1.25, 1.25).startswith("coda grassa")

    def test_coda_moderata(self):
        assert es307_verdetto(1.20, 1.25).startswith("coda moderata")
        assert es307_verdetto(1.15, 1.25).startswith("coda moderata")

    def test_sotto_controllo(self):
        assert es307_verdetto(1.05, 1.25).startswith("coda sotto controllo")

    def test_soglia_ko(self):
        for bad in (1.0, 0.9, -1.5):
            with pytest.raises(ValueError):
                es307_verdetto(1.3, bad)

    def test_verdetto_demo(self):
        assert es307_verdetto(RATIO_BOOK, SOGLIA) == VERDETTO
