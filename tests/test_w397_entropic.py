"""Test tab397 '🔀 Entropic risk measure: avversione esponenziale al rischio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh397_num", "mh397_check_gamma", "mh397_check_alpha",
           "mh397_rho_chiusa", "mh397_rho_quad", "mh397_var_chiusa",
           "mh397_es_chiusa", "mh397_gamma_target", "mh397_benchmarks",
           "mh397_verdetto", "mh397_mappa")

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
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
GAMMA = 2e-05
RHO = 1000.0
VAR = 19599.639845400536
ES = 23378.027922014157
GT = 0.00046756055844028306


class TestRegistry397:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 596
        assert "tab397" in dvars
        assert "tab397" in withs

    def test_titoli_allineati_392_393_394_395_396_397(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397

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
        assert _F["mh397_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](float("inf"), "x")


class TestCheckGamma:
    @pytest.mark.parametrize("g", [0.0, 2e-5, 1e-3])
    def test_gamma_ok(self, g):
        assert _F["mh397_check_gamma"](g) == g

    @pytest.mark.parametrize("g", [-1e-6, -1.0, True, False, "0.1", None,
                                   float("nan"), float("inf")])
    def test_gamma_ko(self, g):
        with pytest.raises(ValueError):
            _F["mh397_check_gamma"](g)


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh397_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh397_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_check_alpha"](float("nan"))


class TestRhoChiusa:
    def test_demo(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, GAMMA) == RHO

    def test_demo_sotto_var(self):
        assert RHO < VAR

    def test_formula(self):
        assert abs(_F["mh397_rho_chiusa"](MU, SIG, GAMMA) -
                   (MU + 0.5 * GAMMA * SIG * SIG)) < 1e-9

    def test_gamma_zero_media(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, 0.0) == MU

    def test_sig_zero(self):
        assert _F["mh397_rho_chiusa"](2000.0, 0.0, GAMMA) == 2000.0

    def test_monotonia_crescente_in_gamma(self):
        rs = [_F["mh397_rho_chiusa"](MU, SIG, g)
              for g in (0.0, 1e-5, 2e-5, 5e-5, 1e-4)]
        assert all(b > a for a, b in zip(rs, rs[1:]))

    def test_traslazione(self):
        assert abs(_F["mh397_rho_chiusa"](5000.0, SIG, GAMMA) -
                   (RHO + 5000.0)) < 1e-6

    def test_scaling_quadratico_in_sig(self):
        assert abs(_F["mh397_rho_chiusa"](MU, 2.0 * SIG, GAMMA) -
                   4.0 * RHO) / RHO < 1e-9

    def test_deterministico(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, GAMMA) == \
            _F["mh397_rho_chiusa"](MU, SIG, GAMMA)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_chiusa"](MU, -1.0, GAMMA)

    def test_gamma_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_chiusa"](MU, SIG, -0.1)


class TestRhoQuad:
    def test_vs_chiusa(self):
        rq = _F["mh397_rho_quad"](MU, SIG, GAMMA)
        assert abs(rq - RHO) / RHO < 1e-6

    def test_gamma_zero(self):
        assert _F["mh397_rho_quad"](MU, SIG, 0.0) == MU

    def test_sig_zero(self):
        assert _F["mh397_rho_quad"](2000.0, 0.0, GAMMA) == 2000.0

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_quad"](MU, SIG, GAMMA, n=4)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_quad"](MU, -1.0, GAMMA)


class TestGammaTarget:
    def test_positivo(self):
        assert GT > 0.0

    def test_eguaglia_es(self):
        assert abs(_F["mh397_rho_chiusa"](MU, SIG, GT) - ES) / ES < 1e-9

    def test_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh397_gamma_target"](SIG, ALPHA) -
                   2.0 * phi / ((1.0 - ALPHA) * SIG)) < 1e-18

    def test_sig_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_gamma_target"](0.0, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_gamma_target"](SIG, 2.0)


class TestEsVarChiusa:
    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh397_var_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * z)) < 1e-9

    def test_es_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh397_es_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_var_chiusa"](MU, -1.0, ALPHA)
        with pytest.raises(ValueError):
            _F["mh397_es_chiusa"](MU, -1.0, ALPHA)


class TestBenchmarks:
    def test_demo(self):
        b = _F["mh397_benchmarks"](MU, SIG, ALPHA)
        assert b["var"] == VAR
        assert b["es"] == ES

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_benchmarks"](MU, -1.0, ALPHA)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh397_verdetto"](RHO, VAR, ES).startswith("SOTTO-VaR")

    def test_bordi(self):
        assert _F["mh397_verdetto"](VAR, VAR, ES).startswith("TRA VaR")
        assert _F["mh397_verdetto"](ES, VAR, ES).startswith("TRA VaR")
        assert _F["mh397_verdetto"](VAR - 1.0, VAR,
                                    ES).startswith("SOTTO-VaR")
        assert _F["mh397_verdetto"](ES + 1.0, VAR,
                                    ES).startswith("OLTRE ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_verdetto"](float("nan"), VAR, ES)


class TestMappa:
    def _b(self):
        return _F["mh397_mappa"](MU, SIG, GAMMA, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA and b["gamma"] == GAMMA
        assert b["rho"] == RHO
        assert b["var"] == VAR and b["es"] == ES
        assert b["gamma_target"] == GT
        assert b["verdetto"].startswith("SOTTO-VaR")

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_mappa"](MU, SIG, GAMMA, 2.0)
