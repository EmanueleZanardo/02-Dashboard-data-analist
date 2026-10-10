"""Test tab308 '💥📈 Stress di correlazione: quanto sale il VaR se si rompono?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab di rischio precedenti, piu' la matematica dello stress di
correlazione: VaR base/stress/tetto, curva monotona, Eulero e verdetto.
"""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("sc308_num", "sc308_conf", "sc308_corr", "sc308_parse_book",
           "sc308_norm_ppf", "sc308_sigmas", "sc308_var_book",
           "sc308_var_curva", "sc308_stress", "sc308_componenti_var",
           "sc308_seg", "sc308_verdetto")

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
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
BOOK_DEMO = ("Cal-28 Baseload power;2500000;18,5;power\n"
             "Q3-28 Peak power;1200000;26,0;power\n"
             "TTF Gas Cal-28;1800000;22,0;gas\n"
             "EUA Carbon Dec-28;700000;31,0;carbon")
RHO_BASE = 0.35
RHO_STRESS = 0.90
CONF = 95
SOGLIA = 25.0
SIG_DEMO = [462500.0, 312000.0, 396000.0, 217000.0]

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
Z95 = 1.6448536269514715
S2B = 1008655600000.0
VAR_BASE = 1651956.8868516753
VAR_STRESS = 2197068.954929856
VAR_TETTO = 2282234.407395167
INCR_PCT = 32.99795971776622
BUFFER_EUR = 545112.0680781808
PENDENZA = 1154636.3607249833
SIG_SUM = 1387500.0
VERDETTO = "breakdown severo: il VaR sale del 33.0% sopra la soglia 25.0%: aumentare il buffer o ridurre le posizioni piu' correlate"
SEG_MAX = "power"


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry308:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 363
        assert TITLE308 in titoli
        assert "tab308" in dvars
        assert "    with tab308:" in src

    def test_titoli_allineati_306_307_308(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab306")] == TITLE306
        assert titoli[dvars.index("tab307")] == TITLE307
        assert titoli[dvars.index("tab308")] == TITLE308

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE363
        assert dvars[-1] == "tab363"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["sc308_conf"](95) == 95

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["sc308_conf"](97)

    def test_corr_fuori_range(self):
        with pytest.raises(ValueError):
            _F["sc308_corr"](1.5)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["sc308_num"](True, "x")

    def test_parse_book_ok(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        assert len(book) == 4
        assert book[0] == ("Cal-28 Baseload power", 2500000.0, 0.185, "power")

    def test_parse_book_3campi_ko(self):
        with pytest.raises(ValueError):
            _F["sc308_parse_book"]("nome;1000;20,0")

    def test_parse_book_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["sc308_parse_book"]("   \n  ")


class TestMatematica:
    def test_ppf_95(self):
        assert abs(_F["sc308_norm_ppf"](0.95) - 1.6448536269514722) < 1e-3

    def test_sigmas_due_posizioni(self):
        # sig1=200, sig2=50, rho=0.5 -> s2 = 40000+2500+2*0.5*200*50 = 52500
        sig, s2 = _F["sc308_sigmas"](
            [("a", 1000.0, 0.2, "x"), ("b", 500.0, 0.1, "y")], 0.5)
        assert sig == [200.0, 50.0]
        assert s2 == pytest.approx(52500.0)

    def test_var_tetto_forma_chiusa(self):
        # a rho=1 la varianza e' (somma sig)^2: check indipendente
        book = _F["sc308_parse_book"](BOOK_DEMO)
        st = _F["sc308_stress"](book, RHO_BASE, RHO_STRESS, CONF)
        assert st["var_tetto"] == pytest.approx(Z95 * SIG_SUM, rel=1e-9)

    def test_stress_demo(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        st = _F["sc308_stress"](book, RHO_BASE, RHO_STRESS, CONF)
        assert st["var_base"] == pytest.approx(VAR_BASE, rel=1e-9)
        assert st["var_stress"] == pytest.approx(VAR_STRESS, rel=1e-9)
        assert st["incremento_pct"] == pytest.approx(INCR_PCT, rel=1e-9)
        assert st["buffer_eur"] == pytest.approx(BUFFER_EUR, rel=1e-9)
        assert st["pendenza"] == pytest.approx(PENDENZA, rel=1e-9)
        assert st["incremento_pct"] == pytest.approx(
            100.0 * (VAR_STRESS - VAR_BASE) / VAR_BASE, rel=1e-9)

    def test_stress_ordine(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        st = _F["sc308_stress"](book, RHO_BASE, RHO_STRESS, CONF)
        assert st["var_base"] < st["var_stress"] <= st["var_tetto"]

    def test_s2_demo(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        _, s2 = _F["sc308_sigmas"](book, RHO_BASE)
        assert s2 == pytest.approx(S2B, rel=1e-9)

    def test_componenti_somma_eulero(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        comp = _F["sc308_componenti_var"](book, RHO_STRESS, CONF)
        assert sum(comp) == pytest.approx(
            _F["sc308_var_book"](book, RHO_STRESS, CONF), rel=1e-9)

    def test_seg_somma(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        comp = _F["sc308_componenti_var"](book, RHO_STRESS, CONF)
        seg = _F["sc308_seg"](book, comp)
        assert sum(seg.values()) == pytest.approx(
            _F["sc308_var_book"](book, RHO_STRESS, CONF), rel=1e-9)
        assert max(seg, key=seg.get) == SEG_MAX

    def test_curva_monotona_ed_estremi(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        curva = _F["sc308_var_curva"](book, CONF)
        assert len(curva) == 41
        assert curva[0][0] == pytest.approx(-1.0)
        assert curva[-1][0] == pytest.approx(1.0)
        vals = [v for _, v in curva]
        assert all(b >= a for a, b in zip(vals, vals[1:]))
        assert curva[-1][1] == pytest.approx(VAR_TETTO, rel=1e-9)

    def test_curva_n_ko(self):
        book = _F["sc308_parse_book"](BOOK_DEMO)
        with pytest.raises(ValueError):
            _F["sc308_var_curva"](book, CONF, n=2)


class TestVerdetto:
    def test_severo(self):
        v = _F["sc308_verdetto"](40.0, SOGLIA)
        assert v.startswith("breakdown severo")

    def test_moderato(self):
        v = _F["sc308_verdetto"](20.0, SOGLIA)
        assert v.startswith("breakdown moderato")

    def test_resiliente(self):
        v = _F["sc308_verdetto"](5.0, SOGLIA)
        assert v.startswith("resiliente")

    def test_non_valutabile(self):
        v = _F["sc308_verdetto"](None, SOGLIA)
        assert v.startswith("non valutabile")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith("breakdown severo")

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["sc308_verdetto"](10.0, 0.0)
