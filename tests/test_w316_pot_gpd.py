"""Test tab316 '🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica POT-GPD: soglia, eccedenze, momenti
pesati in probabilita', stima (xi, beta) della Pareto Generalizzata, VaR/ES di
coda, QQ-plot, confronti con Hill/empirico/normale, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh316_num", "mh316_conf", "mh316_k", "mh316_parse_serie",
           "mh316_norm_ppf", "mh316_perdite", "mh316_soglia",
           "mh316_eccedenze", "mh316_pwm", "mh316_stima", "mh316_hill",
           "mh316_var_gpd", "mh316_es_gpd", "mh316_var_hill",
           "mh316_var_empirico", "mh316_var_normale", "mh316_qq",
           "mh316_risultato", "mh316_verdetto")

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
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
SERIE_DEMO = '-7689 13066 8112 -63229 62852 39916 92196 24157 -9069 986\n-6796 -21240 -45770 -92147 -41405 65384 -249746 -17518 -67249 14967\n67536 20043 -38215 -195168 -30319 -40368 23914 4742 -897 -223481\n-31032 -3617 -6607 54814 -27012 29764 -66225 -258903 -1171 91295\n-57139 -2898 72058 -11675 27543 28342 -297043 -55968 -34426 -63587\n10167 253064 -36629 41993 329157 -92752 -49044 -33433 -22182 9731\n596 -36229 21513 32183 29756 -4331 -17444 12668 -14222 38696\n-6197 64319 -23380 55794 -74553 -23556 46003 8501 91959 -27344\n84011 31131 -71850 -10800 60122 20014 -57979 -14127 -26228 -83049\n-21612 5747 55320 12401 -47501 71536 36926 -72323 -49058 67403\n-24232 -352459 36997 -6063 9064 66434 -22234 44252 -61060 -64021\n-82194 67388 37750 -83448 -66946 -39595 3678 -26929 22239 -44530\n-16531 83110 -29847 -24544 -26872 32082 61709 22204 -21202 13207\n-21291 -67548 19628 61315 15596 47843 25604 -71902 -11348 58829\n-9688 -73248 -264 35737 10802 -68684 -13708 77325 -73463 -87837\n74951 35657 -24316 8134 256845 260928 35922 5358 -44268 59457\n-9750 -38450 37071 44300 -8005 60115 -8831 -54 34491 -64982\n-30951 36466 52359 -1241 41335 56577 1439 -55179 278123 -13374\n21626 -5022 -5668 26555 -23788 32083 5240 86738 -1218 -53702\n22143 27240 -28895 -20704 14206 -641731 80989 24271 55275 -47645\n-76571 82496 -62532 90879 32733 14602 23266 1374 73310 31853\n-47314 17457 30017 -15547 -90575 50574 45809 9943 -30051 46882\n79807 70062 -41899 5484 -10908 15879 -33740 56919 28814 -35468\n52292 42954 -45173 54859 -15658 -38864 24992 84557 -55546 -40903\n-4621 23948 -8369 805164 65154 55048 29350 -29982 1393 -8152\n35452 -4642 51174 1321 60854 -86365 8770 272804 -22471 45833\n3751 32149 7893 14629 73511 -24227 39749 2438 5080 -30937\n-13496 31034 269121 -222554 6059 83384 -61822 -35130 44231 -21991\n-22231 67430 48037 504455 -48391 41817 -66130 -63614 33813 13353\n31161 4704 -10615 17269 -10096 -76538 -17306 -202031 -27894 -60946\n-14546 8057 80104 -60491 17630 -277926 4100 -14294 -457 -70577\n52719 12411 -4991 53889 8238 36992 -57925 69312 -9368 56753\n-40766 58968 14240 84561 20366 15403 -64989 54077 42576 224056\n-68128 -1549 8999 -63716 3024 15645 38593 -36854 19736 -21757\n-3065 -42171 18759 68683 -19885 -14975 -27483 -9242 -44457 -33684\n33204 34045 -7391 -2089 -18703 -33351 40089 18435 2022 93359\n43366 -11025 17247 -13805 25185 -14143 -60018 39621 -85758 -6415\n-9171 -66823 26653 22523 -35972 -16781 22318 48175 11157 46879\n-71206 -8616 -48444 -13749 -41557 -22312 12832 54346 11352 64055\n51972 12823 -43678 39759 17631 44892 11934 -44844 83964 -15675'
K_DEMO = 40
Q_DEMO = 99.0

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_DEMO = 400
XI = 0.6404475862435303
BETA = 23555.024696444874
SOGLIA = 63716.0
VAR_GPD = 187648.71834385575
ES_GPD = 473914.1724984227
VAR_HILL = 192931.25047037363
VAR_EMP = 437.70000000000033
VAR_NOR = 207137.28797868383
RATIO_GH = 0.9726196139109715
RATIO_GE = 428.7153720444497
MAX_STORICO = 641731.0
STATO = "coda pesantissima"
VERDETTO = 'coda pesantissima (xi=0.64): VaR GPD 187,649 euro, ES 473,914 euro: la coda domina il rischio.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _gpd(n=2000, xi=0.4, beta=1000.0):
    """Eccedenze da quantili esatti GPD(xi, beta), crescenti.

    Usa le stesse plotting positions di mh316_qq ((i+1-0.35)/n) cosi' il
    QQ-plot su dati esatti e' quasi la diagonale.
    """
    return [beta / xi * ((1.0 - (i + 1 - 0.35) / n) ** (-xi) - 1.0)
            for i in range(n)]


def _perdite_demo():
    return _F["mh316_perdite"](_F["mh316_parse_serie"](SERIE_DEMO))


def _ris_demo():
    return _F["mh316_risultato"](SERIE_DEMO, K_DEMO, Q_DEMO)


class TestRegistry316:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 623
        assert TITLE316 in titoli
        assert "tab316" in dvars
        assert "    with tab316:" in src

    def test_titoli_allineati_314_315_316(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab314")] == TITLE314
        assert titoli[dvars.index("tab315")] == TITLE315
        assert titoli[dvars.index("tab316")] == TITLE316

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh316_conf"](99.5) == 99.5

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_conf"](97)
        with pytest.raises(ValueError):
            _F["mh316_conf"]("99")

    def test_k_ok(self):
        assert _F["mh316_k"](40, 400) == 40
        assert _F["mh316_k"](10, 20) == 10
        assert _F["mh316_k"](10.0, 400) == 10

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_k"](9, 400)
        with pytest.raises(ValueError):
            _F["mh316_k"](201, 400)
        with pytest.raises(ValueError):
            _F["mh316_k"](10.5, 400)
        with pytest.raises(ValueError):
            _F["mh316_k"](True, 400)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_num"](float("nan"), "x")


class TestParse:
    def test_parse_serie_ok(self):
        txt = "10 -20 30.5" + " 1" * 22
        vals = _F["mh316_parse_serie"](txt)
        assert vals == [10.0, -20.0, 30.5] + [1.0] * 22

    def test_parse_serie_separators(self):
        a = _F["mh316_parse_serie"]("1;2 3\n4" + " 5" * 20)
        b = _F["mh316_parse_serie"]("1 2 3 4" + " 5" * 20)
        assert a == b == [1.0, 2.0, 3.0, 4.0] + [5.0] * 20

    def test_parse_serie_virgola_decimale(self):
        vals = _F["mh316_parse_serie"]("1,5 -2,25" + " 3,5" * 20)
        assert vals == [1.5, -2.25] + [3.5] * 20

    def test_parse_serie_corta_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_parse_serie"]("1 2 3")

    def test_parse_serie_testo_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_parse_serie"](42)

    def test_parse_serie_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_parse_serie"]("1 nan " + "2 " * 25)


class TestPPF:
    def test_ppf_50(self):
        assert abs(_F["mh316_norm_ppf"](0.5)) < 1e-9

    def test_ppf_99(self):
        assert abs(_F["mh316_norm_ppf"](0.99) - 2.326347874) < 1e-6

    def test_ppf_bounds_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_norm_ppf"](0.0)
        with pytest.raises(ValueError):
            _F["mh316_norm_ppf"](1.0)


class TestSogliaEccedenze:
    def test_soglia_e_k_esima(self):
        perd = _perdite_demo()
        assert _F["mh316_soglia"](perd, K_DEMO) == perd[K_DEMO]

    def test_eccedenze_forma(self):
        perd = _perdite_demo()
        ecc = _F["mh316_eccedenze"](perd, K_DEMO)
        assert len(ecc) == K_DEMO
        assert all(y >= 0.0 for y in ecc)
        assert ecc == sorted(ecc, reverse=True)
        assert ecc[0] == perd[0] - perd[K_DEMO]


class TestPWM:
    def test_pwm_su_gpd_esatta(self):
        b0, b1 = _F["mh316_pwm"](_gpd())
        assert abs(b0 - 1000.0 / 0.6) < 5.0
        assert abs(b1 - 1000.0 / 0.6 * 2.6 / 3.2) < 5.0

    def test_pwm_corta_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_pwm"]([1.0] * 9)


class TestStima:
    def test_stima_recupera_xi_beta(self):
        xi, beta = _F["mh316_stima"](_gpd())
        assert abs(xi - 0.4) < 0.03
        assert abs(beta - 1000.0) < 60.0

    def test_stima_demo_coerente(self):
        perd = _perdite_demo()
        xi, beta = _F["mh316_stima"](_F["mh316_eccedenze"](perd, K_DEMO))
        assert xi == XI
        assert beta == BETA


class TestHill:
    def test_hill_su_pareto_nota(self):
        xs = [((1.0 - i / 2001) ** (-0.45)) for i in range(2000, 0, -1)]
        assert abs(_F["mh316_hill"](xs, 200) - 0.45) < 0.03

    def test_hill_demo_coerente(self):
        perd = _perdite_demo()
        assert _F["mh316_hill"](perd, K_DEMO) > 0.0


class TestVaRGPD:
    def test_var_gpd_formula(self):
        v = _F["mh316_var_gpd"](100.0, 0.4, 50.0, 40, 400, 99.0)
        assert abs(v - (100.0 + 125.0 * (10.0 ** 0.4 - 1.0))) < 1e-6

    def test_var_gpd_ramo_esponenziale(self):
        v = _F["mh316_var_gpd"](100.0, 0.0, 50.0, 40, 400, 99.0)
        assert abs(v - (100.0 + 50.0 * math.log(10.0))) < 1e-6

    def test_var_gpd_cresce_con_q(self):
        a = _F["mh316_var_gpd"](100.0, 0.4, 50.0, 40, 400, 99.0)
        b = _F["mh316_var_gpd"](100.0, 0.4, 50.0, 40, 400, 99.9)
        assert b > a

    def test_var_gpd_beta_ko(self):
        with pytest.raises(ValueError):
            _F["mh316_var_gpd"](100.0, 0.4, -5.0, 40, 400, 99.0)


class TestES:
    def test_es_gpd_formula(self):
        v = _F["mh316_var_gpd"](100.0, 0.4, 50.0, 40, 400, 99.0)
        es = _F["mh316_es_gpd"](100.0, 0.4, 50.0, v, 99.0)
        assert abs(es - (v + 50.0 - 0.4 * 100.0) / 0.6) < 1e-6

    def test_es_none_se_xi_ge_1(self):
        assert _F["mh316_es_gpd"](100.0, 1.2, 50.0, 500.0, 99.0) is None

    def test_es_demo_coerente(self):
        assert _F["mh316_es_gpd"](
            SOGLIA, XI, BETA, VAR_GPD, Q_DEMO) == ES_GPD


class TestQQ:
    def test_qq_lunghezza_e_monotonia(self):
        perd = _perdite_demo()
        ecc = _F["mh316_eccedenze"](perd, K_DEMO)
        pts = _F["mh316_qq"](ecc, XI, BETA)
        assert len(pts) == K_DEMO
        ts = [p[0] for p in pts]
        assert all(b >= a for a, b in zip(ts, ts[1:]))
        assert all(p[0] >= 0.0 and p[1] >= 0.0 for p in pts)

    def test_qq_fit_buono_su_gpd_esatta(self):
        ecc = _gpd(n=200)
        xi, beta = _F["mh316_stima"](ecc)
        pts = _F["mh316_qq"](ecc, xi, beta, m=0)
        ts = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        mt, my = sum(ts) / len(ts), sum(ys) / len(ys)
        cov = sum((t - mt) * (y - my) for t, y in pts)
        var = sum((t - mt) ** 2 for t in ts)
        slope = cov / var
        assert 0.9 < slope < 1.1


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N_DEMO == 400
        assert ris["k"] == K_DEMO
        assert ris["xi"] == XI
        assert ris["beta"] == BETA
        assert ris["u"] == SOGLIA
        assert ris["var_gpd"] == VAR_GPD
        assert ris["es_gpd"] == ES_GPD
        assert ris["var_hill"] == VAR_HILL
        assert ris["var_empirico"] == VAR_EMP
        assert ris["var_normale"] == VAR_NOR
        assert ris["max_storico"] == MAX_STORICO
        assert ris["ratio_gpd_hill"] == RATIO_GH
        assert ris["ratio_gpd_emp"] == RATIO_GE

    def test_risultato_ordinamento(self):
        ris = _ris_demo()
        assert ris["var_gpd"] > 0.0
        assert ris["var_empirico"] > 0.0
        assert ris["max_storico"] >= ris["var_empirico"]


class TestVerdetto:
    def test_verdetto_demo(self):
        assert _F["mh316_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def _base(self, **kw):
        ris = _ris_demo()
        ris.update(kw)
        return ris

    def test_stato_pesantissima(self):
        v = _F["mh316_verdetto"](self._base(xi=0.7))
        assert v.startswith("coda pesantissima")

    def test_stato_pesante(self):
        v = _F["mh316_verdetto"](self._base(xi=0.3))
        assert v.startswith("coda pesante") and not v.startswith(
            "coda pesantissima")

    def test_stato_moderata(self):
        v = _F["mh316_verdetto"](self._base(xi=0.1))
        assert v.startswith("coda moderata")

    def test_stato_esponenziale(self):
        v = _F["mh316_verdetto"](self._base(xi=-0.1))
        assert v.startswith("coda esponenziale")

    def test_stato_es_non_finito(self):
        v = _F["mh316_verdetto"](
            self._base(xi=1.2, es_gpd=None, var_gpd=999999.0))
        assert "non finito" in v

    def test_warning_divergenza(self):
        v = _F["mh316_verdetto"](self._base(ratio_gpd_hill=2.0))
        assert "divergono" in v
