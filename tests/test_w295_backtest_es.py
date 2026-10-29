"""Test tab295 '🧪🛡️ Backtest dell'ES: la coda e' sottostimata?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab295. Backtest di Acerbi-Szekely (2014) su Z1/Z2.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("es295_num", "es295_pos", "es295_conf", "es295_parse_pnl",
          "es295_perdite", "es295_parametri", "es295_superamenti",
          "es295_z1", "es295_z2", "es295_norm_cdf",
          "es295_pvalue_asintotico", "es295_verdetto")
es295_num = _F["es295_num"]
es295_pos = _F["es295_pos"]
es295_conf = _F["es295_conf"]
es295_parse_pnl = _F["es295_parse_pnl"]
es295_perdite = _F["es295_perdite"]
es295_parametri = _F["es295_parametri"]
es295_superamenti = _F["es295_superamenti"]
es295_z1 = _F["es295_z1"]
es295_z2 = _F["es295_z2"]
es295_norm_cdf = _F["es295_norm_cdf"]
es295_pvalue_asintotico = _F["es295_pvalue_asintotico"]
es295_verdetto = _F["es295_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"

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


class TestRegistryTab295:
    def test_tab295_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 793
        assert TITLE295 in titoli
        assert "tab295" in dvars
        assert "tab295" in withs
        assert titoli[dvars.index("tab295")] == TITLE295
        assert TITLE482 in titoli
        keys = re.findall(r'key="(es295_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_293_294_295(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab293")] == TITLE293
        assert titoli[dvars.index("tab294")] == TITLE294
        assert titoli[dvars.index("tab295")] == TITLE295


class TestEs295Validatori:
    def test_num_ok(self):
        assert es295_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            es295_num(True, "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            es295_num(float("inf"), "x")

    def test_pos_negativo_ko(self):
        with pytest.raises(ValueError):
            es295_pos(-1.0, "x")

    def test_conf_ok(self):
        assert es295_conf(0.975) == 0.975

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            es295_conf(1.0)
        with pytest.raises(ValueError):
            es295_conf(0.0)


class TestEs295Parse:
    def test_ok_virgole_commenti(self):
        vals = es295_parse_pnl("# cmt\n\n1,5\n" + "\n".join(["2"] * 19))
        assert len(vals) == 20
        assert vals[0] == pytest.approx(1.5)

    def test_troppo_pochi_ko(self):
        with pytest.raises(ValueError):
            es295_parse_pnl("\n".join(["1"] * 19))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            es295_parse_pnl("\n".join(["1"] * 19 + ["abc"]))


class TestEs295Perdite:
    def test_conversione(self):
        assert es295_perdite([100.0, -50.0, 0.0]) == [-100.0, 50.0, -0.0]

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            es295_perdite([])


class TestEs295Parametri:
    def test_ok(self):
        p = es295_parametri(2000.0, 3200.0, 0.975)
        assert p == {"var": 2000.0, "es": 3200.0, "conf": 0.975,
                     "atteso": pytest.approx(0.025)}

    def test_es_uguale_var_ok(self):
        assert es295_parametri(2000.0, 2000.0, 0.95)["es"] == 2000.0

    def test_es_minore_var_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(3200.0, 2000.0, 0.975)

    def test_var_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(0.0, 3200.0, 0.975)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(2000.0, 3200.0, 1.0)


class TestEs295Superamenti:
    def test_conteggio(self):
        r = es295_superamenti([100.0, 2500.0, 50.0, 2600.0, 300.0], 2000.0)
        assert r["n"] == 5
        assert r["N"] == 2
        assert r["tasso"] == pytest.approx(0.4)
        assert r["indici"] == [1, 3]

    def test_uguaglianza_non_supera(self):
        r = es295_superamenti([2000.0, 2000.01], 2000.0)
        assert r["N"] == 1
        assert r["indici"] == [1]


class TestEs295Z1:
    def test_sintetico_valori_noti(self):
        # perdite [50,150,250,30], var=100, es=200, conf=0.9:
        # Y = [0, 7.5, 12.5, 0] -> media 5 -> Z1 = 4
        r = es295_z1([50.0, 150.0, 250.0, 30.0], 100.0, 200.0, 0.9)
        assert r["n"] == 4
        assert r["N"] == 2
        assert r["z1"] == pytest.approx(4.000000000000001)
        assert r["media_y"] == pytest.approx(5.0)
        assert r["s_y"] == pytest.approx(6.123724356957946)

    def test_zero_sotto_h0_costruita(self):
        # 2 superamenti al 5% con perdita = ES -> media(Y) = 1 -> Z1 = 0
        perd = [200.0, 200.0] + [10.0] * 38
        r = es295_z1(perd, 100.0, 200.0, 0.95)
        assert r["N"] == 2
        assert r["z1"] == pytest.approx(0.0, abs=1e-12)

    def test_es_minore_var_ko(self):
        with pytest.raises(ValueError):
            es295_z1([150.0] * 20, 200.0, 100.0, 0.95)


class TestEs295Z2:
    def test_sintetico_valori_noti(self):
        # W = [0.75, 1.25] -> media 1 -> Z2 = 0
        r = es295_z2([50.0, 150.0, 250.0, 30.0], 100.0, 200.0)
        assert r["N"] == 2
        assert r["z2"] == pytest.approx(0.0, abs=1e-12)
        assert r["media_w"] == pytest.approx(1.0)
        assert r["s_w"] == pytest.approx(0.3535533905932738)

    def test_nessun_superamento_ko(self):
        with pytest.raises(ValueError):
            es295_z2([10.0, 20.0, 30.0], 100.0, 200.0)

    def test_singolo_superamento_s_zero(self):
        r = es295_z2([500.0] + [10.0] * 25, 100.0, 200.0)
        assert r["N"] == 1
        assert r["s_w"] == 0.0


class TestEs295NormCdf:
    def test_zero(self):
        assert es295_norm_cdf(0.0) == pytest.approx(0.5)

    def test_valore_noto(self):
        assert es295_norm_cdf(1.6448536269514729) == pytest.approx(0.95)

    def test_simmetria(self):
        assert es295_norm_cdf(-1.2) == pytest.approx(1.0 - es295_norm_cdf(1.2))


class TestEs295Pvalue:
    def test_stat_zero_p_mezo(self):
        r = es295_pvalue_asintotico(0.0, 40, 1.5)
        assert r["z"] == pytest.approx(0.0)
        assert r["p"] == pytest.approx(0.5)

    def test_sintetico(self):
        r = es295_pvalue_asintotico(4.000000000000001, 4, 6.123724356957946)
        assert r["z"] == pytest.approx(1.3063945294843617)
        assert r["p"] == pytest.approx(0.09570921261880372)

    def test_s_nulla_ko(self):
        with pytest.raises(ValueError):
            es295_pvalue_asintotico(1.0, 10, 0.0)

    def test_n_eff_troppo_piccolo_ko(self):
        with pytest.raises(ValueError):
            es295_pvalue_asintotico(1.0, 1, 0.5)


class TestEs295Verdetto:
    def test_coerente(self):
        r = es295_verdetto(0.5, 0.4, 7)
        assert r["verdetto"] == "coda coerente col modello"
        assert r["pmin"] == pytest.approx(0.4)

    def test_zona_gialla(self):
        assert es295_verdetto(0.03, None, 7)["verdetto"].startswith("zona gialla")

    def test_sottostimata_prende_minimo(self):
        r = es295_verdetto(0.5, 0.005, 7)
        assert r["verdetto"].startswith("coda sottostimata")
        assert r["pmin"] == pytest.approx(0.005)

    def test_nessun_superamento(self):
        r = es295_verdetto(None, None, 0)
        assert r["verdetto"] == "nessun superamento: modello conservativo"
        assert r["pmin"] is None

    def test_dati_insufficienti(self):
        assert es295_verdetto(None, None, 7)["verdetto"] == \
            "dati insufficienti per il test"

    def test_p_fuori_range_ko(self):
        with pytest.raises(ValueError):
            es295_verdetto(1.5, None, 7)


class TestEs295Integrazione:
    def test_catena_demo(self):
        pnl = es295_parse_pnl(DEMO_TXT)
        assert len(pnl) == 60
        perd = es295_perdite(pnl)
        sup = es295_superamenti(perd, 2000.0)
        assert sup["N"] == 7
        z1 = es295_z1(perd, 2000.0, 3200.0, 0.975)
        assert z1["z1"] == pytest.approx(3.4166666666666625)
        assert z1["s_y"] == pytest.approx(12.443658335407692)
        z2 = es295_z2(perd, 2000.0, 3200.0)
        assert z2["N"] == 7
        assert z2["z2"] == pytest.approx(-0.0535714285714286)
        r1 = es295_pvalue_asintotico(z1["z1"], z1["n"], z1["s_y"])
        assert r1["p"] == pytest.approx(0.016717638577597338)
        r2 = es295_pvalue_asintotico(z2["z2"], z2["N"], z2["s_w"])
        v = es295_verdetto(r1["p"], r2["p"], z1["N"])
        assert v["verdetto"] == "zona gialla: coda piu' pesante del modello"
