"""Test tab359 'Kelly con take-profit: sizing con vincita troncata': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh359_num", "mh359_parse_seq", "mh359_kelly_tp",
           "mh359_kelly_base", "mh359_verdetto", "mh359_walk",
           "mh359_confronto")

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
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
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
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
T = 1.1
EQUITY0 = 10000.0
FTP = 0.04545454545454549
FBASE = 0.16666666666666666
RATIO = 0.272727272727273
EQSFIN = 10229.611250772074
EQBFIN = 15041.37952717448
GAP = -4811.768276402407
GAP_PCT = -0.31990205869808913
MAXDD = 0.16790604179731916
N = 20
NWINS = 10
VERDETTO = "TAGLIO FORTE: il take-profit a 1.10x dimezza il Kelly (da 16.67% a 4.55%, rapporto 0.27x): il TP mangia buona parte dell'edge. O accetti un sizing molto prudente, o allenti il take-profit per lasciare correre di piu' i profitti."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry359:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 469
        assert "tab359" in dvars
        assert "tab359" in withs

    def test_titoli_allineati_355_356_357_358_359(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab469"
        assert titoli[-1] == TITLE469
        assert withs[-1] == "tab469"


class TestNum:
    def test_num_ok(self):
        assert _F["mh359_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh359_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh359_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"](123)


class TestKellyTp:
    def test_demo(self):
        assert _F["mh359_kelly_tp"](0.5, 1.1) == pytest.approx(0.05 / 1.1)

    def test_no_edge_zero(self):
        assert _F["mh359_kelly_tp"](0.2, 1.1) == 0.0

    def test_mai_negativo(self):
        assert _F["mh359_kelly_tp"](0.1, 1.1) == 0.0

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_kelly_tp"](0.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_kelly_tp"](1.5, 1.1)


class TestKellyBase:
    def test_demo(self):
        assert _F["mh359_kelly_base"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh359_kelly_base"](0.2, 1.5) == 0.0

    def test_sempre_sopra_tp(self):
        for p, b, t in ((0.5, 1.5, 1.1), (0.6, 2.0, 1.3),
                        (0.7, 1.5, 1.2), (0.55, 1.8, 1.4)):
            ft = _F["mh359_kelly_tp"](p, t)
            fb = _F["mh359_kelly_base"](p, b)
            if (p * t - (1.0 - p)) > 0:
                assert fb >= ft


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh359_verdetto"](0.2, 1.5, 1.1)
        assert v.startswith("NESSUN EDGE")

    def test_tp_inutile(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.5)
        assert v.startswith("TP INUTILE")

    def test_taglio_forte(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.1)
        assert v.startswith("TAGLIO FORTE")

    def test_taglio_moderato(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.3)
        assert v.startswith("TAGLIO MODERATO")

    def test_taglio_leggero(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.45)
        assert v.startswith("TAGLIO LEGGERO")

    def test_soglie_05_09(self):
        # r = 0.2727 -> FORTE; r = 0.6923 -> MODERATO; r = 0.9310 -> LEGGERO
        assert _F["mh359_verdetto"](0.5, 1.5, 1.1).startswith("TAGLIO FORTE")
        assert _F["mh359_verdetto"](0.5, 1.5, 1.3).startswith(
            "TAGLIO MODERATO")
        assert _F["mh359_verdetto"](0.5, 1.5, 1.45).startswith(
            "TAGLIO LEGGERO")

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_verdetto"](0.5, 1.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_verdetto"](2.0, 1.5, 1.1)


class TestWalk:
    def _demo(self):
        return _F["mh359_confronto"](SEQ, B, P, T, EQUITY0)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_tp"] == FTP == pytest.approx(0.05 / 1.1)
        assert m["f_base"] == FBASE == 1.0 / 6.0
        assert m["ratio"] == RATIO == pytest.approx(
            (0.05 / 1.1) / (1.0 / 6.0))
        assert abs(m["eqs_fin"] - EQSFIN) < 1e-9
        assert abs(m["eqb_fin"] - EQBFIN) < 1e-9
        assert abs(m["gap"] - GAP) < 1e-9
        assert abs(m["gap_pct"] - GAP_PCT) < 1e-12
        assert abs(m["max_dd_tp"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("TAGLIO FORTE")
        assert m["t"] == T == 1.1
        assert m["equity0"] == EQUITY0 == 10000.0

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eqs_path"] == m2["eqs_path"]
        assert m1["eqb_path"] == m2["eqb_path"]

    def test_equity_iniziale(self):
        m = self._demo()
        assert m["eqs_path"][0] == EQUITY0
        assert m["eqb_path"][0] == EQUITY0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eqs_path"]) == N + 1
        assert len(m["eqb_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_righe_coerenti(self):
        m = self._demo()
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        for i, r in enumerate(m["righe"]):
            assert r["eq_tp"] == m["eqs_path"][i + 1]
            assert r["eq_base"] == m["eqb_path"][i + 1]

    def test_gap_coerente(self):
        m = self._demo()
        assert m["gap"] == m["eqs_fin"] - m["eqb_fin"]
        assert m["gap_pct"] == m["gap"] / m["eqb_fin"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"]("", B, P, T, EQUITY0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, 1.5, T, EQUITY0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, T, 0.0)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, -0.5, EQUITY0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh359_confronto"](SEQ, B, P, T, EQUITY0)
        assert m["b"] == B
        assert m["p"] == P
        assert m["t"] == T
        assert m["equity0"] == EQUITY0

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"]("XYZ", B, P, T, EQUITY0)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, 0.0, EQUITY0)

