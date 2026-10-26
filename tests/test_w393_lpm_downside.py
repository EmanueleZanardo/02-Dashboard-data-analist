"""Test tab393 '🎯📉 LPM: il rischio downside contro un target': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh393_num", "mh393_check_n", "mh393_lpm", "mh393_lpm_quad",
           "mh393_upm", "mh393_share", "mh393_verdetto", "mh393_mappa")

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
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
MU = 0.0
SIG = 10000.0
TAU = 0.0
N = 2
LPM2 = 50000000.0
LPM0 = 0.5
LPM1 = 3989.422804014327
SHARE = 0.5


class TestRegistry393:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 724
        assert "tab393" in dvars
        assert "tab393" in withs

    def test_titoli_allineati_388_389_390_391_392_393(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab388")] == TITLE388
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393

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
        assert _F["mh393_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](float("inf"), "x")


class TestCheckN:
    @pytest.mark.parametrize("n", [0, 1, 2, 3])
    def test_n_ok(self, n):
        assert _F["mh393_check_n"](n) == n

    @pytest.mark.parametrize("n", [-1, 4, 5, True, False, 1.5, "2", None])
    def test_n_ko(self, n):
        with pytest.raises(ValueError):
            _F["mh393_check_n"](n)


class TestLpm:
    def test_demo_lpm2(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 2) == LPM2

    def test_demo_lpm0(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 0) == LPM0

    def test_demo_lpm1(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 1) == LPM1

    def test_forma_chiusa_n1(self):
        from statistics import NormalDist
        d = (TAU - MU) / SIG
        Phi = NormalDist().cdf(d)
        phi = math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh393_lpm"](MU, SIG, TAU, 1) -
                   SIG * (d * Phi + phi)) < 1e-9

    def test_forma_chiusa_n3(self):
        from statistics import NormalDist
        d = (TAU - MU) / SIG
        Phi = NormalDist().cdf(d)
        phi = math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh393_lpm"](MU, SIG, TAU, 3) -
                   SIG ** 3 * ((d ** 3 + 3.0 * d) * Phi +
                               (d * d + 2.0) * phi)) < 1e-9

    @pytest.mark.parametrize("n", [0, 1, 2, 3])
    @pytest.mark.parametrize("pt", [(0.0, 10000.0, 0.0),
                                    (2000.0, 8000.0, 5000.0)])
    def test_quad_crosscheck(self, n, pt):
        mu, sg, ta = pt
        c = _F["mh393_lpm"](mu, sg, ta, n)
        q = _F["mh393_lpm_quad"](mu, sg, ta, n)
        assert abs(c - q) / max(abs(c), 1e-12) < 1e-6

    def test_monotonia_tau(self):
        assert _F["mh393_lpm"](MU, SIG, -5000.0, 2) < \
            _F["mh393_lpm"](MU, SIG, 0.0, 2) < \
            _F["mh393_lpm"](MU, SIG, 5000.0, 2)

    def test_lpm0_in_unit(self):
        assert 0.0 <= _F["mh393_lpm"](MU, SIG, TAU, 0) <= 1.0
        assert _F["mh393_lpm"](MU, SIG, 1e9, 0) > 0.999999
        assert _F["mh393_lpm"](MU, SIG, -1e9, 0) < 1e-6

    def test_sig_zero_n0(self):
        assert _F["mh393_lpm"](2000.0, 0.0, 1000.0, 0) == 1.0
        assert _F["mh393_lpm"](2000.0, 0.0, 3000.0, 0) == 0.0

    def test_sig_zero_n2(self):
        assert _F["mh393_lpm"](2000.0, 0.0, 5000.0, 2) == 3000.0 ** 2
        assert _F["mh393_lpm"](2000.0, 0.0, 1000.0, 2) == 0.0

    def test_traslazione(self):
        assert _F["mh393_lpm"](5000.0, SIG, 5000.0, 2) == \
            _F["mh393_lpm"](MU, SIG, TAU, 2)

    def test_scaling(self):
        assert _F["mh393_lpm"](MU, 2 * SIG, TAU, 2) == \
            4.0 * _F["mh393_lpm"](MU, SIG, TAU, 2)

    def test_deterministico(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 3) == \
            _F["mh393_lpm"](MU, SIG, TAU, 3)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, TAU, 4)

    def test_n_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, TAU, True)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, -1.0, TAU, 2)

    def test_tau_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, float("nan"), 2)

    def test_quad_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm_quad"](MU, SIG, TAU, 5)


class TestUpmShare:
    def test_simmetria(self):
        assert _F["mh393_upm"](MU, SIG, TAU) == \
            _F["mh393_lpm"](MU, SIG, TAU, 1)

    def test_demo_share(self):
        assert _F["mh393_share"](MU, SIG, TAU) == SHARE

    def test_share_banda(self):
        s = _F["mh393_share"](2000.0, 8000.0, 5000.0)
        assert 0.0 <= s <= 1.0

    def test_share_tau_alto(self):
        assert _F["mh393_share"](MU, SIG, 20000.0) > 0.9

    def test_share_tau_basso(self):
        assert _F["mh393_share"](MU, SIG, -20000.0) < 0.1

    def test_upm_sig_zero(self):
        assert _F["mh393_upm"](5000.0, 0.0, 2000.0) == 3000.0
        assert _F["mh393_upm"](5000.0, 0.0, 8000.0) == 0.0

    def test_share_degenere(self):
        assert _F["mh393_share"](2000.0, 0.0, 2000.0) == 0.5

    def test_upm_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_upm"](MU, -1.0, TAU)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh393_verdetto"](LPM0).startswith("TARGET BILANCIATO")

    def test_bordi(self):
        assert _F["mh393_verdetto"](0.30).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](0.3001).startswith("TARGET BILANCIATO")
        assert _F["mh393_verdetto"](0.60).startswith("TARGET BILANCIATO")
        assert _F["mh393_verdetto"](0.6001).startswith("TARGET AGGRESSIVO")
        assert _F["mh393_verdetto"](0.0).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](1.0).startswith("TARGET AGGRESSIVO")

    def test_clamp(self):
        assert _F["mh393_verdetto"](-0.5).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](1.5).startswith("TARGET AGGRESSIVO")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](float("nan"))

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](float("inf"))

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](True)


class TestMappa:
    def _b(self):
        return _F["mh393_mappa"](MU, SIG, TAU, N)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["tau"] == TAU and b["n"] == N
        assert b["lpm0"] == LPM0
        assert b["lpm1"] == LPM1
        assert b["lpm2"] == LPM2
        assert b["lpm_n"] == LPM2
        assert b["share"] == SHARE
        assert b["verdetto"].startswith("TARGET BILANCIATO")

    def test_coerenza(self):
        b = self._b()
        assert abs(b["down_std"] - math.sqrt(b["lpm2"])) < 1e-9
        assert abs(b["share"] - b["lpm1"] / (b["lpm1"] + b["upm1"])) < 1e-15
        assert b["lpm_n"] == b["lpm2"]

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_mappa"](MU, SIG, TAU, 7)
