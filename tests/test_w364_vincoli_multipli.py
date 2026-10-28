"""Test tab364 'Kelly con vincoli multipli: cap, lotti, stop e drawdown': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh364_num", "mh364_parse_seq", "mh364_fstar_sl", "mh364_g_sl",
           "mh364_cap", "mh364_lotti", "mh364_dd_mult", "mh364_bindings",
           "mh364_verdetto", "mh364_walk", "mh364_curva", "mh364_analisi")

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
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
P = 0.6
B = 1.2
L = 0.5
FCAP = 0.2
LOT = 0.01
DD = 0.05
DDMAX = 0.25
SEQ = "WLWWLWWWLLWWWLWWLWLW"
FSTAR = 0.8666666666666667
FDCAP = 0.2
FDLOT = 0.2
FFIN = 0.16000000000000003
GSTAR = 0.20057626967129927
GFIN = 0.07202689761027432
GR = 0.3590997964430722
FINK = 198.83179954253245
FINV = 5.471496322668106
BIND = ['cap', 'drawdown']
VERDETTO = "VINCOLI FORTI (cap, drawdown): il tasso di crescita crolla al 35.9% dell'ottimo (f* 86.67% -> 16.00%). Valuta se tutti i vincoli sono davvero necessari."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry364:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 770
        assert "tab364" in dvars
        assert "tab364" in withs

    def test_titoli_allineati_360_361_362_363_364(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh364_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_num"](float("nan"), "x")


class TestParseSeq:
    def test_ok(self):
        assert _F["mh364_parse_seq"]("wL") == ("W", "L")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_parse_seq"]("   ")

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_parse_seq"]("WX")


class TestFstarSl:
    def test_demo(self):
        assert abs(_F["mh364_fstar_sl"](P, B, L) - FSTAR) < 1e-12

    def test_stop_1_classico(self):
        assert abs(_F["mh364_fstar_sl"](P, B, 1.0)
                   - (P * B - (1.0 - P)) / B) < 1e-12

    def test_no_edge(self):
        assert _F["mh364_fstar_sl"](0.30, 1.0, 0.5) == 0.0

    def test_L_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_fstar_sl"](P, B, 0.0)


class TestGSl:
    def test_g_zero(self):
        assert _F["mh364_g_sl"](0.0, P, B, L) == 0.0

    def test_g_demo(self):
        assert abs(_F["mh364_g_sl"](FSTAR, P, B, L) - GSTAR) < 1e-12

    def test_g_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_g_sl"](1.0 / L, P, B, L)


class TestCap:
    def test_cap_vincolante(self):
        assert _F["mh364_cap"](FSTAR, FCAP) == FDCAP

    def test_cap_non_vincolante(self):
        assert _F["mh364_cap"](0.10, 0.30) == 0.10

    def test_fcap_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_cap"](0.10, 1.0)


class TestLotti:
    def test_demo(self):
        assert _F["mh364_lotti"](FDCAP, LOT) == FDLOT

    def test_floor_prudente(self):
        assert _F["mh364_lotti"](0.157, 0.05) == pytest.approx(0.15)

    def test_lot_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_lotti"](0.10, 0.0)


class TestDdMult:
    def test_demo(self):
        assert abs(_F["mh364_dd_mult"](DD, DDMAX) - 0.8) < 1e-12

    def test_azzerato_al_limite(self):
        assert _F["mh364_dd_mult"](DDMAX, DDMAX) == 0.0

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_dd_mult"](0.05, 0.0)


class TestBindings:
    def test_demo(self):
        assert _F["mh364_bindings"](FSTAR, FDCAP, FDLOT, 0.8) == BIND

    def test_nessuno(self):
        assert _F["mh364_bindings"](0.10, 0.10, 0.10, 1.0) == []


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh364_verdetto"](0.0, 0.0, 1.0, []).startswith(
            "NESSUN EDGE")

    def test_non_vincolanti(self):
        assert _F["mh364_verdetto"](0.20, 0.20, 1.0, []).startswith(
            "NON VINCOLANTI")

    def test_leggeri(self):
        assert _F["mh364_verdetto"](0.20, 0.19, 0.99, ["cap"]).startswith(
            "VINCOLI LEGGERI")

    def test_significativi(self):
        assert _F["mh364_verdetto"](0.20, 0.15, 0.80,
                                   ["cap"]).startswith(
            "VINCOLI SIGNIFICATIVI")

    def test_forti(self):
        assert _F["mh364_verdetto"](0.20, 0.10, 0.50,
                                   ["cap", "drawdown"]).startswith(
            "VINCOLI FORTI")


class TestWalk:
    def test_demo(self):
        sq = _F["mh364_parse_seq"](SEQ)
        wk = _F["mh364_walk"](sq, FSTAR, B, L)
        wv = _F["mh364_walk"](sq, FFIN, B, L)
        assert wk["n"] == wv["n"] == 20
        assert abs(wk["finale"] - FINK) < 1e-9
        assert abs(wv["finale"] - FINV) < 1e-9
        assert len(wk["equity"]) == 21
        assert 0.0 <= wk["max_dd"] < 1.0

    def test_stop_tronca_perdita(self):
        sq = _F["mh364_parse_seq"]("L")
        w = _F["mh364_walk"](sq, 0.10, 2.0, 0.5)
        assert w["finale"] == pytest.approx(1.0 - 0.10 * 0.5)

    def test_f_zero_fermo(self):
        sq = _F["mh364_parse_seq"]("WL")
        w = _F["mh364_walk"](sq, 0.0, B, L)
        assert all(e == 1.0 for e in w["equity"])

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_walk"](("W",), 1.0 / L, B, L)


class TestCurva:
    def test_demo(self):
        c = _F["mh364_curva"](P, B, L, 1.90, 25)
        assert len(c) == 25
        assert c[0]["f"] == 0.0
        assert abs(c[0]["g"]) < 1e-15
        imax = max(range(25), key=lambda i: c[i]["g"])
        assert abs(c[imax]["f"] - FSTAR) < 0.10

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_curva"](P, B, L, 1.90, 1)


class TestAnalisi:
    def _demo(self):
        return _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, DDMAX, SEQ)

    def test_demo(self):
        a = self._demo()
        assert abs(a["f_star"] - FSTAR) < 1e-12
        assert a["f_dopo_cap"] == FDCAP
        assert a["f_dopo_lotti"] == FDLOT
        assert abs(a["f_fin"] - FFIN) < 1e-9
        assert abs(a["g_star"] - GSTAR) < 1e-12
        assert abs(a["g_ratio"] - GR) < 1e-12
        assert abs(a["finalek"] - FINK) < 1e-9
        assert abs(a["finalev"] - FINV) < 1e-9
        assert a["bindings"] == BIND
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("VINCOLI FORTI")
        assert a["n"] == 20
        assert a["finalev"] < a["finalek"]

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["finalek"] == a2["finalek"]
        assert a1["verdetto"] == a2["verdetto"]

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](0.0, B, L, FCAP, LOT, DD, DDMAX, SEQ)

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, 0.0, SEQ)

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, DDMAX, "WX")
