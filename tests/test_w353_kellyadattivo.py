"""Test tab353 'Kelly adattivo: win-rate rolling e size dinamica': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh353_num", "mh353_parse_seq", "mh353_ewma_p", "mh353_kelly_f",
           "mh353_adaptive", "mh353_verdetto", "mh353_confronto")

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
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
SEQ = 'WLLWLLWLLWWWLWWWWLWW'
B = 1.5
LAM = 0.92
PPRIOR = 0.55
FCAP = 0.4
MAXSTEP = 0.05
N = 20
NWINS = 12
PFREQ = 0.6
PEWMA = 0.6563440757052181
FSTATIC = 0.33333333333333326
FFINAL = 0.4
VERDETTO = "AUMENTO SIZE: la win-rate recente (p_ewma=65.6%) e' sopra la media storica (60.0%): il Kelly adattivo sale a f=40.00% contro f_static=33.33% (+6.67%). Il regime recente e' piu' favorevole: puoi spingere la size, restando sotto il cap."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry353:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 474
        assert "tab353" in dvars
        assert "tab353" in withs

    def test_titoli_allineati_349_350_351_352_353(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab349")] == TITLE349
        assert titoli[dvars.index("tab350")] == TITLE350
        assert titoli[dvars.index("tab351")] == TITLE351
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab474"
        assert titoli[-1] == TITLE474
        assert withs[-1] == "tab474"


class TestNum:
    def test_num_ok(self):
        assert _F["mh353_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh353_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh353_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"](123)


class TestEwma:
    def test_lam_1_prior_intatto(self):
        assert _F["mh353_ewma_p"]((1, 0, 1), 1.0, 0.55) == 0.55

    def test_manuale_due_passi(self):
        # 0.5 -> 0.75 -> 0.875 con lam=0.5
        assert _F["mh353_ewma_p"]((1, 1), 0.5, 0.5) == 0.875

    def test_lam_0_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((1,), 0.0, 0.5)

    def test_prior_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((1,), 0.9, 0.0)

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((), 0.9, 0.5)


class TestKellyF:
    def test_demo(self):
        assert abs(_F["mh353_kelly_f"](0.6, 1.5) - 1.0 / 3.0) < 1e-12

    def test_no_edge_zero(self):
        assert _F["mh353_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_kelly_f"](1.5, 1.5)


class TestAdaptive:
    def _demo(self):
        return _F["mh353_confronto"](SEQ, B, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 12
        assert abs(m["p_freq"] - PFREQ) < 1e-12
        assert abs(m["p_ewma"] - PEWMA) < 1e-9
        assert abs(m["f_static"] - FSTATIC) < 1e-12
        assert abs(m["f_final"] - FFINAL) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("AUMENTO SIZE")

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["f_path"] == m2["f_path"]
        assert m1["p_path"] == m2["p_path"]

    def test_slew_rate_limit(self):
        m = self._demo()
        passi = [abs(b - a)
                 for a, b in zip(m["f_path"], m["f_path"][1:])]
        assert max(passi) <= MAXSTEP + 1e-12

    def test_cap_rispettato(self):
        m = self._demo()
        assert all(0.0 <= f <= FCAP + 1e-12 for f in m["f_path"])

    def test_f_iniziale_da_prior(self):
        m = self._demo()
        atteso = min(_F["mh353_kelly_f"](PPRIOR, B), FCAP)
        assert abs(m["f_path"][0] - atteso) < 1e-15

    def test_righe(self):
        m = self._demo()
        assert len(m["righe"]) == N
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        assert len(m["f_path"]) == N + 1
        assert len(m["p_path"]) == N + 1

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh353_confronto"]("WLW", B, LAM, PPRIOR, FCAP, MAXSTEP)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh353_verdetto"](0.10, 0.10, 0.50, 0.50, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_pausa(self):
        v = _F["mh353_verdetto"](0.0, 0.10, 0.40, 0.50, 20)
        assert v.startswith("PAUSA")

    def test_aumento(self):
        v = _F["mh353_verdetto"](0.40, 1.0 / 3.0, 0.656, 0.60, 20)
        assert v.startswith("AUMENTO SIZE")

    def test_riduzione(self):
        v = _F["mh353_verdetto"](0.10, 0.20, 0.45, 0.55, 20)
        assert v.startswith("RIDUZIONE SIZE")

    def test_stabile(self):
        v = _F["mh353_verdetto"](0.20, 0.205, 0.55, 0.55, 20)
        assert v.startswith("STABILE")

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_verdetto"](-0.1, 0.1, 0.5, 0.5, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_verdetto"](0.1, 0.1, 0.5, 0.5, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh353_confronto"](SEQ, B, LAM, PPRIOR, FCAP, MAXSTEP)
        assert m["b"] == B
        assert m["lam"] == LAM
        assert m["p_prior"] == PPRIOR
        assert m["f_cap"] == FCAP
        assert m["max_step"] == MAXSTEP
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"]("XYZ", B, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"](SEQ, -1.0, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"](SEQ, B, 1.5, PPRIOR, FCAP, MAXSTEP)

