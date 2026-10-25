"""Test tab319 '🎛📉 FHS: il VaR con la volatilita' di oggi': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica FHS: validatori, vol EWMA
RiskMetrics, shock standardizzati, bootstrap deterministico, VaR/ES FHS vs
simulazione storica vs EWMA-normale, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh319_num", "mh319_conf", "mh319_lambda", "mh319_nboot",
           "mh319_parse_pnl", "mh319_ewma_vol", "mh319_standardized",
           "mh319_norm_ppf", "mh319_rng", "mh319_quantile", "mh319_fhs",
           "mh319_risultato", "mh319_verdetto")

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
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
SERIE_DEMO = '1024.72\n-759.19\n-849.85\n1183.27\n368.60\n-471.35\n-123.13\n-604.63\n981.92\n850.78\n763.68\n-499.95\n181.57\n1836.79\n-1400.38\n-275.02\n-505.12\n-1052.98\n-887.58\n759.35\n-208.11\n124.02\n-1031.46\n1345.68\n-1289.15\n334.99\n-498.60\n724.58\n931.28\n1392.21\n832.94\n854.02\n974.72\n148.76\n-753.86\n-632.27\n875.68\n-49.22\n253.14\n-207.79\n-1626.33\n907.24\n-261.39\n807.62\n-299.56\n-293.48\n353.75\n-1496.63\n545.26\n-615.50\n759.07\n-125.14\n1135.15\n530.43\n57.32\n402.82\n-1235.72\n563.76\n-181.15\n373.39\n-160.45\n-1340.78\n-524.18\n467.99\n-114.19\n-446.92\n-558.35\n-806.41\n-1089.67\n-549.43\n986.01\n182.54\n-1115.77\n362.22\n1419.56\n1209.24\n-9.24\n311.67\n-206.63\n354.37\n-225.32\n-143.45\n-1183.92\n1041.87\n-346.70\n691.57\n1619.52\n-859.40\n-514.12\n1910.09\n57.32\n793.15\n291.00\n-438.24\n-1100.66\n-70.11\n-165.44\n-651.89\n1512.68\n307.99\n-1173.64\n97.06\n414.09\n-544.86\n804.19\n-267.62\n1085.25\n266.50\n32.22\n-1140.49\n1950.97\n-222.43\n462.56\n-1747.28\n964.66\n-579.45\n842.89\n-1139.98\n618.56\n1345.16\n-386.19\n-69.68\n1030.50\n1144.34\n-941.29\n-591.52\n-382.02\n-502.03\n-1022.11\n651.44\n40.23\n1197.60\n-476.35\n-373.98\n-699.11\n125.35\n-41.40\n-965.09\n781.66\n107.01\n248.53\n1823.39\n432.47\n-533.15\n746.49\n-1714.14\n571.21\n-265.82\n154.43\n486.33\n-219.21\n512.56\n152.39\n485.58\n-118.73\n-3.82\n355.11\n445.28\n8.53\n-358.30\n-952.04\n-472.32\n-532.64\n-188.77\n1026.24\n374.51\n737.64\n939.06\n-33.38\n254.50\n645.80\n-568.82\n-352.31\n927.51\n215.70\n-334.74\n-922.04\n1364.92\n57.10\n171.17\n-649.28\n950.28\n-970.37\n289.33\n858.54\n448.51\n-78.40\n130.89\n122.87\n1506.66\n-37.63\n-298.46\n1272.04\n1173.65\n731.13\n2344.31\n-129.02\n107.95\n-94.44\n-24.68\n5140.89\n-791.80\n-3513.54\n653.82\n-737.34\n-1093.80\n2188.86\n-2284.73\n-132.35\n979.76\n-4668.48\n-24.88\n-213.85\n-2700.36\n-5929.24\n-1146.93\n758.99\n2564.71\n-1989.53\n708.71\n552.79\n-878.86\n652.38\n-1170.93\n-1546.00\n1660.90\n-2109.15\n-993.97\n1610.65\n-276.69\n-1320.94\n-1646.93\n4518.56\n-1238.86\n2588.61\n-544.41\n-114.99\n146.04\n-452.13\n-3115.50\n-2877.36\n-2131.26\n-1349.76\n611.26\n-218.00\n73.69\n831.15\n4014.55\n-2782.39\n3146.73\n-1514.27\n2500.55\n-297.72\n1187.75\n1033.16\n-6292.74\n-1535.94\n-325.09\n-3679.67\n-843.45'
Q_DEMO = 99.0
LAM_DEMO = 0.94
NBOOT_DEMO = 5000

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 260
SIG_NOW = 2364.648239067609
SIG_AVG = 1081.5765625243384
VAR_FHS = 7056.526025393739
ES_FHS = 7579.983051581226
VAR_HS = 4085.0821000000246
ES_HS = 5630.153333333333
VAR_N = 5500.994403809351
GAP = 0.7273890347010886
VOL_RATIO = 2.1862975964906766
STATO = "FHS molto prudente"
VERDETTO = "FHS molto prudente: il VaR con la volatilita' di oggi supera del 72.7% quello storico (7,057 vs 4,085 euro): la serie e' in regime stressato, usa il VaR FHS per il limite."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _r_demo():
    return _F["mh319_parse_pnl"](SERIE_DEMO)


def _ris_demo():
    return _F["mh319_risultato"](SERIE_DEMO, LAM_DEMO, Q_DEMO, NBOOT_DEMO)


class TestRegistry319:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 716
        assert TITLE319 in titoli
        assert "tab319" in dvars
        assert "    with tab319:" in src

    def test_titoli_allineati_317_318_319(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab317")] == TITLE317
        assert titoli[dvars.index("tab318")] == TITLE318
        assert titoli[dvars.index("tab319")] == TITLE319

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh319_conf"](99.0) == pytest.approx(0.01)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh319_conf"](97.5)

    def test_lambda_ok(self):
        assert _F["mh319_lambda"](0.94) == 0.94
        assert _F["mh319_lambda"](0.90) == 0.90
        assert _F["mh319_lambda"](0.99) == 0.99

    def test_lambda_ko(self):
        for bad in (0.89, 1.0, 0.5):
            with pytest.raises(ValueError):
                _F["mh319_lambda"](bad)

    def test_nboot_ko(self):
        for bad in (999, 20001, 5000.5):
            with pytest.raises(ValueError):
                _F["mh319_nboot"](bad)

    def test_parse_pnl_ok(self):
        r = _r_demo()
        assert len(r) == N == 260
        assert all(isinstance(v, float) for v in r)

    def test_parse_pnl_ko(self):
        with pytest.raises(ValueError):
            _F["mh319_parse_pnl"]("1.5\n2.5\n3.5")
        with pytest.raises(ValueError):
            _F["mh319_parse_pnl"]("a\nb\nc")
        with pytest.raises(ValueError):
            _F["mh319_parse_pnl"](";" .join(["1.0"] * 59))

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x"):
            with pytest.raises(ValueError):
                _F["mh319_num"](bad, "t")


class TestEwma:
    def test_lunghezze_e_positivita(self):
        ew = _F["mh319_ewma_vol"](_r_demo(), LAM_DEMO)
        assert len(ew["vols"]) == N
        assert all(v > 0.0 for v in ew["vols"])
        assert ew["sig_now"] > 0.0
        assert ew["sig_avg"] > 0.0

    def test_shock_alza_vol(self):
        r = [100.0] * 130 + [800.0] * 130
        ew = _F["mh319_ewma_vol"](r, 0.94)
        assert ew["vols"][-1] > ew["vols"][0]
        assert ew["sig_now"] > ew["sig_avg"]

    def test_lambda_piu_basso_piu_reattivo(self):
        r = _r_demo()
        s90 = _F["mh319_ewma_vol"](r, 0.90)["sig_now"]
        s94 = _F["mh319_ewma_vol"](r, 0.94)["sig_now"]
        s99 = _F["mh319_ewma_vol"](r, 0.99)["sig_now"]
        assert s90 > s94 > s99

    def test_demo_stressato(self):
        assert SIG_NOW > SIG_AVG
        assert VOL_RATIO > 1.5


class TestStandardized:
    def test_z_finite(self):
        z = _F["mh319_standardized"](_r_demo(), LAM_DEMO)
        assert len(z) == N
        assert all(math.isfinite(v) for v in z)


class TestFhs:
    def test_determinismo(self):
        r = _r_demo()
        f1 = _F["mh319_fhs"](r, LAM_DEMO, Q_DEMO, 2000)
        f2 = _F["mh319_fhs"](r, LAM_DEMO, Q_DEMO, 2000)
        assert f1["perd_fhs"] == f2["perd_fhs"]
        assert f1["var_fhs"] == f2["var_fhs"]

    def test_lunghezze(self):
        f = _F["mh319_fhs"](_r_demo(), LAM_DEMO, Q_DEMO, 2000)
        assert len(f["perd_fhs"]) == 2000
        assert len(f["perd_hs"]) == N

    def test_norm_ppf_noto(self):
        assert _F["mh319_norm_ppf"](0.975) == pytest.approx(1.959964, abs=1e-6)

    def test_quantile(self):
        assert _F["mh319_quantile"]([1.0, 2.0, 3.0, 4.0], 0.5) == 2.5

    def test_fhs_supera_storica_su_demo(self):
        assert VAR_FHS > VAR_HS > 0.0
        assert ES_FHS >= VAR_FHS
        assert GAP > 0.15


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N == 260
        assert ris["lam"] == LAM_DEMO
        assert ris["q"] == Q_DEMO
        assert ris["nboot"] == NBOOT_DEMO
        assert ris["sig_now"] == SIG_NOW
        assert ris["sig_avg"] == SIG_AVG
        assert ris["var_fhs"] == VAR_FHS
        assert ris["es_fhs"] == ES_FHS
        assert ris["var_hs"] == VAR_HS
        assert ris["es_hs"] == ES_HS
        assert ris["var_n"] == VAR_N
        assert ris["gap"] == GAP
        assert ris["vol_ratio"] == VOL_RATIO
        assert ris["gap"] == pytest.approx(
            (ris["var_fhs"] - ris["var_hs"]) / ris["var_hs"])

    def test_lunghezze_scenari(self):
        ris = _ris_demo()
        assert len(ris["perd_fhs"]) == NBOOT_DEMO
        assert len(ris["perd_hs"]) == N


class TestVerdetto:
    def _base(self, **kw):
        return {"gap": 0.0, "vol_ratio": 1.0, "var_fhs": 100000.0,
                "var_hs": 90000.0, **kw}

    def test_verdetto_demo(self):
        assert _F["mh319_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_molto_prudente(self):
        v = _F["mh319_verdetto"](self._base(gap=0.50, var_fhs=135000.0,
                                            var_hs=90000.0))
        assert v.startswith("FHS molto prudente")

    def test_stato_prudente(self):
        v = _F["mh319_verdetto"](self._base(gap=0.20, vol_ratio=1.2,
                                            var_fhs=108000.0, var_hs=90000.0))
        assert v.startswith("FHS prudente")

    def test_stato_vol_alta(self):
        v = _F["mh319_verdetto"](self._base(gap=0.05, vol_ratio=1.8))
        assert v.startswith("volatilita' corrente alta")

    def test_stato_clemente(self):
        v = _F["mh319_verdetto"](self._base(gap=-0.15, vol_ratio=0.9))
        assert v.startswith("FHS piu' clemente")

    def test_stato_concordano(self):
        v = _F["mh319_verdetto"](self._base(gap=0.02, vol_ratio=1.1))
        assert v.startswith("FHS e storica concordano")
