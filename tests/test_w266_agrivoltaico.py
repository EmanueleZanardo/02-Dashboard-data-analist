"""Test tab266 'Agrivoltaico: doppio reddito': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab266.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("av266_num", "av266_int", "av266_ler", "av266_produzione_annua",
          "av266_fattore_rendita", "av266_npv_solo_agri",
          "av266_npv_agrivoltaico", "av266_npv_fv_terra",
          "av266_confronto", "av266_anno_pareggio",
          "av266_sensibilita_prezzo")
av266_num = _F["av266_num"]
av266_int = _F["av266_int"]
av266_ler = _F["av266_ler"]
av266_produzione_annua = _F["av266_produzione_annua"]
av266_fattore_rendita = _F["av266_fattore_rendita"]
av266_npv_solo_agri = _F["av266_npv_solo_agri"]
av266_npv_agrivoltaico = _F["av266_npv_agrivoltaico"]
av266_npv_fv_terra = _F["av266_npv_fv_terra"]
av266_confronto = _F["av266_confronto"]
av266_anno_pareggio = _F["av266_anno_pareggio"]
av266_sensibilita_prezzo = _F["av266_sensibilita_prezzo"]

APP = Path(__file__).parent.parent / "app.py"

TITLE266 = "\U0001F33E\uFE0F Agrivoltaico: doppio reddito"
TITLE267 = "🟢 Biometano: business case"
TITLE268 = "🌬️ Eolico onshore: business case"
TITLE269 = "🌊 Idroelettrico run-of-river: business case"
TITLE270 = "🔥 Geotermia profonda: business case"
TITLE271 = "☀️ Solare termodinamico (CSP): business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
TITLE276 = "💧 Cash flow at risk (CFaR)"
TITLE277 = "⚡ Aste MI: scostamenti vs MGP"
TITLE278 = "🌡️ Stress climatico: domanda e prezzo"
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE284 = "🏭 Unit commitment CCGT: accendere o no?"
TITLE285 = "🛛️ Differenziali greggio: sweet vs sour"
TITLE286 = "⛽ Basis gas TTF–PSV"
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
TITLE265 = "\U0000267B\uFE0F Fine vita FV: revamping vs dismissione"

HA = 10.0
MARGINE_HA = 1200.0
PERDITA = 25.0
KWP = 1000.0
RESA = 1100.0
DEGRADO = 0.5
PREZZO = 0.10
CAPEX_AGRIV = 945000.0
CAPEX_FV = 700000.0
OEM = 12000.0
ANNI = 25
TASSO = 5.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab266:
    def test_tab266_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 641
        assert TITLE266 in titoli
        assert "tab266" in dvars
        assert "tab266" in withs
        assert titoli[dvars.index("tab266")] == TITLE266
        assert TITLE482 in titoli
        keys = re.findall(r'key="(av266_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_265_266(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab265")] == TITLE265
        assert titoli[dvars.index("tab266")] == TITLE266
        assert titoli[dvars.index("tab267")] == TITLE267
        assert titoli[dvars.index("tab268")] == TITLE268
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[dvars.index("tab274")] == TITLE274
        assert titoli[dvars.index("tab275")] == TITLE275
        assert titoli[dvars.index("tab276")] == TITLE276
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestAv266Num:
    def test_ok(self):
        assert av266_num(3, "x") == 3.0
        assert av266_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                av266_num(bad, "x")

    def test_int(self):
        assert av266_int(25, "anni") == 25
        assert av266_int(25.0, "anni") == 25
        for bad in (0, -3, 2.5, "25"):
            with pytest.raises(ValueError):
                av266_int(bad, "anni")


class TestAv266Ler:
    def test_perdita_zero(self):
        assert av266_ler(0.0) == pytest.approx(2.0)

    def test_perdita_25(self):
        assert av266_ler(25.0) == pytest.approx(1.75)

    def test_perdita_totale(self):
        assert av266_ler(100.0) == pytest.approx(1.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_ler(-0.1)
        with pytest.raises(ValueError):
            av266_ler(100.1)


class TestAv266ProduzioneAnnua:
    def test_anno1_e_anno2(self):
        assert av266_produzione_annua(KWP, RESA, DEGRADO, 1) == pytest.approx(KWP * RESA)
        assert av266_produzione_annua(KWP, RESA, DEGRADO, 2) == pytest.approx(KWP * RESA * 0.995)

    def test_degrado_nullo(self):
        assert av266_produzione_annua(KWP, RESA, 0.0, 9) == pytest.approx(KWP * RESA)

    def test_monotonia(self):
        prods = [av266_produzione_annua(KWP, RESA, DEGRADO, a) for a in range(1, 11)]
        assert all(b < a for a, b in zip(prods, prods[1:]))

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_produzione_annua(-1.0, RESA, DEGRADO, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, -10.0, DEGRADO, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, RESA, 51.0, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, RESA, DEGRADO, 0)


class TestAv266FattoreRendita:
    def test_tasso_zero(self):
        assert av266_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert av266_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert av266_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            av266_fattore_rendita(5.0, 0)


class TestAv266NpvSoloAgri:
    def test_base(self):
        r = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, TASSO)
        assert r["reddito_annuo"] == pytest.approx(HA * MARGINE_HA)
        assert r["npv"] == pytest.approx(HA * MARGINE_HA * av266_fattore_rendita(TASSO, ANNI))

    def test_tasso_zero(self):
        r = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, 0.0)
        assert r["npv"] == pytest.approx(HA * MARGINE_HA * ANNI)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_solo_agri(0.0, MARGINE_HA, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_solo_agri(HA, MARGINE_HA, ANNI, -1.0)


class TestAv266NpvAgrivoltaico:
    def test_chiavi_e_coerenza(self):
        r = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)
        assert set(r) == {"npv", "capex", "margine_agri_residuo", "produzioni",
                          "flussi_attualizzati", "produzione_totale_kwh"}
        assert len(r["produzioni"]) == len(r["flussi_attualizzati"]) == ANNI
        assert r["capex"] == pytest.approx(CAPEX_AGRIV)
        assert r["margine_agri_residuo"] == pytest.approx(HA * MARGINE_HA * 0.75)
        assert r["produzione_totale_kwh"] == pytest.approx(sum(r["produzioni"]))
        assert r["npv"] == pytest.approx(sum(r["flussi_attualizzati"]) - CAPEX_AGRIV)
        assert r["produzioni"][0] == pytest.approx(KWP * RESA)

    def test_capex_zero_perdita_zero_scomposizione(self):
        # senza capex e senza perdita agricola: agri + FV separati
        r = av266_npv_agrivoltaico(HA, MARGINE_HA, 0.0, KWP, RESA, DEGRADO,
                                  PREZZO, 0.0, OEM, ANNI, TASSO)
        a = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, TASSO)["npv"]
        f = av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, 0.0, OEM, ANNI, TASSO)["npv"]
        assert r["npv"] == pytest.approx(a + f)

    def test_prezzo_alto_aumenta_npv(self):
        r1 = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.05, CAPEX_AGRIV, OEM, ANNI, TASSO)
        r2 = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.20, CAPEX_AGRIV, OEM, ANNI, TASSO)
        assert r2["npv"] > r1["npv"]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, 101.0, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  -0.1, CAPEX_AGRIV, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, -1.0, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(0.0, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)


class TestAv266NpvFvTerra:
    def test_base(self):
        r = av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, CAPEX_FV, OEM, ANNI, TASSO)
        atteso = (sum(av266_produzione_annua(KWP, RESA, DEGRADO, a) * PREZZO
                      / 1.05 ** a for a in range(1, ANNI + 1))
                  - sum(OEM / 1.05 ** a for a in range(1, ANNI + 1)) - CAPEX_FV)
        assert r["npv"] == pytest.approx(atteso)
        assert r["produzione_totale_kwh"] == pytest.approx(sum(r["produzioni"]))

    def test_prezzo_zero_negativo(self):
        r = av266_npv_fv_terra(KWP, RESA, DEGRADO, 0.0, CAPEX_FV, OEM, ANNI, TASSO)
        assert r["npv"] < 0

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, -5.0, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, CAPEX_FV, -1.0, ANNI, TASSO)


class TestAv266Confronto:
    def test_vince_agrivoltaico(self):
        r = av266_confronto(100.0, 150.0, 120.0)
        assert r["verdetto"] == "agrivoltaico"
        assert r["migliore"] == "agrivoltaico"
        assert r["secondo"] == "fv_terra"
        assert r["margine_pct"] == pytest.approx(20.0)

    def test_vince_solo_agri(self):
        r = av266_confronto(200.0, 100.0, -50.0)
        assert r["verdetto"] == "solo_agri"
        assert r["margine_pct"] == pytest.approx(50.0)

    def test_vince_fv_terra(self):
        r = av266_confronto(50.0, 80.0, 120.0)
        assert r["verdetto"] == "fv_terra"
        assert r["secondo"] == "agrivoltaico"

    def test_indifferente(self):
        r = av266_confronto(100.0, 103.0, 90.0)
        assert r["verdetto"] == "indifferente"
        assert r["migliore"] == "agrivoltaico"
        assert r["margine_pct"] == pytest.approx(3.0 / 103.0 * 100.0)

    def test_migliore_zero(self):
        r = av266_confronto(0.0, -10.0, -20.0)
        assert r["verdetto"] == "solo_agri"
        assert r["margine_pct"] is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_confronto("100", 150.0, 120.0)


class TestAv266Pareggio:
    def test_capex_zero_pareggio_anno1(self):
        a = av266_anno_pareggio(HA, MARGINE_HA, 0.0, KWP, RESA, DEGRADO,
                                PREZZO, 0.0, OEM, ANNI, TASSO)
        assert a == 1

    def test_capex_enorme_mai(self):
        a = av266_anno_pareggio(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                PREZZO, 1e12, OEM, ANNI, TASSO)
        assert a is None

    def test_pareggio_intermedio(self):
        # prezzo alto + perdita contenuta: pareggia entro l'orizzonte
        a = av266_anno_pareggio(HA, MARGINE_HA, 10.0, KWP, RESA, DEGRADO,
                                0.30, 200000.0, OEM, ANNI, TASSO)
        assert a is not None and 1 <= a <= ANNI

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_anno_pareggio(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                PREZZO, -1.0, OEM, ANNI, TASSO)


class TestAv266Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                         CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                         0.2, 0.1)
        assert len(righe) == 3
        assert righe[0]["prezzo_kwh"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_kwh"] == pytest.approx(0.2)
        assert set(righe[0]) == {"prezzo_kwh", "npv_agri", "npv_agrivoltaico", "npv_fv"}

    def test_monotonia_e_coerenza(self):
        righe = av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                         CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                         0.2, 0.1)
        nv = [r["npv_agrivoltaico"] for r in righe]
        nf = [r["npv_fv"] for r in righe]
        na = [r["npv_agri"] for r in righe]
        assert all(b > a for a, b in zip(nv, nv[1:]))
        assert all(b > a for a, b in zip(nf, nf[1:]))
        assert all(x == na[0] for x in na)
        assert righe[1]["npv_agrivoltaico"] == pytest.approx(
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.1, CAPEX_AGRIV, OEM, ANNI, TASSO)["npv"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                     CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                     0.0, 0.1)
        with pytest.raises(ValueError):
            av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                     CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                     0.2, 0.0)
