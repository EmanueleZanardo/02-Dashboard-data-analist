"""Test tab381 'Component VaR: attribution del VaR per asset': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh381_num", "mh381_z", "mh381_sigma_p", "mh381_var_base",
           "mh381_cov_e", "mh381_mvar", "mh381_cvar",
           "mh381_concentration", "mh381_verdetto", "mh381_mappa")

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
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
E = (10000.0, 8000.0, 6000.0)
S = (0.15, 0.2, 0.1)
RHO = (0.6, 0.3, 0.4)
ALPHA = 0.95
Z = 1.6448536269514715
SIGP = 3059.0848304680926
VARB = 5031.746778547669
CE = (396.0, 548.0, 169.0)
MV = (0.21292709171883706, 0.2946566824796028, 0.09087040025374611)
CV = (2129.2709171883707, 2357.2534598368225, 545.2224015224766)
CONC = 0.46847617012182097


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry381:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 767
        assert "tab381" in dvars
        assert "tab381" in withs

    def test_titoli_allineati_376_377_378_379_380_381(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377
        assert titoli[dvars.index("tab378")] == TITLE378
        assert titoli[dvars.index("tab379")] == TITLE379
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh381_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_num"](float("inf"), "x")


class TestZ:
    def test_z_demo(self):
        assert _F["mh381_z"](ALPHA) == pytest.approx(Z)

    def test_z_95_forma_nota(self):
        assert _F["mh381_z"](0.95) == pytest.approx(1.6448536269514715)

    def test_z_99_forma_nota(self):
        assert _F["mh381_z"](0.99) == pytest.approx(2.3263478740408408)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_z"](0.4)
        with pytest.raises(ValueError):
            _F["mh381_z"](1.0)


class TestSigmaP:
    def test_demo(self):
        assert _F["mh381_sigma_p"](E, S, RHO) == pytest.approx(SIGP)

    def test_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        var = (se[0] ** 2 + se[1] ** 2 + se[2] ** 2
               + 2.0 * (se[0] * se[1] * r12 + se[0] * se[2] * r13
                        + se[1] * se[2] * r23))
        assert _F["mh381_sigma_p"](E, S, RHO) == pytest.approx(
            math.sqrt(var))

    def test_demo_var_9358000(self):
        assert SIGP ** 2 == pytest.approx(9358000.0, rel=1e-9)

    def test_zero_vol(self):
        assert _F["mh381_sigma_p"](E, (0.0, 0.0, 0.0), RHO) == pytest.approx(
            0.0)

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_sigma_p"](E, (-0.1, S[1], S[2]), RHO)

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_sigma_p"](E, S, (1.5, RHO[1], RHO[2]))


class TestVarBase:
    def test_demo(self):
        assert _F["mh381_var_base"](SIGP, Z) == pytest.approx(VARB)

    def test_forma_chiusa(self):
        assert VARB == pytest.approx(Z * SIGP)

    def test_zero_sigma(self):
        assert _F["mh381_var_base"](0.0, Z) == pytest.approx(0.0)

    def test_z_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_var_base"](SIGP, 0.0)
        with pytest.raises(ValueError):
            _F["mh381_var_base"](SIGP, -1.0)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_var_base"](-1.0, Z)


class TestCovE:
    def test_demo(self):
        ce = _F["mh381_cov_e"](E, S, RHO)
        assert ce[0] == pytest.approx(CE[0])
        assert ce[1] == pytest.approx(CE[1])
        assert ce[2] == pytest.approx(CE[2])

    def test_forma_chiusa(self):
        # (C E)_i = s_i * (s_i E_i + s_j rho_ij E_j + s_k rho_ik E_k)
        r12, r13, r23 = RHO
        rmat = ((1.0, r12, r13), (r12, 1.0, r23), (r13, r23, 1.0))
        ce = _F["mh381_cov_e"](E, S, RHO)
        for i in range(3):
            exp = S[i] * sum(S[j] * rmat[i][j] * E[j] for j in range(3))
            assert ce[i] == pytest.approx(exp)

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_cov_e"](E, (-0.1, S[1], S[2]), RHO)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_cov_e"]((1.0, 2.0), S, RHO)


class TestMvar:
    def test_demo(self):
        mv = _F["mh381_mvar"](E, S, RHO, SIGP, Z)
        assert mv[0] == pytest.approx(MV[0])
        assert mv[1] == pytest.approx(MV[1])
        assert mv[2] == pytest.approx(MV[2])

    def test_forma_chiusa(self):
        mv = _F["mh381_mvar"](E, S, RHO, SIGP, Z)
        for i in range(3):
            assert mv[i] == pytest.approx(Z * CE[i] / SIGP)

    def test_sigma_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_mvar"](E, S, RHO, 0.0, Z)

    def test_z_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_mvar"](E, S, RHO, SIGP, 0.0)


class TestCvar:
    def test_demo(self):
        cv = _F["mh381_cvar"](E, MV)
        assert cv[0] == pytest.approx(CV[0])
        assert cv[1] == pytest.approx(CV[1])
        assert cv[2] == pytest.approx(CV[2])

    def test_forma_chiusa(self):
        cv = _F["mh381_cvar"](E, MV)
        for i in range(3):
            assert cv[i] == pytest.approx(E[i] * MV[i])

    def test_eulero(self):
        # decomposizione di Eulero: somma dei Component VaR = VaR
        cv = _F["mh381_cvar"](E, MV)
        assert sum(cv) == pytest.approx(VARB)

    def test_quote_sommano_1(self):
        cv = _F["mh381_cvar"](E, MV)
        assert sum(c / VARB for c in cv) == pytest.approx(1.0)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_cvar"](E, (MV[0], MV[1]))


class TestConcentration:
    def test_demo(self):
        assert _F["mh381_concentration"](CV, VARB) == pytest.approx(CONC)

    def test_forma_chiusa(self):
        assert CONC == pytest.approx(max(CV) / VARB)

    def test_demo_bilanciato(self):
        assert 0.35 <= CONC < 0.50

    def test_var_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_concentration"](CV, 0.0)
        with pytest.raises(ValueError):
            _F["mh381_concentration"](CV, -5.0)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_concentration"]((CV[0], CV[1]), VARB)


class TestVerdetto:
    def test_diversificato(self):
        assert _F["mh381_verdetto"](0.0).startswith("DIVERSIFICATO")
        assert _F["mh381_verdetto"](0.3499).startswith("DIVERSIFICATO")

    def test_bilanciato(self):
        assert _F["mh381_verdetto"](0.35).startswith("BILANCIATO")
        assert _F["mh381_verdetto"](0.4999).startswith("BILANCIATO")

    def test_concentrato(self):
        assert _F["mh381_verdetto"](0.50).startswith("CONCENTRATO")
        assert _F["mh381_verdetto"](0.6499).startswith("CONCENTRATO")

    def test_dominato(self):
        assert _F["mh381_verdetto"](0.65).startswith("DOMINATO")
        assert _F["mh381_verdetto"](0.9).startswith("DOMINATO")

    def test_demo_bilanciato(self):
        assert _F["mh381_verdetto"](CONC).startswith("BILANCIATO")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh381_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh381_verdetto"](-0.1)


class TestMappa:
    def _b(self):
        return _F["mh381_mappa"](E, S, RHO, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["sigma_p"] == pytest.approx(SIGP)
        assert b["var_base"] == pytest.approx(VARB)
        assert b["ce"] == (pytest.approx(CE[0]), pytest.approx(CE[1]),
                           pytest.approx(CE[2]))
        assert b["mvar"] == (pytest.approx(MV[0]), pytest.approx(MV[1]),
                             pytest.approx(MV[2]))
        assert b["cvar"] == (pytest.approx(CV[0]), pytest.approx(CV[1]),
                             pytest.approx(CV[2]))
        assert b["conc"] == pytest.approx(CONC)
        assert b["verdetto"].startswith("BILANCIATO")

    def test_coerenza(self):
        b = self._b()
        assert b["var_base"] == pytest.approx(b["z"] * b["sigma_p"])
        assert sum(b["cvar"]) == pytest.approx(b["var_base"])
        assert b["conc"] == pytest.approx(max(b["cvar"]) / b["var_base"])
        for i in range(3):
            assert b["mvar"][i] == pytest.approx(
                b["z"] * b["ce"][i] / b["sigma_p"])
            assert b["cvar"][i] == pytest.approx(b["E"][i] * b["mvar"][i])
        assert b["alpha"] == pytest.approx(ALPHA)

    def test_echo_input(self):
        b = self._b()
        assert b["E"] == E
        assert b["s"] == S
        assert b["rho"] == RHO
