"""Test tab394 '📐⚖ Expectile: la misura di rischio elicitabile e coerente': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh394_num", "mh394_check_alpha", "mh394_up_down",
           "mh394_expectile", "mh394_expectile_quad", "mh394_var",
           "mh394_es", "mh394_ratio", "mh394_verdetto", "mh394_mappa")

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
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
EXP = 13983.771246759594
VAR = 19599.639845400536
ES = 23378.027922014157
RATIO = 0.7134708268652792


class TestRegistry394:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 796
        assert "tab394" in dvars
        assert "tab394" in withs

    def test_titoli_allineati_389_390_391_392_393_394(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394

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
        assert _F["mh394_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](float("inf"), "x")


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh394_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh394_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_check_alpha"](float("nan"))


class TestUpDown:
    def test_chiuse_demo(self):
        from statistics import NormalDist
        up, down = _F["mh394_up_down"](MU, SIG, EXP)
        z = (EXP - MU) / SIG
        Phi = NormalDist().cdf(z)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(up - SIG * (phi - z * (1.0 - Phi))) < 1e-9
        assert abs(down - SIG * (phi + z * Phi)) < 1e-9

    def test_foc_demo(self):
        up, down = _F["mh394_up_down"](MU, SIG, EXP)
        assert abs(ALPHA * up - (1.0 - ALPHA) * down) < 1e-9 * SIG

    def test_sig_zero(self):
        assert _F["mh394_up_down"](2000.0, 0.0, 5000.0) == (0.0, 3000.0)
        assert _F["mh394_up_down"](2000.0, 0.0, 1000.0) == (1000.0, 0.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_up_down"](MU, -1.0, EXP)


class TestExpectile:
    def test_demo(self):
        assert _F["mh394_expectile"](MU, SIG, ALPHA) == EXP

    def test_alpha_mezzo_e_media(self):
        assert _F["mh394_expectile"](MU, SIG, 0.5) == MU
        assert _F["mh394_expectile"](1234.5, SIG, 0.5) == 1234.5

    def test_monotonia_alpha(self):
        assert _F["mh394_expectile"](MU, SIG, 0.90) < \
            _F["mh394_expectile"](MU, SIG, 0.95) < \
            _F["mh394_expectile"](MU, SIG, 0.99)

    def test_minore_del_var(self):
        assert EXP < VAR

    @pytest.mark.parametrize("pt", [(0.0, 10000.0, 0.975),
                                    (2000.0, 8000.0, 0.95)])
    def test_quad_crosscheck(self, pt):
        mu, sg, aa = pt
        c = _F["mh394_expectile"](mu, sg, aa)
        q = _F["mh394_expectile_quad"](mu, sg, aa)
        assert abs(c - q) / max(abs(c), 1e-12) < 1e-4

    def test_gerarchia_livelli(self):
        for aa in (0.90, 0.95, 0.975, 0.99):
            e = _F["mh394_expectile"](MU, SIG, aa)
            v = _F["mh394_var"](MU, SIG, aa)
            s = _F["mh394_es"](MU, SIG, aa)
            assert e < v < s

    def test_sig_zero(self):
        assert _F["mh394_expectile"](2000.0, 0.0, ALPHA) == 2000.0
        assert _F["mh394_expectile_quad"](2000.0, 0.0, ALPHA) == 2000.0

    def test_traslazione(self):
        assert abs(_F["mh394_expectile"](5000.0, SIG, ALPHA) -
                   (EXP + 5000.0)) < 1e-6

    def test_scaling(self):
        assert abs(_F["mh394_expectile"](MU, 2.0 * SIG, ALPHA) -
                   2.0 * EXP) < 1e-6

    def test_deterministico(self):
        assert _F["mh394_expectile"](MU, SIG, ALPHA) == \
            _F["mh394_expectile"](MU, SIG, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](MU, SIG, 1.5)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](MU, -1.0, ALPHA)

    def test_mu_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](float("nan"), SIG, ALPHA)


class TestVarEs:
    def test_demo_var(self):
        assert _F["mh394_var"](MU, SIG, ALPHA) == VAR

    def test_demo_es(self):
        assert _F["mh394_es"](MU, SIG, ALPHA) == ES

    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh394_var"](MU, SIG, ALPHA) - (MU + SIG * z)) < 1e-9

    def test_es_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh394_es"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_var"](MU, -1.0, ALPHA)


class TestRatioVerdetto:
    def test_demo_ratio(self):
        assert _F["mh394_ratio"](EXP, VAR) == RATIO

    def test_demo_verdetto(self):
        assert _F["mh394_verdetto"](RATIO).startswith("MENO CONSERVATIVO")

    def test_bordi(self):
        assert _F["mh394_verdetto"](1.0).startswith("CONSERVATIVO")
        assert _F["mh394_verdetto"](1.5).startswith("CONSERVATIVO")
        assert _F["mh394_verdetto"](0.99).startswith("INTERMEDIO")
        assert _F["mh394_verdetto"](0.85).startswith("INTERMEDIO")
        assert _F["mh394_verdetto"](0.849).startswith("MENO CONSERVATIVO")
        assert _F["mh394_verdetto"](0.0).startswith("MENO CONSERVATIVO")

    def test_var_non_positivo_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_ratio"](100.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh394_ratio"](100.0, -5.0)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh394_mappa"](MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["expectile"] == EXP
        assert b["var"] == VAR
        assert b["es"] == ES
        assert b["ratio"] == RATIO
        assert b["verdetto"].startswith("MENO CONSERVATIVO")

    def test_coerenza(self):
        b = self._b()
        assert abs(b["ratio"] - b["expectile"] / b["var"]) < 1e-15

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_mappa"](MU, SIG, 2.0)
