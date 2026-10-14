"""Test tab360 'Kelly frazionario (fractional Kelly): λ·f*': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh360_num", "mh360_parse_seq", "mh360_kelly",
           "mh360_verdetto", "mh360_walk", "mh360_confronto")

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
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
LAM = 0.5
EQUITY0 = 10000.0
FEFF = 0.08333333333333333
FFULL = 0.16666666666666666
EQFFIN = 13603.154027780993
EQBFIN = 15041.37952717448
GAP = -1438.2254993934876
GAP_PCT = -0.09561792499119647
GF = 0.015504800579495104
GB = 0.0206207261596576
MDDF = 0.2718686704282409
MDDB = 0.4976530349794238
N = 20
NWINS = 10
VERDETTO = "HALF-KELLY: λ = 0.50 e' il compromesso classico: circa il 75% della crescita attesa del Kelly pieno con circa meta' del drawdown e della volatilita'. La scelta standard quando le stime di win-rate e payoff sono incerte."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry360:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 457
        assert "tab360" in dvars
        assert "tab360" in withs

    def test_titoli_allineati_356_357_358_359_360(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab457"
        assert titoli[-1] == TITLE457
        assert withs[-1] == "tab457"


class TestNum:
    def test_num_ok(self):
        assert _F["mh360_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh360_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh360_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"](123)


class TestKelly:
    def test_demo(self):
        assert _F["mh360_kelly"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh360_kelly"](0.2, 1.5) == 0.0

    def test_mai_negativo(self):
        assert _F["mh360_kelly"](0.1, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_kelly"](0.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_kelly"](1.5, 1.5)


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh360_verdetto"](0.2, 1.5, 0.5)
        assert v.startswith("NESSUN EDGE")

    def test_leva(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 1.5)
        assert v.startswith("LEVA")

    def test_full_kelly(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 1.0)
        assert v.startswith("FULL-KELLY")

    def test_half_kelly(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 0.5)
        assert v.startswith("HALF-KELLY")

    def test_frazione_prudente(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 0.3)
        assert v.startswith("FRAZIONE PRUDENTE")

    def test_soglie(self):
        # 0.95 -> FULL-KELLY; 0.45 -> HALF-KELLY; 0.44 -> PRUDENTE; 1.01 -> LEVA
        assert _F["mh360_verdetto"](0.5, 1.5, 0.95).startswith("FULL-KELLY")
        assert _F["mh360_verdetto"](0.5, 1.5, 0.45).startswith("HALF-KELLY")
        assert _F["mh360_verdetto"](0.5, 1.5, 0.44).startswith(
            "FRAZIONE PRUDENTE")
        assert _F["mh360_verdetto"](0.5, 1.5, 1.01).startswith("LEVA")

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_verdetto"](0.5, 1.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_verdetto"](2.0, 1.5, 0.5)


class TestWalk:
    def _demo(self):
        return _F["mh360_confronto"](SEQ, B, P, LAM, EQUITY0)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_eff"] == FEFF == 1.0 / 12.0
        assert m["f_full"] == FFULL == 1.0 / 6.0
        assert m["lam"] == LAM == 0.5
        assert abs(m["eqf_fin"] - EQFFIN) < 1e-9
        assert abs(m["eqb_fin"] - EQBFIN) < 1e-9
        assert abs(m["gap"] - GAP) < 1e-9
        assert abs(m["gap_pct"] - GAP_PCT) < 1e-12
        assert abs(m["growth_frac"] - GF) < 1e-12
        assert abs(m["growth_full"] - GB) < 1e-12
        assert abs(m["max_dd_frac"] - MDDF) < 1e-12
        assert abs(m["max_dd_full"] - MDDB) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("HALF-KELLY")
        assert m["equity0"] == EQUITY0 == 10000.0

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eqf_path"] == m2["eqf_path"]
        assert m1["eqb_path"] == m2["eqb_path"]

    def test_equity_iniziale(self):
        m = self._demo()
        assert m["eqf_path"][0] == EQUITY0
        assert m["eqb_path"][0] == EQUITY0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eqf_path"]) == N + 1
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
            assert r["eq_frac"] == m["eqf_path"][i + 1]
            assert r["eq_full"] == m["eqb_path"][i + 1]

    def test_gap_coerente(self):
        m = self._demo()
        assert m["gap"] == m["eqf_fin"] - m["eqb_fin"]
        assert m["gap_pct"] == m["gap"] / m["eqb_fin"]

    def test_frazionario_cresce_meno(self):
        m = self._demo()
        assert m["growth_frac"] < m["growth_full"]

    def test_frazionario_drawdown_minore(self):
        m = self._demo()
        assert m["max_dd_frac"] < m["max_dd_full"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"]("", B, P, LAM, EQUITY0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, 1.5, LAM, EQUITY0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, LAM, 0.0)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, -0.5, EQUITY0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh360_confronto"](SEQ, B, P, LAM, EQUITY0)
        assert m["b"] == B
        assert m["p"] == P
        assert m["lam"] == LAM
        assert m["equity0"] == EQUITY0

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"]("XYZ", B, P, LAM, EQUITY0)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, 0.0, EQUITY0)

