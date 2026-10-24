"""Test tab385 'Expected Shortfall: misura di rischio coerente': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh385_num", "mh385_phi", "mh385_ppf", "mh385_port_sigma",
           "mh385_var", "mh385_es", "mh385_comp_es", "mh385_extra",
           "mh385_verdetto", "mh385_tail_prob", "mh385_mappa")

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
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
E1 = 10000.0
E2 = 8000.0
S1 = 0.15
S2 = 0.2
RHO = 0.6
ALPHA = 0.99
SIG = 2773.0849247724095
VAR = 6451.160219279
ES = 7390.865375730005
EXTRA = 0.14566451994832486
RATIO = 1.1456645199483249
CES1 = 3546.46205935549
CES2 = 3844.403316374515
TAIL2 = 1.6381173918444958e-06


class TestRegistry385:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 681
        assert "tab385" in dvars
        assert "tab385" in withs

    def test_titoli_allineati_380_381_382_383_384_385(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385

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


class TestNum:
    def test_num_ok(self):
        assert _F["mh385_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](float("inf"), "x")


class TestPhiPpf:
    def test_phi_zero(self):
        assert _F["mh385_phi"](0.0) == pytest.approx(0.3989422804014327)

    def test_phi_simmetria(self):
        assert _F["mh385_phi"](1.5) == pytest.approx(_F["mh385_phi"](-1.5))

    def test_ppf_nota(self):
        assert _F["mh385_ppf"](0.99) == pytest.approx(2.32634787404084)

    def test_ppf_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_ppf"](1.0)
        with pytest.raises(ValueError):
            _F["mh385_ppf"](0.0)


class TestPortSigma:
    def test_demo(self):
        assert _F["mh385_port_sigma"](E1, E2, S1, S2, RHO) == pytest.approx(SIG)

    def test_forma_chiusa(self):
        v1, v2 = E1 * S1, E2 * S2
        att = math.sqrt(v1 ** 2 + v2 ** 2 + 2.0 * RHO * v1 * v2)
        assert _F["mh385_port_sigma"](E1, E2, S1, S2, RHO) == pytest.approx(att)

    def test_rho_meno_uno(self):
        v1, v2 = E1 * S1, E2 * S2
        assert _F["mh385_port_sigma"](
            E1, E2, S1, S2, -1.0) == pytest.approx(abs(v1 - v2))

    def test_rho_uno(self):
        v1, v2 = E1 * S1, E2 * S2
        assert _F["mh385_port_sigma"](
            E1, E2, S1, S2, 1.0) == pytest.approx(v1 + v2)

    def test_vuoto_zero(self):
        assert _F["mh385_port_sigma"](0.0, 0.0, S1, S2, RHO) == 0.0

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](E1, E2, S1, S2, 1.5)

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](E1, E2, 0.0, S2, RHO)

    def test_e_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](-1.0, E2, S1, S2, RHO)


class TestVarEs:
    def test_demo_var(self):
        assert _F["mh385_var"](SIG, ALPHA) == pytest.approx(VAR)

    def test_demo_es(self):
        assert _F["mh385_es"](SIG, ALPHA) == pytest.approx(ES)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert _F["mh385_var"](SIG, ALPHA) == pytest.approx(SIG * z)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh385_es"](SIG, ALPHA) == pytest.approx(
            SIG * phi / (1.0 - ALPHA))

    def test_es_maggiore_var(self):
        assert _F["mh385_es"](SIG, ALPHA) > _F["mh385_var"](SIG, ALPHA)

    def test_ratio_normale_99(self):
        assert ES / VAR == pytest.approx(1.1456, abs=1e-3)

    def test_sig_zero(self):
        assert _F["mh385_var"](0.0, ALPHA) == 0.0
        assert _F["mh385_es"](0.0, ALPHA) == 0.0

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_var"](SIG, 1.0)
        with pytest.raises(ValueError):
            _F["mh385_es"](SIG, 0.0)


class TestCompEs:
    def test_demo(self):
        c1, c2 = _F["mh385_comp_es"](E1, E2, S1, S2, RHO, ALPHA)
        assert c1 == pytest.approx(CES1)
        assert c2 == pytest.approx(CES2)

    def test_somma_eulero(self):
        c1, c2 = _F["mh385_comp_es"](E1, E2, S1, S2, RHO, ALPHA)
        assert c1 + c2 == pytest.approx(ES)

    def test_vuoto(self):
        assert _F["mh385_comp_es"](
            0.0, 0.0, S1, S2, RHO, ALPHA) == (0.0, 0.0)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_comp_es"](E1, E2, S1, S2, RHO, 1.5)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh385_extra"](ES, VAR) == pytest.approx(EXTRA)
        assert _F["mh385_verdetto"](EXTRA).startswith("MODERATA")

    def test_bordi(self):
        assert _F["mh385_verdetto"](0.0).startswith("CONTENUTA")
        assert _F["mh385_verdetto"](0.0999).startswith("CONTENUTA")
        assert _F["mh385_verdetto"](0.10).startswith("MODERATA")
        assert _F["mh385_verdetto"](0.1999).startswith("MODERATA")
        assert _F["mh385_verdetto"](0.20).startswith("RILEVANTE")
        assert _F["mh385_verdetto"](0.3499).startswith("RILEVANTE")
        assert _F["mh385_verdetto"](0.35).startswith("SEVERA")
        assert _F["mh385_verdetto"](math.inf).startswith("SEVERA")

    def test_extra_inf(self):
        assert _F["mh385_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh385_extra"](0.0, 0.0) == 0.0

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_verdetto"](-0.01)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_verdetto"](float("nan"))


class TestTailProb:
    def test_demo(self):
        assert _F["mh385_tail_prob"](SIG, VAR, 2.0) == pytest.approx(TAIL2)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        att = 1.0 - NormalDist().cdf(2.0 * VAR / SIG)
        assert _F["mh385_tail_prob"](SIG, VAR, 2.0) == pytest.approx(att)

    def test_piccola(self):
        assert 0.0 < _F["mh385_tail_prob"](SIG, VAR, 2.0) < 0.01

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_tail_prob"](0.0, VAR, 2.0)


class TestMappa:
    def _b(self):
        return _F["mh385_mappa"](E1, E2, S1, S2, RHO, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["sig"] == pytest.approx(SIG)
        assert b["var"] == pytest.approx(VAR)
        assert b["es"] == pytest.approx(ES)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["ces1"] == pytest.approx(CES1)
        assert b["ces2"] == pytest.approx(CES2)
        assert b["tail2"] == pytest.approx(TAIL2)
        assert b["verdetto"].startswith("MODERATA")

    def test_coerenza(self):
        b = self._b()
        assert b["ces1"] + b["ces2"] == pytest.approx(b["es"])
        assert b["es"] > b["var"]
        assert b["extra"] == pytest.approx((b["es"] - b["var"]) / b["var"])
        assert b["ratio"] == pytest.approx(b["es"] / b["var"])

    def test_echo_input(self):
        b = self._b()
        assert b["e1"] == E1
        assert b["e2"] == E2
        assert b["s1"] == S1
        assert b["s2"] == S2
        assert b["rho"] == RHO
        assert b["alpha"] == ALPHA

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_mappa"](E1, E2, S1, S2, RHO, 1.5)
