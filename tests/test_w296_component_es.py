"""Test tab296 '🪓🛡 Component ES: chi contribuisce alla coda?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab296. Allocazione di Eulero dell'ES:
CES_i = E[L_i | L_tot > VaR], somma_i CES_i = ES.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ce296_num", "ce296_conf", "ce296_parse_matrice",
          "ce296_quantile", "ce296_componenti", "ce296_verdetto")
ce296_num = _F["ce296_num"]
ce296_conf = _F["ce296_conf"]
ce296_parse_matrice = _F["ce296_parse_matrice"]
ce296_quantile = _F["ce296_quantile"]
ce296_componenti = _F["ce296_componenti"]
ce296_verdetto = _F["ce296_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE428 = "⏱️ Tempo sott'acqua: durata dei drawdown e recupero"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE467 = "📅 L'edge annualizzato: il trade si ripete?"
TITLE466 = "💸 Costi veri: l'edge sopravvive al netto?"
TITLE465 = "📐 Correlazione: la diversificazione è reale?"
TITLE464 = "🧺 Portafoglio: quanti trade insieme?"
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE427 = "🛡 CDaR: la perdita media dei peggiori drawdown"
TITLE429 = "🎯 Attribuzione del drawdown: chi ha causato il peggior calo"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"

# matrice sintetica 20x2 a valori noti: A=[100]*5+[0]*15, B=[50]*5+[0]*15
SYN_MATRICE = [[100.0, 50.0]] * 5 + [[0.0, 0.0]] * 15

DEMO_TXT = """88,66;-126,32;-68,09
-144,61;527,22;539,76
148,57;-134,88;74,99
722,39;-148,75;-149,99
-96,02;-97,44;89,49
1674,31;-60,09;638,81
70,4;-96,72;134,4
-137,05;663,18;-144,07
621,44;451,64;-148,11
-145,41;-100,42;152,36
2504,37;154,86;-131,85
-135,66;473,31;126,38
-148,49;-140,71;-120,04
-149,79;-70,31;-7,06
146,15;-149,13;-110,02
1145,85;42,18;-76,79
-126,57;-67,55;732,16
-147,98;-13,51;-79,43
79,45;-124,92;1715,81
321,97;-148,72;-149,68
-54,55;-121,78;-78,18
-131,57;494,93;-149,84
-149,88;-134,73;-124,72
538,52;643,16;933,61
-81,8;-102,37;-101,25
-149,97;-148,77;69,25
-81,25;-129,89;269,72
130,37;440,08;366,81
-135,35;-149,92;2644,91
-115,64;667,79;-109,58
-137,47;334,22;-117,0
-146,6;-110,21;-142,05
-104,15;521,38;-115,29
286,64;-149,99;-58,32
-150,0;-90,23;-111,37
-145,6;266,98;144,33
-105,25;-15,57;-148,86
-108,49;-141,35;-143,56
330,32;-149,5;16,01
25,11;-149,66;521,29
-149,84;464,71;187,2
-47,73;-86,08;-98,97
-149,72;-48,82;-123,74
181,61;-53,74;348,51
564,28;-139,33;153,81
-149,94;52,52;-141,82
344,07;-112,8;559,82
-137,48;-51,73;80,06"""


def _demo_matrice():
    righe = []
    for ln in DEMO_TXT.split("\n"):
        s = ln.strip()
        if not s:
            continue
        righe.append([float(c.replace(",", ".")) for c in s.split(";")])
    return righe


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab296:
    def test_tab296_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 738
        assert TITLE296 in titoli
        assert "tab296" in dvars
        assert "tab296" in withs
        assert titoli[dvars.index("tab296")] == TITLE296
        assert TITLE482 in titoli
        keys = re.findall(r'key="(ce296_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_294_295_296(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab294")] == TITLE294
        assert titoli[dvars.index("tab295")] == TITLE295
        assert titoli[dvars.index("tab296")] == TITLE296


class TestCe296Validatori:
    def test_num_ok(self):
        assert ce296_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            ce296_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            ce296_num(float("nan"), "x")

    def test_conf_ok(self):
        assert ce296_conf(0.975) == 0.975

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            ce296_conf(1.0)
        with pytest.raises(ValueError):
            ce296_conf(0.0)


class TestCe296Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["1,5;2"] * 20)
        m = ce296_parse_matrice(t)
        assert len(m) == 20 and len(m[0]) == 2
        assert m[0][0] == pytest.approx(1.5)

    def test_una_colonna_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1"] * 20))

    def test_troppo_poche_righe_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19))

    def test_righe_disallineate_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19 + ["1;2;3"]))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19 + ["1;xx"]))


class TestCe296Quantile:
    def test_mediana(self):
        assert ce296_quantile([3.0, 1.0, 2.0], 0.5) == pytest.approx(2.0)

    def test_interpolazione(self):
        # type-7: pos = 0.25*3 = 0.75 -> 1 + 3*0.75 = 3.25
        assert ce296_quantile([1.0, 2.0, 3.0, 4.0], 0.25) == pytest.approx(1.75)

    def test_bordi(self):
        assert ce296_quantile([5.0, 6.0], 0.0) == pytest.approx(5.0)
        assert ce296_quantile([5.0, 6.0], 1.0) == pytest.approx(6.0)

    def test_singolo(self):
        assert ce296_quantile([7.0], 0.9) == pytest.approx(7.0)

    def test_q_fuori_range_ko(self):
        with pytest.raises(ValueError):
            ce296_quantile([1.0, 2.0], 1.5)

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            ce296_quantile([], 0.5)


class TestCe296Componenti:
    def test_sintetico_valori_noti(self):
        # totali = [150]*5 + [0]*15, conf 0.75 -> VaR = 37.5, 5 superamenti
        r = ce296_componenti(SYN_MATRICE, 0.75)
        assert r["n"] == 20
        assert r["m"] == 2
        assert r["var"] == pytest.approx(37.5)
        assert r["superamenti"] == 5
        assert r["es"] == pytest.approx(150.0)
        assert r["componenti"][0] == pytest.approx(100.0)
        assert r["componenti"][1] == pytest.approx(50.0)
        assert sum(r["componenti"]) == pytest.approx(r["es"])
        assert r["quote"][0] == pytest.approx(0.6666666666666666)
        assert r["standalone"][0] == pytest.approx(100.0)
        assert r["standalone"][1] == pytest.approx(50.0)
        assert r["diversificazione"] == pytest.approx(0.0)

    def test_nessun_superamento_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti([[1.0, 1.0]] * 20, 0.999)

    def test_righe_disallineate_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti([[1.0, 2.0], [1.0]], 0.9)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti(SYN_MATRICE, 1.0)


class TestCe296Verdetto:
    def test_diversificata(self):
        assert ce296_verdetto(0.3) == "coda diversificata: nessuna posizione domina"

    def test_elevata(self):
        assert ce296_verdetto(0.6).startswith("concentrazione elevata")

    def test_critica(self):
        assert ce296_verdetto(0.8).startswith("concentrazione critica")

    def test_soglie(self):
        assert ce296_verdetto(0.5).startswith("concentrazione elevata")
        assert ce296_verdetto(0.7).startswith("concentrazione critica")

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            ce296_verdetto(1.2)


class TestCe296Integrazione:
    def test_catena_demo(self):
        m = _demo_matrice()
        assert len(m) == 48
        assert len(m[0]) == 3
        r = ce296_componenti(m, 0.975)
        assert r["n"] == 48
        assert r["superamenti"] == 2
        assert r["var"] == pytest.approx(2340.9832499999993)
        assert r["es"] == pytest.approx(2443.51)
        assert sum(r["componenti"]) == pytest.approx(r["es"])
        assert r["componenti"][0] == pytest.approx(1184.51)
        assert max(r["quote"]) == pytest.approx(0.5142315767072776)
        assert ce296_verdetto(max(r["quote"])) == 'concentrazione elevata: la coda dipende da poche posizioni'
        # parse round-trip della demo come appare nella UI
        m2 = ce296_parse_matrice(DEMO_TXT)
        assert len(m2) == 48
