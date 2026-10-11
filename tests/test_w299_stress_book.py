"""Test tab299 '🧪⚡ Stress test: quanto perde il book negli scenari?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab299. Stress test deterministico del book:
shock di scenario per posizione, P&L per scenario, scenario peggiore e
verdetto semaforo (follow-up operativo del filone VaR tab292/296/297/298).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("st299_num", "st299_parse_book", "st299_parse_scenari",
          "st299_pnl_scenario", "st299_pnl_scenari",
          "st299_scenario_peggiore", "st299_perdita_massima_singola",
          "st299_verdetto")
st299_num = _F["st299_num"]
st299_parse_book = _F["st299_parse_book"]
st299_parse_scenari = _F["st299_parse_scenari"]
st299_pnl_scenario = _F["st299_pnl_scenario"]
st299_pnl_scenari = _F["st299_pnl_scenari"]
st299_scenario_peggiore = _F["st299_scenario_peggiore"]
st299_perdita_massima_singola = _F["st299_perdita_massima_singola"]
st299_verdetto = _F["st299_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"

# book sintetico 2 posizioni
SYN_BOOK = [("A", 1_000_000.0), ("B", 500_000.0)]
SYN_SCEN = {"ShockA": {"A": 0.10, "B": -0.05},
            "ShockB": {"A": -0.20, "B": -0.10}}
SYN_NOZ = 1_500_000.0

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""
DEMO_SCEN = """# scenario;posizione;shock % (+ = prezzo su, - = prezzo giu')
TTF shock invernale;Gas TTF;+40
TTF shock invernale;Power DE;+25
TTF shock invernale;CO2 EUA;+10
Crisi power;Gas TTF;+60
Crisi power;Power DE;+55
Crisi power;CO2 EUA;+20
Vendita forzata;Spark spread;-35
Vendita forzata;Gas TTF;-20
Taglio CO2;CO2 EUA;-30
Taglio CO2;Spark spread;-15"""


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab299:
    def test_tab299_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert TITLE299 in titoli
        assert "tab299" in dvars
        assert "tab299" in withs
        assert titoli[dvars.index("tab299")] == TITLE299
        assert titoli[-1] == TITLE374
        keys = re.findall(r'key="(st299_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_297_298_299(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab297")] == TITLE297
        assert titoli[dvars.index("tab298")] == TITLE298
        assert titoli[dvars.index("tab299")] == TITLE299


class TestSt299Num:
    def test_ok(self):
        assert st299_num(2.5, "x") == 2.5

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            st299_num(True, "x")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            st299_num(float("nan"), "x")

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            st299_num(float("inf"), "x")


class TestSt299ParseBook:
    def test_ok(self):
        p = st299_parse_book("Gas;1000000;2,5\nPower;2000000;3")
        assert p == [("Gas", 1_000_000.0), ("Power", 2_000_000.0)]

    def test_commenti_e_vuote(self):
        p = st299_parse_book("# cmt\n\n" + "\n".join(["X;100;1"] * 2))
        assert len(p) == 2

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            st299_parse_book("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            st299_parse_book("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            st299_parse_book("Gas;-5;2\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            st299_parse_book("Gas;xx;2\nPower;2000000;2")


class TestSt299ParseScenari:
    def test_ok(self):
        s = st299_parse_scenari("S1;A;+10\nS1;B;-5\nS2;A;20", ["A", "B"])
        assert set(s) == {"S1", "S2"}
        assert s["S1"] == {"A": 0.10, "B": -0.05}
        assert s["S2"] == {"A": 0.20}

    def test_posizione_sconosciuta_ko(self):
        with pytest.raises(ValueError):
            st299_parse_scenari("S1;C;10", ["A", "B"])

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            st299_parse_scenari("S1;A", ["A"])

    def test_shock_non_numerico_ko(self):
        with pytest.raises(ValueError):
            st299_parse_scenari("S1;A;xx", ["A"])

    def test_scenario_vuoto_ko(self):
        with pytest.raises(ValueError):
            st299_parse_scenari("# solo commenti", ["A"])

    def test_duplicato_ko(self):
        with pytest.raises(ValueError):
            st299_parse_scenari("S1;A;10\nS1;A;20", ["A"])


class TestSt299Pnl:
    def test_scenario_singolo(self):
        dett, tot = st299_pnl_scenario(SYN_BOOK, SYN_SCEN["ShockA"])
        assert tot == pytest.approx(75000.0)
        assert dett[0][3] == pytest.approx(100_000.0)
        assert dett[1][3] == pytest.approx(-25_000.0)

    def test_senza_shock_zero(self):
        dett, tot = st299_pnl_scenario(SYN_BOOK, {})
        assert tot == 0.0
        assert all(p == 0.0 for _, _, _, p in dett)

    def test_tutti(self):
        ris = st299_pnl_scenari(SYN_BOOK, SYN_SCEN)
        assert ris["ShockA"][1] == pytest.approx(75000.0)
        assert ris["ShockB"][1] == pytest.approx(-250000.0)


class TestSt299Peggiori:
    def test_scenario_peggiore(self):
        ris = st299_pnl_scenari(SYN_BOOK, SYN_SCEN)
        assert st299_scenario_peggiore(ris) == ("ShockB", pytest.approx(-250000.0))

    def test_perdita_massima_singola(self):
        ris = st299_pnl_scenari(SYN_BOOK, SYN_SCEN)
        assert st299_perdita_massima_singola(ris) == ("ShockB", "A",
                                                     pytest.approx(-200_000.0))

    def test_vuoti_ko(self):
        with pytest.raises(ValueError):
            st299_scenario_peggiore({})


class TestSt299Verdetto:
    def test_contenuta(self):
        assert st299_verdetto(2.0).startswith("contenuta")
        assert st299_verdetto(2.99).startswith("contenuta")

    def test_moderata(self):
        assert st299_verdetto(3.0).startswith("moderata")
        assert st299_verdetto(7.99).startswith("moderata")

    def test_attenzione_alta(self):
        assert st299_verdetto(8.0).startswith("attenzione alta")
        assert st299_verdetto(14.99).startswith("attenzione alta")

    def test_estremo(self):
        assert st299_verdetto(15.0).startswith("scenario estremo")
        assert st299_verdetto(40.0).startswith("scenario estremo")


class TestSt299Integrazione:
    def test_catena_demo(self):
        pos = st299_parse_book(DEMO_TXT)
        assert len(pos) == 4
        scenari = st299_parse_scenari(DEMO_SCEN, [p[0] for p in pos])
        assert len(scenari) == 4
        ris = st299_pnl_scenari(pos, scenari)
        pegg, tot = st299_scenario_peggiore(ris)
        assert pegg == 'Vendita forzata'
        assert tot == pytest.approx(-920000.0)
        noz = sum(w for _, w in pos)
        assert noz == pytest.approx(6400000.0)
        perdita = max(0.0, -tot / noz * 100.0)
        assert perdita == pytest.approx(14.374999999999998)
        assert st299_verdetto(perdita) == 'attenzione alta: perdita rilevante del nozionale'
        scen_m, pos_m, pnl_m = st299_perdita_massima_singola(ris)
        assert (scen_m, pos_m) == ('Vendita forzata', 'Gas TTF')
        assert pnl_m == pytest.approx(-500000.0)
