"""Test tab399 '🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh399_num", "mh399_check_vol", "mh399_check_rho",
           "mh399_check_budgets", "mh399_covmat", "mh399_rischio",
           "mh399_parity", "mh399_verdetto", "mh399_mappa")

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
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.6
R13 = 0.3
R23 = 0.45
B1 = 0.3333333333333333
B2 = 0.3333333333333333
B3 = 0.3333333333333333
W1 = 0.3924976729098959
W2 = 0.2619163820515359
W3 = 0.3455859450385682
SIGP = 0.2328782193569889
ITER = 14
MAXDEV = 1.9824142327706795e-12


class TestRegistry399:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 582
        assert "tab399" in dvars
        assert "tab399" in withs

    def test_titoli_allineati_394_395_396_397_398_399(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397
        assert titoli[dvars.index("tab398")] == TITLE398
        assert titoli[dvars.index("tab399")] == TITLE399

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestParity:
    def _demo(self):
        return _F["mh399_parity"]((V1, V2, V3), R12, R13, R23,
                                  (B1, B2, B3))

    def test_demo_costanti(self):
        p = self._demo()
        assert p["converged"]
        assert p["iters"] == ITER
        for got, exp in zip(p["w"], (W1, W2, W3)):
            assert abs(got - exp) < 1e-15
        assert abs(p["sig"] - SIGP) / SIGP < 1e-15
        assert abs(p["max_dev_pp"] - MAXDEV) < 1e-12

    def test_parita_rc(self):
        # i contributi realizzati eguagliano i budget target
        p = self._demo()
        for got, exp in zip(p["rc_pct"], p["target_pct"]):
            assert abs(got - exp) < 1e-9
        assert abs(sum(p["rc"]) - p["sig"]) / p["sig"] < 1e-12
        assert abs(sum(p["rc_pct"]) - 100.0) < 1e-9

    def test_somma_pesi_e_nonnegativi(self):
        p = self._demo()
        assert abs(sum(p["w"]) - 1.0) < 1e-12
        assert all(_x >= 0.0 for _x in p["w"])

    def test_simmetria(self):
        p = _F["mh399_parity"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                               (1.0, 1.0, 1.0))
        assert p["converged"]
        for _x in p["w"]:
            assert abs(_x - 1.0 / 3.0) < 1e-9

    def test_legge_vol_inversa(self):
        # rho=0, budget pari -> pesi proporzionali a 1/vol
        p = _F["mh399_parity"]((0.2, 0.4, 0.8), 0.0, 0.0, 0.0,
                               (1.0, 1.0, 1.0))
        assert p["converged"]
        _iv = [(1.0 / _v) for _v in (0.2, 0.4, 0.8)]
        _s = sum(_iv)
        for got, exp in zip(p["w"], [_x / _s for _x in _iv]):
            assert abs(got - exp) < 1e-6

    def test_budget_mirati(self):
        # (60,30,10) con vol uguali e rho=0 -> RC% = (60,30,10)
        p = _F["mh399_parity"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                               (60.0, 30.0, 10.0))
        assert p["converged"]
        for got, exp in zip(p["rc_pct"], (60.0, 30.0, 10.0)):
            assert abs(got - exp) < 1e-6
        # legge: w_i proporzionale a sqrt(b_i) a parita' di vol
        _sq = [math.sqrt(_b) for _b in (0.6, 0.3, 0.1)]
        _s = sum(_sq)
        for got, exp in zip(p["w"], [_x / _s for _x in _sq]):
            assert abs(got - exp) < 1e-4

    def test_budget_normalizzati(self):
        # (6,3,1) == (60,30,10): la scala dei budget non conta
        p1 = _F["mh399_parity"]((0.25, 0.35, 0.30), 0.6, 0.3, 0.45,
                                (6.0, 3.0, 1.0))
        p2 = _F["mh399_parity"]((0.25, 0.35, 0.30), 0.6, 0.3, 0.45,
                                (60.0, 30.0, 10.0))
        for a, b in zip(p1["w"], p2["w"]):
            assert abs(a - b) < 1e-12

    def test_invarianza_scala_vol(self):
        # vol x2 -> stessi pesi (il rischio scala, l'allocazione no)
        p1 = self._demo()
        p2 = _F["mh399_parity"]((2 * V1, 2 * V2, 2 * V3), R12, R13, R23,
                                (B1, B2, B3))
        assert p2["converged"]
        for a, b in zip(p1["w"], p2["w"]):
            assert abs(a - b) < 1e-9
        assert abs(p2["sig"] - 2 * p1["sig"]) / p1["sig"] < 1e-9

    def test_rho_simmetrico(self):
        p = _F["mh399_parity"]((0.3, 0.3, 0.3), 0.5, 0.5, 0.5,
                               (1.0, 1.0, 1.0))
        assert p["converged"]
        for _x in p["w"]:
            assert abs(_x - 1.0 / 3.0) < 1e-9

    def test_budget_zero(self):
        # budget 0 -> peso 0, gli altri si spartiscono il rischio
        p = _F["mh399_parity"]((0.25, 0.35, 0.30), 0.6, 0.3, 0.45,
                               (50.0, 50.0, 0.0))
        assert p["converged"]
        assert p["w"][2] == 0.0
        assert p["rc_pct"][2] == 0.0
        assert abs(p["rc_pct"][0] - 50.0) < 1e-6
        assert abs(p["rc_pct"][1] - 50.0) < 1e-6

    def test_budget_pieno(self):
        # budget 100% su un nome -> tutto il nozionale li'
        p = _F["mh399_parity"]((0.25, 0.35, 0.30), 0.6, 0.3, 0.45,
                               (0.0, 100.0, 0.0))
        assert p["converged"]
        assert p["w"] == (0.0, 1.0, 0.0)
        assert p["iters"] == 0

    def test_vol_nulla_non_ammissibile(self):
        # vol nulla ma budget > 0: impossibile -> converged=False
        p = _F["mh399_parity"]((0.0, 0.3, 0.3), 0.0, 0.0, 0.0,
                               (1.0, 1.0, 1.0))
        assert not p["converged"]
        assert p["max_dev_pp"] > 1.0

    def test_cov_psd_ko(self):
        with pytest.raises(ValueError):
            _F["mh399_covmat"]((0.2, 0.2, 0.2), 0.9, 0.9, -0.9)
        with pytest.raises(ValueError):
            _F["mh399_parity"]((0.2, 0.2, 0.2), 0.9, 0.9, -0.9,
                               (1.0, 1.0, 1.0))

    def test_vol_tutte_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh399_parity"]((0.0, 0.0, 0.0), 0.0, 0.0, 0.0,
                               (1.0, 1.0, 1.0))

    def test_num_ko(self):
        with pytest.raises(ValueError):
            _F["mh399_num"](True, "x")
        with pytest.raises(ValueError):
            _F["mh399_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh399_num"](float("inf"), "x")
        with pytest.raises(ValueError):
            _F["mh399_check_vol"](2.5)
        with pytest.raises(ValueError):
            _F["mh399_check_vol"](-0.1)
        with pytest.raises(ValueError):
            _F["mh399_check_rho"](1.5)
        with pytest.raises(ValueError):
            _F["mh399_check_budgets"]((0.0, 0.0, 0.0))
        with pytest.raises(ValueError):
            _F["mh399_check_budgets"]((-1.0, 2.0, 3.0))
        with pytest.raises(ValueError):
            _F["mh399_check_budgets"]((1.0, 1.0))
        with pytest.raises(ValueError):
            _F["mh399_rischio"]((0.5, 0.5), ((1.0, 0.0), (0.0, 1.0)))
        with pytest.raises(ValueError):
            _F["mh399_mappa"]((V1, V2, V3), R12, R13, R23,
                              (B1, B2, B3), 0.0)
        with pytest.raises(ValueError):
            _F["mh399_mappa"]((V1, V2, V3), R12, R13, R23,
                              (B1, B2, B3), -2.0)

    def test_verdetto_stati(self):
        p = self._demo()
        assert _F["mh399_verdetto"](
            p["converged"], p["max_dev_pp"],
            max(p["w"]) * 100.0).startswith("BILANCIATO")
        assert _F["mh399_verdetto"](
            False, 5.0, 30.0).startswith("NON CONVERGENTE")
        assert _F["mh399_verdetto"](
            True, 2.0, 30.0).startswith("NON CONVERGENTE")
        assert _F["mh399_verdetto"](
            True, 0.01, 65.0).startswith("CONCENTRATO")
        assert _F["mh399_verdetto"](
            True, 0.01, 60.0).startswith("CONCENTRATO")
        assert _F["mh399_verdetto"](
            True, 0.01, 59.9).startswith("BILANCIATO")

    def test_mappa_demo(self):
        m = _F["mh399_mappa"]((V1, V2, V3), R12, R13, R23,
                              (B1, B2, B3), 5.0)
        assert m["converged"]
        assert abs(m["sig_eur"] - m["sig"] * 5.0e6) / m["sig_eur"] < 1e-12
        assert abs(sum(m["w_eur"]) - 5.0e6) / 5.0e6 < 1e-12
        assert abs(sum(m["rc_eur"]) - m["sig_eur"]) / m["sig_eur"] < 1e-12
        assert m["verdetto"].startswith("BILANCIATO")
        assert abs(m["max_w_pct"] - max(m["w"]) * 100.0) < 1e-12
