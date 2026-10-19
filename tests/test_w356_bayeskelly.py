"""Test tab356 'Kelly bayesiano: sizing con win-rate posterior': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh356_num", "mh356_parse_seq", "mh356_kelly_f",
           "mh356_posterior", "mh356_beta_reg", "mh356_p_quantile",
           "mh356_edge_prob", "mh356_verdetto", "mh356_walk",
           "mh356_confronto")

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
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
ALPHA = 2.0
BETA = 2.0
APOST = 12.0
BPOST = 12.0
PMEAN = 0.5
PQUANT05 = 0.3351476474715449
EDGEPROB = 0.8363565593601016
PEST = 0.5
F = 0.16666666666666666
EQFIN = 0.5832514684465875
MAXDD = 0.8133595300970919
N = 20
NWINS = 10
VERDETTO = "EDGE MARGINALE: la posterior da' 83.6% di probabilita' che il vero win-rate batta il break-even. Considera la modalita' prudente (quantile 5%)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry356:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 558
        assert "tab356" in dvars
        assert "tab356" in withs

    def test_titoli_allineati_352_353_354_355_356(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353
        assert titoli[dvars.index("tab354")] == TITLE354
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh356_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh356_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh356_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"](123)


class TestBetaReg:
    def test_uniforme(self):
        assert abs(_F["mh356_beta_reg"](1, 1, 0.3) - 0.3) < 1e-9

    def test_quadrato(self):
        assert abs(_F["mh356_beta_reg"](2, 1, 0.5) - 0.25) < 1e-9

    def test_complemento(self):
        assert abs(_F["mh356_beta_reg"](1, 2, 0.5) - 0.75) < 1e-9

    def test_simmetria(self):
        assert abs(_F["mh356_beta_reg"](12, 12, 0.5) - 0.5) < 1e-9

    def test_bordi(self):
        assert _F["mh356_beta_reg"](3, 4, 0.0) == 0.0
        assert _F["mh356_beta_reg"](3, 4, 1.0) == 1.0

    def test_a_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_beta_reg"](0, 1, 0.5)

    def test_x_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_beta_reg"](1, 1, 1.5)


class TestQuantile:
    def test_radice(self):
        assert abs(_F["mh356_p_quantile"](2, 1, 0.25) - 0.5) < 1e-9

    def test_complemento(self):
        assert abs(_F["mh356_p_quantile"](1, 2, 0.75) - 0.5) < 1e-9

    def test_uniforme(self):
        assert abs(_F["mh356_p_quantile"](1, 1, 0.05) - 0.05) < 1e-9

    def test_mediana_simmetrica(self):
        assert abs(_F["mh356_p_quantile"](12, 12, 0.5) - 0.5) < 1e-7

    def test_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_p_quantile"](2, 2, 1.5)

    def test_a_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_p_quantile"](0, 2, 0.5)


class TestKellyF:
    def test_demo(self):
        assert _F["mh356_kelly_f"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh356_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_kelly_f"](1.5, 1.5)


class TestPosterior:
    def test_demo(self):
        assert _F["mh356_posterior"](2.0, 2.0, (1, 1, 0)) == (4.0, 3.0)

    def test_vuota(self):
        assert _F["mh356_posterior"](2.0, 2.0, ()) == (2.0, 2.0)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_posterior"](0.0, 2.0, (1,))


class TestEdgeProb:
    def test_demo(self):
        assert abs(_F["mh356_edge_prob"](12.0, 12.0, 1.5)
                   - EDGEPROB) < 1e-9

    def test_simmetria(self):
        assert abs(_F["mh356_edge_prob"](12.0, 12.0, 1.0) - 0.5) < 1e-9

    def test_monotonia_b(self):
        assert (_F["mh356_edge_prob"](12.0, 12.0, 2.0)
                > _F["mh356_edge_prob"](12.0, 12.0, 1.5))

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_edge_prob"](12.0, 12.0, 0.0)


class TestWalk:
    def _demo(self):
        return _F["mh356_confronto"](SEQ, B, ALPHA, BETA)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["a_post"] == APOST == 12.0
        assert m["b_post"] == BPOST == 12.0
        assert m["p_mean"] == PMEAN == 0.5
        assert abs(m["p_quant05"] - PQUANT05) < 1e-9
        assert abs(m["edge_prob"] - EDGEPROB) < 1e-9
        assert m["p_est"] == PEST == 0.5
        assert abs(m["f"] - F) < 1e-12
        assert abs(m["eq_fin"] - EQFIN) < 1e-9
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("EDGE MARGINALE")
        assert m["p_be"] == 0.4

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eq_path"] == m2["eq_path"]
        assert m1["p_est"] == m2["p_est"]

    def test_equity_iniziale_uno(self):
        m = self._demo()
        assert m["eq_path"][0] == 1.0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eq_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_prudente_taglia_size(self):
        m = _F["mh356_confronto"](SEQ, B, ALPHA, BETA, "prudente")
        assert m["p_est"] == m["p_quant05"]
        assert m["f"] == 0.0
        assert m["verdetto"] == VERDETTO

    def test_righe_progressive(self):
        m = self._demo()
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        assert m["righe"][-1]["a"] == APOST
        assert m["righe"][-1]["b"] == BPOST
        for i, r in enumerate(m["righe"]):
            assert r["equity"] == m["eq_path"][i + 1]

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh356_confronto"]("WLW", B, ALPHA, BETA)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_modo_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, B, ALPHA, BETA, "strano")

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"]("XYZ", B, ALPHA, BETA)


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh356_verdetto"](0.99, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_marginale(self):
        v = _F["mh356_verdetto"](0.84, 20)
        assert v.startswith("EDGE MARGINALE")

    def test_attendibile(self):
        v = _F["mh356_verdetto"](0.95, 20)
        assert v.startswith("EDGE ATTENDIBILE")

    def test_non_attendibile(self):
        v = _F["mh356_verdetto"](0.49, 20)
        assert v.startswith("EDGE NON ATTENDIBILE")

    def test_soglia_090_attendibile(self):
        v = _F["mh356_verdetto"](0.91, 20)
        assert v.startswith("EDGE ATTENDIBILE")

    def test_soglia_050_marginale(self):
        v = _F["mh356_verdetto"](0.51, 20)
        assert v.startswith("EDGE MARGINALE")

    def test_ep_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_verdetto"](1.5, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_verdetto"](0.9, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh356_confronto"](SEQ, B, ALPHA, BETA)
        assert m["b"] == B
        assert m["alpha"] == ALPHA
        assert m["beta"] == BETA
        assert m["modo"] == "media"
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"]("XYZ", B, ALPHA, BETA)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, -1.0, ALPHA, BETA)

    def test_prior_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, B, 0.0, BETA)

