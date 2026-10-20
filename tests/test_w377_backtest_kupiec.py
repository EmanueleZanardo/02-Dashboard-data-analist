"""Test tab377 'Backtest VaR di Kupiec: copertura e likelihood ratio': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh377_num", "mh377_z", "mh377_chi2_1_sf", "mh377_sim_gbm",
           "mh377_log_returns", "mh377_var_par", "mh377_kupiec",
           "mh377_basel_zone", "mh377_verdetto", "mh377_backtest")

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
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
S0 = 100.0
MU = 0.05
SIG = 0.2
N = 250
SEED = 7
ALPHA = 0.99
Z = 2.3263478740408408
SIGD = 0.012906200153838396
VARF = 0.030024311289827525
T = 4
LR = 0.7691383643858458
PV = 0.380483738238954
EXP = 2.500000000000002
ZONE = 'VERDE: 4 violazioni su 250 entro la soglia (4) - modello adeguato'
VERDETTO = "ACCETTABILE: il tasso di violazioni e' compatibile con il VaR (p >= 10%)"
P0 = 100.0
PN = 119.54918615981961
RET0 = -0.003116658079341123


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry377:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 588
        assert "tab377" in dvars
        assert "tab377" in withs

    def test_titoli_allineati_372_373_374_375_376_377(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh377_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](float("inf"), "x")


class TestZChi2:
    def test_z_demo(self):
        assert _F["mh377_z"](ALPHA) == pytest.approx(Z)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_z"](0.5)

    def test_chi2_sf_zero(self):
        assert _F["mh377_chi2_1_sf"](0.0) == pytest.approx(1.0)

    def test_chi2_sf_forma_chiusa(self):
        assert _F["mh377_chi2_1_sf"](1.0) == pytest.approx(
            math.erfc(math.sqrt(0.5)))

    def test_chi2_sf_decresce(self):
        assert _F["mh377_chi2_1_sf"](0.5) > _F["mh377_chi2_1_sf"](5.0)

    def test_chi2_sf_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_chi2_1_sf"](-0.1)


class TestSim:
    def test_demo_struttura(self):
        p = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        assert len(p) == N + 1
        assert p[0] == pytest.approx(P0)
        assert p[-1] == pytest.approx(PN)
        assert all(x > 0.0 for x in p)

    def test_riproducibile(self):
        a = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        b = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        assert a == b

    def test_seed_diverso_serie_diversa(self):
        a = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        b = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED + 1)
        assert a != b

    def test_log_returns(self):
        p = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        r = _F["mh377_log_returns"](p)
        assert len(r) == N
        assert r[0] == pytest.approx(RET0)
        assert r[0] == pytest.approx(math.log(p[1] / p[0]))

    def test_s0_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](0.0, MU, SIG, N, SEED)

    def test_sigma_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, -0.1, N, SEED)

    def test_n_troppo_piccolo_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, SIG, 29, SEED)

    def test_seed_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, SIG, N, 7.5)

    def test_prezzi_non_positivi_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_log_returns"]((100.0, 0.0, 101.0))


class TestKupiec:
    def test_demo(self):
        assert _F["mh377_kupiec"](N, T, 1.0 - ALPHA) == pytest.approx(LR)
        assert LR >= 0.0

    def test_forma_chiusa(self):
        p = 1.0 - ALPHA
        nn, tt = N, T
        def _lnl(nn_, tt_, pp_):
            a = tt_ * math.log(pp_) if tt_ > 0 else 0.0
            b = (nn_ - tt_) * math.log(1.0 - pp_) if tt_ < nn_ else 0.0
            return a + b
        ph = tt / nn
        ph = max(min(ph, 1.0 - 1e-12), 1e-12)
        att = max(-2.0 * (_lnl(nn, tt, p) - _lnl(nn, tt, ph)), 0.0)
        assert _F["mh377_kupiec"](nn, tt, p) == pytest.approx(att)

    def test_zero_violazioni(self):
        lr = _F["mh377_kupiec"](250, 0, 0.01)
        assert lr >= 0.0 and math.isfinite(lr)

    def test_tutte_violazioni(self):
        lr = _F["mh377_kupiec"](250, 250, 0.01)
        assert lr >= 0.0 and math.isfinite(lr)

    def test_t_sopra_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_kupiec"](250, 251, 0.01)

    def test_p_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_kupiec"](250, 3, 1.0)


class TestBasel:
    def test_verde(self):
        assert _F["mh377_basel_zone"](250, 4).startswith("VERDE")
        assert _F["mh377_basel_zone"](250, 0).startswith("VERDE")

    def test_giallo(self):
        assert _F["mh377_basel_zone"](250, 5).startswith("GIALLO")
        assert _F["mh377_basel_zone"](250, 9).startswith("GIALLO")

    def test_rosso(self):
        assert _F["mh377_basel_zone"](250, 10).startswith("ROSSO")
        assert _F["mh377_basel_zone"](250, 50).startswith("ROSSO")

    def test_scaling_n(self):
        # N=500: soglie doppie (8/18)
        assert _F["mh377_basel_zone"](500, 8).startswith("VERDE")
        assert _F["mh377_basel_zone"](500, 9).startswith("GIALLO")


class TestVerdetto:
    def test_accettabile(self):
        assert _F["mh377_verdetto"](0.10).startswith("ACCETTABILE")
        assert _F["mh377_verdetto"](0.99).startswith("ACCETTABILE")

    def test_dubbio(self):
        assert _F["mh377_verdetto"](0.05).startswith("DUBBIO")
        assert _F["mh377_verdetto"](0.0999).startswith("DUBBIO")

    def test_rifiutato(self):
        assert _F["mh377_verdetto"](0.0499).startswith("RIFIUTATO")
        assert _F["mh377_verdetto"](0.0).startswith("RIFIUTATO")

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_verdetto"](1.5)


class TestBacktest:
    def _b(self):
        return _F["mh377_backtest"](S0, MU, SIG, N, SEED, ALPHA)

    def test_demo_completa(self):
        b = self._b()
        assert b["n"] == N
        assert b["seed"] == SEED
        assert b["alpha"] == pytest.approx(ALPHA)
        assert b["z"] == pytest.approx(Z)
        assert b["sigma_daily"] == pytest.approx(SIGD)
        assert b["var_frac"] == pytest.approx(VARF)
        assert b["T"] == T
        assert b["lr"] == pytest.approx(LR)
        assert b["pvalue"] == pytest.approx(PV)
        assert b["attese"] == pytest.approx(EXP)
        assert b["basel"] == ZONE
        assert b["verdetto"] == VERDETTO

    def test_violazioni_conteggio_manuale(self):
        b = self._b()
        att = sum(1 for r in b["rendimenti"] if r < -b["var_frac"])
        assert b["T"] == att

    def test_pvalue_forma_chiusa(self):
        b = self._b()
        assert b["pvalue"] == pytest.approx(
            math.erfc(math.sqrt(b["lr"] / 2.0)))
        assert 0.0 < b["pvalue"] <= 1.0

    def test_sigma_daily_forma_chiusa(self):
        import statistics
        b = self._b()
        assert b["sigma_daily"] == pytest.approx(
            statistics.stdev(b["rendimenti"]))
        assert b["var_frac"] == pytest.approx(b["z"] * b["sigma_daily"])

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_backtest"](S0, MU, SIG, N, SEED, 0.5)

    def test_num_ok(self):
        assert _F["mh377_num"](5.0, "x") == 5.0
