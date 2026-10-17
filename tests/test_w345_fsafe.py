"""Test tab345 '🎯 Sizing anti-rovina: f massima con ROR vincolato': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del sizing vincolato dal rischio
di rovina: validatori, Kelly pieno f* = (p*(b+1)-1)/b, coefficiente di
Lundberg theta (radice di p*(1+f*b)^(-theta) + q*(1-f)^(-theta) = 1 via
bisezione), R = barriera^theta (Cramer-Lundberg), edge per trade
e = f*(p*b-q), f_safe = unica f con R(f) = Rmax (bisezione, R monotono
crescente in f), misure (f_rec = min(half-Kelly, f_safe)) e verdetto a
3 stati (SIZING BLOCCATO / VINCOLO ROVINA ATTIVO / HALF-KELLY ENTRO RMAX).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh345_num", "mh345_kelly", "mh345_theta", "mh345_ror",
           "mh345_edge", "mh345_f_safe", "mh345_misure", "mh345_verdetto")

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
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
BAR = 0.5
RMAX = 0.05
B = 1.2
F_STAR = 0.17500000000000016
F_HALF = 0.08750000000000008
F_SAFE = 0.06588426159267208
F_REC = 0.06588426159267208
THETA = 4.321928094887394
EDGE = 0.013835694934461141
ROR = 0.04999999999999891
VERDETTO = 'VINCOLO ROVINA ATTIVO (f_safe = 6.59% < half-Kelly 8.75%): half-Kelly ha ROR oltre il limite 5%: tagliare la frazione a 6.59% (ROR = 5% al limite).'

_M = None


def _misure():
    global _M
    if _M is None:
        _M = _F["mh345_misure"](P, WIN, LOSS, BAR, RMAX)
    return _M


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry345:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 523
        assert "tab345" in dvars
        assert "tab345" in withs

    def test_titoli_allineati_342_343_344_345(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab342")] == TITLE342
        assert titoli[dvars.index("tab343")] == TITLE343
        assert titoli[dvars.index("tab344")] == TITLE344
        assert titoli[dvars.index("tab345")] == TITLE345

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh345_num"](1.5, "x") == 1.5
        assert _F["mh345_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh345_num"](bad, "x")


class TestKelly:
    def test_demo(self):
        assert _F["mh345_kelly"](P, B) == pytest.approx(F_STAR, rel=1e-9)
        assert _F["mh345_kelly"](P, B) == pytest.approx(0.175, rel=1e-9)

    def test_formula(self):
        assert _F["mh345_kelly"](0.6, 2.0) == pytest.approx(
            max(0.0, (0.6 * 3.0 - 1.0) / 2.0), rel=1e-9)

    def test_nessun_edge_zero(self):
        assert _F["mh345_kelly"](0.4, 1.0) == 0.0

    def test_ko_p_bordi(self):
        for p in (0.0, 1.0):
            with pytest.raises(ValueError):
                _F["mh345_kelly"](p, B)

    def test_ko_b(self):
        with pytest.raises(ValueError):
            _F["mh345_kelly"](P, 0.0)


class TestTheta:
    def test_demo_radice(self):
        th = _F["mh345_theta"](P, B, F_REC)
        assert th == pytest.approx(THETA, rel=1e-9)
        assert th > 0
        up, down = 1.0 + F_REC * B, 1.0 - F_REC
        assert P * up ** (-th) + (1.0 - P) * down ** (-th) == pytest.approx(
            1.0, rel=1e-9)

    def test_nessun_edge_zero(self):
        # drift logaritmico <= 0: nessuna radice positiva
        assert _F["mh345_theta"](0.4, 1.0, 0.05) == 0.0

    def test_ko_f(self):
        with pytest.raises(ValueError):
            _F["mh345_theta"](P, B, 1.0)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh345_theta"](1.0, B, 0.05)


class TestRor:
    def test_demo(self):
        r = _F["mh345_ror"](P, B, F_REC, BAR)
        assert r == pytest.approx(ROR, rel=1e-9)
        assert r == pytest.approx(BAR ** THETA, rel=1e-9)

    def test_nessun_edge_uno(self):
        assert _F["mh345_ror"](0.4, 1.0, 0.05, 0.5) == 1.0

    def test_monotonia_f(self):
        # a parita' di edge, piu' f -> piu' rischio di rovina
        r1 = _F["mh345_ror"](P, B, 0.02, BAR)
        r2 = _F["mh345_ror"](P, B, 0.15, BAR)
        assert r1 < r2

    def test_range(self):
        for p, b, f in ((0.55, 1.2, 0.0875), (0.6, 2.0, 0.05),
                        (0.51, 1.1, 0.02)):
            r = _F["mh345_ror"](p, b, f, 0.5)
            assert 0.0 <= r <= 1.0

    def test_ko_barriera(self):
        with pytest.raises(ValueError):
            _F["mh345_ror"](P, B, 0.05, 1.0)


class TestEdge:
    def test_demo(self):
        e = _F["mh345_edge"](P, B, F_REC)
        assert e == pytest.approx(EDGE, rel=1e-9)
        assert e == pytest.approx(F_REC * (0.55 * 1.2 - 0.45), rel=1e-9)

    def test_formula(self):
        assert _F["mh345_edge"](0.6, 2.0, 0.1) == pytest.approx(
            0.1 * (0.6 * 2.0 - 0.4), rel=1e-9)

    def test_zero_f(self):
        assert _F["mh345_edge"](P, B, 0.0) == 0.0

    def test_negativo(self):
        assert _F["mh345_edge"](0.4, 1.0, 0.05) < 0.0

    def test_ko_f_uno(self):
        with pytest.raises(ValueError):
            _F["mh345_edge"](P, B, 1.0)


class TestFSafe:
    def test_demo_al_limite(self):
        fs = _F["mh345_f_safe"](P, B, BAR, RMAX)
        assert fs == pytest.approx(F_SAFE, rel=1e-9)
        # f_safe tocca il vincolo: R(f_safe) == Rmax
        assert _F["mh345_ror"](P, B, fs, BAR) == pytest.approx(
            RMAX, rel=1e-6)
        assert 0.0 < fs < F_HALF  # vincolo attivo nella demo

    def test_monotonia_rmax(self):
        # vincolo piu' severo -> f_safe piu' piccola
        assert _F["mh345_f_safe"](P, B, BAR, 0.02) < \
            _F["mh345_f_safe"](P, B, BAR, 0.10)

    def test_rmax_largo_ritorna_hi(self):
        # edge fortissimo (drift > 0 anche a f=0.99): R(0.99) <= Rmax
        assert _F["mh345_f_safe"](0.99, 12.0, 0.5, 0.99) == 0.99

    def test_nessun_edge_zero(self):
        assert _F["mh345_f_safe"](0.4, 1.0, 0.5, 0.05) == 0.0

    def test_barriera_severa_piu_piccola(self):
        # barriera piu' profonda (20% = drawdown 80%, tolleranza maggiore)
        # -> R piu' basso a parita' di theta -> f_safe piu' alta
        assert _F["mh345_f_safe"](P, B, 0.2, RMAX) > \
            _F["mh345_f_safe"](P, B, 0.8, RMAX)

    def test_ko_rmax(self):
        for rm in (0.0, 1.0, 1.5):
            with pytest.raises(ValueError):
                _F["mh345_f_safe"](P, B, BAR, rm)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh345_f_safe"](1.0, B, BAR, RMAX)


class TestMisure:
    def test_demo(self):
        m = _misure()
        assert m["p"] == pytest.approx(P)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f_star"] == pytest.approx(F_STAR, rel=1e-9)
        assert m["f_half"] == pytest.approx(F_HALF, rel=1e-9)
        assert m["f_safe"] == pytest.approx(F_SAFE, rel=1e-9)
        assert m["f_rec"] == pytest.approx(F_REC, rel=1e-9)
        assert m["vincolo_attivo"] is True
        assert m["barriera"] == pytest.approx(BAR)
        assert m["rmax"] == pytest.approx(RMAX)
        assert m["theta"] == pytest.approx(THETA, rel=1e-9)
        assert m["edge"] == pytest.approx(EDGE, rel=1e-9)
        assert m["ror"] == pytest.approx(ROR, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_relazioni(self):
        m = _misure()
        assert m["f_half"] == pytest.approx(m["f_star"] / 2.0, rel=1e-9)
        assert m["f_rec"] == pytest.approx(
            min(m["f_half"], m["f_safe"]), rel=1e-9)
        assert m["ror"] == pytest.approx(m["barriera"] ** THETA, rel=1e-9)

    def test_vincolo_non_attivo(self):
        m = _F["mh345_misure"](0.7, 300.0, 100.0, 0.5, 0.30)
        assert m["vincolo_attivo"] is False
        assert m["f_rec"] == pytest.approx(m["f_half"], rel=1e-12)

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh345_misure"](P, 0.0, LOSS, BAR, RMAX)

    def test_ko_rmax(self):
        with pytest.raises(ValueError):
            _F["mh345_misure"](P, WIN, LOSS, BAR, 1.0)


class TestVerdetto:
    def test_bloccato(self):
        v = _F["mh345_verdetto"](0.0, 0.0, 1.0, 0.05)
        assert v.startswith("SIZING BLOCCATO")

    def test_vincolo_attivo(self):
        v = _F["mh345_verdetto"](0.05, 0.0875, 0.05, 0.05)
        assert v.startswith("VINCOLO ROVINA ATTIVO")

    def test_half_kelly_ok(self):
        v = _F["mh345_verdetto"](0.10, 0.0875, 0.03, 0.05)
        assert v.startswith("HALF-KELLY ENTRO RMAX")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith("VINCOLO ROVINA ATTIVO")
        assert "5%" in VERDETTO or "5.00" in VERDETTO
