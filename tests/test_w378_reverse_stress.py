"""Test tab378 'Reverse stress test: quanto shock regge il limite?': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh378_num", "mh378_z", "mh378_cov", "mh378_sigma_p",
           "mh378_AB", "mh378_var_p", "mh378_var_k",
           "mh378_break_vol", "mh378_break_corr", "mh378_verdetto",
           "mh378_reverse")

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
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
E = (10000.0, 8000.0, 6000.0)
S = (0.15, 0.2, 0.1)
RHO = (0.6, 0.3, 0.4)
SE = (1500.0, 1600.0, 600.0)
ALPHA = 0.95
LIM = 12000.0
LIM2 = 5500.0
Z = 1.6448536269514715
SIGP = 3059.0848304680926
VARB = 5031.746778547669
MSTAR = 2.3848576902082503
KSTAR2 = 0.4207636568358517
AA = 9358000.0
BB = 4332000.0
C01 = 1440000.0


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry378:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 583
        assert "tab378" in dvars
        assert "tab378" in withs

    def test_titoli_allineati_373_374_375_376_377_378(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377
        assert titoli[dvars.index("tab378")] == TITLE378

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh378_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_num"](float("inf"), "x")


class TestZ:
    def test_z_demo(self):
        assert _F["mh378_z"](ALPHA) == pytest.approx(Z)

    def test_z_95_forma_nota(self):
        assert _F["mh378_z"](0.95) == pytest.approx(1.6448536269514722)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_z"](0.4)
        with pytest.raises(ValueError):
            _F["mh378_z"](1.0)


class TestCov:
    def test_demo_c01(self):
        C = _F["mh378_cov"](SE, RHO)
        assert C[0][1] == pytest.approx(C01)
        assert C[1][0] == pytest.approx(C01)

    def test_diagonale(self):
        C = _F["mh378_cov"](SE, RHO)
        for i in range(3):
            assert C[i][i] == pytest.approx(SE[i] ** 2)

    def test_rho_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_cov"](SE, (1.5, 0.0, 0.0))

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_cov"]((-1.0, SE[1], SE[2]), RHO)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_cov"]((1.0, 2.0), RHO)


class TestSigmaP:
    def test_demo(self):
        assert _F["mh378_sigma_p"](E, S, RHO) == pytest.approx(SIGP)

    def test_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        var = (se[0] ** 2 + se[1] ** 2 + se[2] ** 2
               + 2.0 * (se[0] * se[1] * r12 + se[0] * se[2] * r13
                        + se[1] * se[2] * r23))
        assert _F["mh378_sigma_p"](E, S, RHO) == pytest.approx(
            math.sqrt(var))

    def test_zero_vol(self):
        assert _F["mh378_sigma_p"](E, (0.0, 0.0, 0.0), RHO) == pytest.approx(
            0.0)

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_sigma_p"](E, (-0.1, S[1], S[2]), RHO)


class TestAB:
    def test_demo(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        assert A == pytest.approx(AA)
        assert B == pytest.approx(BB)

    def test_a_uguale_sigma_quadro(self):
        A, _ = _F["mh378_AB"](E, S, RHO)
        assert A == pytest.approx(SIGP ** 2)

    def test_b_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        b = 2.0 * (se[0] * se[1] * (1.0 - r12)
                   + se[0] * se[2] * (1.0 - r13)
                   + se[1] * se[2] * (1.0 - r23))
        _, B = _F["mh378_AB"](E, S, RHO)
        assert B == pytest.approx(b)

    def test_sigma_k_affine(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        for k in (0.0, 0.37, 1.0):
            rp = tuple((1.0 - k) * r + k for r in RHO)
            s2 = _F["mh378_sigma_p"](E, S, rp) ** 2
            assert s2 == pytest.approx(A + k * B)


class TestVarP:
    def test_demo(self):
        assert _F["mh378_var_p"](E, S, RHO, ALPHA) == pytest.approx(VARB)

    def test_uguale_z_sigma(self):
        assert _F["mh378_var_p"](E, S, RHO, ALPHA) == pytest.approx(Z * SIGP)

    def test_scala_con_m(self):
        m = 2.5
        v = _F["mh378_var_p"](E, tuple(m * x for x in S), RHO, ALPHA)
        assert v == pytest.approx(m * VARB)


class TestVarK:
    def test_k0_uguale_base(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        assert _F["mh378_var_k"](A, B, Z, 0.0) == pytest.approx(VARB)

    def test_k1_forma_chiusa(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        assert _F["mh378_var_k"](A, B, Z, 1.0) == pytest.approx(
            Z * math.sqrt(A + B))

    def test_k_fuori_ko(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        with pytest.raises(ValueError):
            _F["mh378_var_k"](A, B, Z, 1.5)


class TestBreakVol:
    def test_demo(self):
        assert _F["mh378_break_vol"](E, S, RHO, ALPHA, LIM) == pytest.approx(
            MSTAR)
        assert MSTAR == pytest.approx(LIM / VARB)

    def test_gia_rotto(self):
        m = _F["mh378_break_vol"](E, S, RHO, ALPHA, VARB / 2.0)
        assert m == pytest.approx(0.5)
        assert m < 1.0

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_break_vol"](E, S, RHO, ALPHA, 0.0)

    def test_var_nullo_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_break_vol"](E, (0.0, 0.0, 0.0), RHO, ALPHA, LIM)


class TestBreakCorr:
    def test_demo_none(self):
        # con LIM serve k* > 1: nemmeno la correlazione piena rompe
        assert _F["mh378_break_corr"](E, S, RHO, ALPHA, LIM) is None

    def test_k2_forma_chiusa(self):
        A, B = _F["mh378_AB"](E, S, RHO)
        att = ((LIM2 / Z) ** 2 - A) / B
        k = _F["mh378_break_corr"](E, S, RHO, ALPHA, LIM2)
        assert k == pytest.approx(KSTAR2)
        assert k == pytest.approx(att)
        assert 0.0 < k < 1.0

    def test_k2_rompe_davvero(self):
        k = _F["mh378_break_corr"](E, S, RHO, ALPHA, LIM2)
        rp = tuple((1.0 - k) * r + k for r in RHO)
        assert _F["mh378_var_p"](E, S, rp, ALPHA) == pytest.approx(LIM2)

    def test_gia_rotto_negativo(self):
        k = _F["mh378_break_corr"](E, S, RHO, ALPHA, VARB / 2.0)
        assert k < 0.0

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh378_break_corr"](E, S, RHO, ALPHA, -5.0)


class TestVerdetto:
    def test_rotto(self):
        assert _F["mh378_verdetto"](VARB, VARB / 2.0, 0.5, -0.3).startswith(
            "ROTTO")

    def test_fragile(self):
        assert _F["mh378_verdetto"](VARB, LIM, 1.5, None).startswith(
            "FRAGILE")

    def test_moderato(self):
        assert _F["mh378_verdetto"](VARB, LIM, 2.5, 0.4).startswith(
            "MODERATO")

    def test_resiliente(self):
        assert _F["mh378_verdetto"](VARB, LIM, 3.0, None).startswith(
            "RESILIENTE")

    def test_bordi(self):
        assert _F["mh378_verdetto"](VARB, LIM, 1.0, None).startswith(
            "FRAGILE")
        assert _F["mh378_verdetto"](VARB, LIM, 2.0, None).startswith(
            "MODERATO")
        assert _F["mh378_verdetto"](VARB, LIM, 2.9999, None).startswith(
            "MODERATO")


class TestReverse:
    def _b(self):
        return _F["mh378_reverse"](E, S, RHO, ALPHA, LIM)

    def test_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["sigma_p"] == pytest.approx(SIGP)
        assert b["var_base"] == pytest.approx(VARB)
        assert b["m_star"] == pytest.approx(MSTAR)
        assert b["k_star"] is None
        assert b["limite"] == pytest.approx(LIM)
        assert b["verdetto"].startswith("MODERATO")

    def test_coerenza(self):
        b = self._b()
        assert b["var_base"] == pytest.approx(b["z"] * b["sigma_p"])
        assert b["m_star"] == pytest.approx(b["limite"] / b["var_base"])
        assert b["A"] == pytest.approx(b["sigma_p"] ** 2)

    def test_k2_non_none(self):
        b = _F["mh378_reverse"](E, S, RHO, ALPHA, LIM2)
        assert b["k_star"] == pytest.approx(KSTAR2)
