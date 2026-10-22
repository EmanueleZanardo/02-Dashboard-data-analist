"""Test tab383 'Jump VaR: VaR con salti di prezzo (Merton)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh383_num", "mh383_phi", "mh383_npdf", "mh383_ppf",
           "mh383_kappa", "mh383_pesi", "mh383_momenti", "mh383_cdf_ret",
           "mh383_pdf_ret", "mh383_q_jump", "mh383_var_jump",
           "mh383_var_diff", "mh383_es_jump", "mh383_es_diff",
           "mh383_p_salto", "mh383_quota", "mh383_verdetto", "mh383_mappa")

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
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
E = 100000.0
MU = 0.0
SIG = 0.25
LAM = 3.0
MUJ = -0.08
SIGJ = 0.12
T = 0.003968253968253968
ALPHA = 0.99
QJ = 0.043076861225698995
VARJ = 4307.686122569899
VARD = 3592.467147999595
ESJ = 12595.977697951392
ESD = 4126.131481340088
QUOTA = 0.16603321463533555
PSALTO = 0.011834180588984777


def _pesi_demo():
    return _F["mh383_pesi"](LAM, T)


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry383:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 635
        assert "tab383" in dvars
        assert "tab383" in withs

    def test_titoli_allineati_378_379_380_381_382_383(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab378")] == TITLE378
        assert titoli[dvars.index("tab379")] == TITLE379
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh383_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_num"](float("inf"), "x")


class TestPhiNpdfPpf:
    def test_phi_zero(self):
        assert _F["mh383_phi"](0.0) == pytest.approx(0.5)

    def test_phi_nota(self):
        assert _F["mh383_phi"](1.6448536269514715) == pytest.approx(0.95)

    def test_npdf_zero(self):
        assert _F["mh383_npdf"](0.0) == pytest.approx(1.0 / math.sqrt(
            2.0 * math.pi))

    def test_npdf_simmetria(self):
        assert _F["mh383_npdf"](1.5) == pytest.approx(_F["mh383_npdf"](-1.5))

    def test_ppf_nota(self):
        assert _F["mh383_ppf"](0.975) == pytest.approx(1.959963984540054)

    def test_ppf_inversa_phi(self):
        for p in (0.01, 0.25, 0.9):
            assert _F["mh383_phi"](_F["mh383_ppf"](p)) == pytest.approx(p)

    def test_ppf_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_ppf"](0.0)
        with pytest.raises(ValueError):
            _F["mh383_ppf"](1.0)


class TestKappa:
    def test_zero(self):
        assert _F["mh383_kappa"](0.0, 0.0) == pytest.approx(0.0)

    def test_forma_chiusa(self):
        assert _F["mh383_kappa"](MUJ, SIGJ) == pytest.approx(
            math.exp(MUJ + 0.5 * SIGJ ** 2) - 1.0)

    def test_demo_negativo(self):
        assert _F["mh383_kappa"](MUJ, SIGJ) < 0.0

    def test_sigj_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_kappa"](MUJ, -0.1)


class TestPesi:
    def test_somma_uno(self):
        assert sum(_pesi_demo()) == pytest.approx(1.0)

    def test_w0_poisson(self):
        assert _pesi_demo()[0] == pytest.approx(math.exp(-LAM * T))

    def test_lam_zero_degenere(self):
        assert _F["mh383_pesi"](0.0, T) == [1.0]

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_pesi"](-1.0, T)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_pesi"](LAM, 0.0)


class TestMomenti:
    def test_k0_diffusione(self):
        kap = math.exp(MUJ + 0.5 * SIGJ ** 2) - 1.0
        m, s = _F["mh383_momenti"](MU, SIG, LAM, MUJ, SIGJ, T, 0)
        assert m == pytest.approx((MU - LAM * kap - 0.5 * SIG ** 2) * T)
        assert s == pytest.approx(SIG * math.sqrt(T))

    def test_k1_sposta_media(self):
        m0, _ = _F["mh383_momenti"](MU, SIG, LAM, MUJ, SIGJ, T, 0)
        m1, s1 = _F["mh383_momenti"](MU, SIG, LAM, MUJ, SIGJ, T, 1)
        assert m1 == pytest.approx(m0 + MUJ)
        assert s1 ** 2 == pytest.approx(SIG ** 2 * T + SIGJ ** 2)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_momenti"](MU, SIG, LAM, MUJ, SIGJ, T, -1)
        with pytest.raises(ValueError):
            _F["mh383_momenti"](MU, SIG, LAM, MUJ, SIGJ, T, 1.5)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_momenti"](MU, -0.1, LAM, MUJ, SIGJ, T, 0)


class TestCdf:
    def test_limiti(self):
        w = _pesi_demo()
        assert _F["mh383_cdf_ret"](-10.0, MU, SIG, LAM, MUJ, SIGJ, T, w) \
            == pytest.approx(0.0)
        assert _F["mh383_cdf_ret"](10.0, MU, SIG, LAM, MUJ, SIGJ, T, w) \
            == pytest.approx(1.0)

    def test_monotona(self):
        w = _pesi_demo()
        xs = [-0.2, -0.1, -0.05, 0.0, 0.05]
        vs = [_F["mh383_cdf_ret"](x, MU, SIG, LAM, MUJ, SIGJ, T, w)
              for x in xs]
        assert all(b >= a for a, b in zip(vs, vs[1:]))

    def test_lam_zero_e_normale(self):
        w = _F["mh383_pesi"](0.0, T)
        m, s = _F["mh383_momenti"](MU, SIG, 0.0, MUJ, SIGJ, T, 0)
        assert _F["mh383_cdf_ret"](m, MU, SIG, 0.0, MUJ, SIGJ, T, w) \
            == pytest.approx(0.5)

    def test_pesi_vuoti_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_cdf_ret"](0.0, MU, SIG, LAM, MUJ, SIGJ, T, [])

    def test_pdf_integra_uno(self):
        w = _pesi_demo()
        xs = [-0.5 + i * 0.01 for i in range(101)]
        ys = [_F["mh383_pdf_ret"](x, MU, SIG, LAM, MUJ, SIGJ, T, w)
              for x in xs]
        area = sum(0.5 * (a + b) * 0.01 for a, b in zip(ys, ys[1:]))
        assert area == pytest.approx(1.0, abs=1e-3)


class TestQJump:
    def test_demo_residuo_bisezione(self):
        w = _pesi_demo()
        assert abs(_F["mh383_cdf_ret"](
            -QJ, MU, SIG, LAM, MUJ, SIGJ, T, w) - (1.0 - ALPHA)) < 1e-9

    def test_demo_positivo(self):
        assert QJ > 0.0

    def test_lam_zero_chiusa(self):
        q0 = _F["mh383_q_jump"](MU, SIG, 0.0, MUJ, SIGJ, T, ALPHA)
        kap = math.exp(MUJ + 0.5 * SIGJ ** 2) - 1.0
        m0 = (MU - 0.5 * SIG ** 2) * T
        s0 = SIG * math.sqrt(T)
        assert q0 == pytest.approx(max(0.0, -(m0 + s0 * _F["mh383_ppf"](
            1.0 - ALPHA))))

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_q_jump"](MU, SIG, LAM, MUJ, SIGJ, T, 0.4)


class TestVarJump:
    def test_demo(self):
        assert _F["mh383_var_jump"](
            E, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA) == pytest.approx(VARJ)

    def test_demo_forma(self):
        assert VARJ == pytest.approx(E * QJ)

    def test_sopra_diffusione(self):
        assert VARJ >= VARD

    def test_E_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_var_jump"](0.0, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA)
        with pytest.raises(ValueError):
            _F["mh383_var_jump"](-100.0, MU, SIG, LAM, MUJ, SIGJ, T,
                                 ALPHA)


class TestVarDiff:
    def test_demo(self):
        assert _F["mh383_var_diff"](
            E, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA) == pytest.approx(VARD)

    def test_demo_chiusa(self):
        kap = math.exp(MUJ + 0.5 * SIGJ ** 2) - 1.0
        m0 = (MU - LAM * kap - 0.5 * SIG ** 2) * T
        s0 = SIG * math.sqrt(T)
        assert VARD == pytest.approx(E * max(
            0.0, -(m0 + s0 * _F["mh383_ppf"](1.0 - ALPHA))))

    def test_E_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_var_diff"](0.0, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA)


class TestEsJump:
    def test_demo(self):
        assert _F["mh383_es_jump"](
            E, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA) == pytest.approx(ESJ)

    def test_sopra_var(self):
        assert ESJ >= VARJ

    def test_quadratura_indipendente(self):
        w = _pesi_demo()
        n = 4000
        a, b = -1.0, -QJ
        h = (b - a) / n
        tot = 0.0
        for i in range(n + 1):
            x = a + i * h
            fx = (-x) * _F["mh383_pdf_ret"](x, MU, SIG, LAM, MUJ, SIGJ,
                                            T, w)
            tot += (0.5 if i in (0, n) else 1.0) * fx
        es_num = E * tot * h / (1.0 - ALPHA)
        assert es_num == pytest.approx(ESJ, rel=1e-3)

    def test_E_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_es_jump"](0.0, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA)


class TestEsDiff:
    def test_demo(self):
        assert _F["mh383_es_diff"](
            E, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA) == pytest.approx(ESD)

    def test_sopra_var_diff(self):
        assert ESD >= VARD

    def test_demo_chiusa(self):
        kap = math.exp(MUJ + 0.5 * SIGJ ** 2) - 1.0
        m0 = (MU - LAM * kap - 0.5 * SIG ** 2) * T
        s0 = SIG * math.sqrt(T)
        q = max(0.0, -(m0 + s0 * _F["mh383_ppf"](1.0 - ALPHA)))
        d = (-q - m0) / s0
        assert ESD == pytest.approx(
            E * (-m0 * _F["mh383_phi"](d) + s0 * _F["mh383_npdf"](d)) /
            (1.0 - ALPHA))


class TestPSalto:
    def test_demo(self):
        assert _F["mh383_p_salto"](LAM, T) == pytest.approx(PSALTO)

    def test_forma_chiusa(self):
        assert PSALTO == pytest.approx(1.0 - math.exp(-LAM * T))

    def test_lam_zero(self):
        assert _F["mh383_p_salto"](0.0, T) == pytest.approx(0.0)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_p_salto"](-1.0, T)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_p_salto"](LAM, 0.0)


class TestQuota:
    def test_demo(self):
        assert _F["mh383_quota"](VARJ, VARD) == pytest.approx(QUOTA)

    def test_forma_chiusa(self):
        assert QUOTA == pytest.approx((VARJ - VARD) / VARJ)

    def test_demo_rilevante(self):
        assert 0.15 <= QUOTA < 0.30

    def test_varj_zero(self):
        assert _F["mh383_quota"](0.0, VARD) == 0.0

    def test_vard_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_quota"](VARJ, -1.0)


class TestVerdetto:
    def test_trascurabile(self):
        assert _F["mh383_verdetto"](0.0).startswith("TRASCURABILE")
        assert _F["mh383_verdetto"](0.0499).startswith("TRASCURABILE")

    def test_moderato(self):
        assert _F["mh383_verdetto"](0.05).startswith("MODERATO")
        assert _F["mh383_verdetto"](0.1499).startswith("MODERATO")

    def test_rilevante(self):
        assert _F["mh383_verdetto"](0.15).startswith("RILEVANTE")
        assert _F["mh383_verdetto"](0.2999).startswith("RILEVANTE")

    def test_dominante(self):
        assert _F["mh383_verdetto"](0.30).startswith("DOMINANTE")
        assert _F["mh383_verdetto"](0.9).startswith("DOMINANTE")

    def test_demo_rilevante(self):
        assert _F["mh383_verdetto"](QUOTA).startswith("RILEVANTE")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh383_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh383_verdetto"](-0.1)


class TestMappa:
    def _b(self):
        return _F["mh383_mappa"](E, MU, SIG, LAM, MUJ, SIGJ, T, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["var_jump"] == pytest.approx(VARJ)
        assert b["var_diff"] == pytest.approx(VARD)
        assert b["es_jump"] == pytest.approx(ESJ)
        assert b["es_diff"] == pytest.approx(ESD)
        assert b["p_salto"] == pytest.approx(PSALTO)
        assert b["quota"] == pytest.approx(QUOTA)
        assert b["verdetto"].startswith("RILEVANTE")

    def test_coerenza(self):
        b = self._b()
        assert b["quota"] == pytest.approx(
            (b["var_jump"] - b["var_diff"]) / b["var_jump"])
        assert b["var_jump"] >= b["var_diff"]
        assert b["es_jump"] >= b["var_jump"]
        assert b["es_diff"] >= b["var_diff"]
        assert b["p_salto"] == pytest.approx(1.0 - math.exp(-b["lam"] *
                                                           b["t"]))
        assert b["alpha"] == pytest.approx(ALPHA)

    def test_echo_input(self):
        b = self._b()
        assert b["E"] == E
        assert b["mu"] == MU
        assert b["sigma"] == SIG
        assert b["lam"] == LAM
        assert b["mu_j"] == MUJ
        assert b["sig_j"] == SIGJ
        assert b["t"] == T
