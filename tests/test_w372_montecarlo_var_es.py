"""Test tab372 'Monte Carlo: VaR e Expected Shortfall di una posizione power': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh372_num", "mh372_int", "mh372_paths", "mh372_quantile",
           "mh372_var", "mh372_es", "mh372_prob_perdita",
           "mh372_quota_var", "mh372_verdetto", "mh372_var_teorico",
           "mh372_analisi")

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
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
Q = 100.0
PREZZO = 95.0
MU = 0.0
SG = 1.5
H = 1
N = 20000
SEED = 42
ALPHA = 0.95
VAR = 249.40169299684396
ES = 309.5088619538586
PROB = 0.5016
QUOTA = 0.02625280978914147
VARTEO = 246.72804404272074
VERDETTO = 'MODERATO: VaR tra il 2% e il 5% del notionale'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry372:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 824
        assert "tab372" in dvars
        assert "tab372" in withs

    def test_titoli_allineati_367_368_369_370_371_372(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh372_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](float("inf"), "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh372_int"](5, "x", 1) == 5

    def test_float_intero_ok(self):
        assert _F["mh372_int"](5.0, "x", 1) == 5

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](True, "x", 0)

    def test_float_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](5.5, "x", 1)

    def test_sotto_minimo_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](0, "x", 1)


class TestPaths:
    def test_determinismo(self):
        p1 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        p2 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert p1 == p2

    def test_lunghezza(self):
        assert len(_F["mh372_paths"](Q, MU, SG, H, 500, SEED)) == 500

    def test_seed_diverso(self):
        p1 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        p2 = _F["mh372_paths"](Q, MU, SG, H, N, SEED + 1)
        assert p1 != p2

    def test_media_vicina_drift(self):
        # mu=0, h=1 -> media ~ 0 (tolleranza 3 sigma/sqrt(n) * Q)
        p = _F["mh372_paths"](Q, 0.0, SG, 1, N, SEED)
        assert abs(sum(p) / len(p)) < 15.0

    def test_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](0.0, MU, SG, H, N, SEED)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](Q, MU, 0.0, H, N, SEED)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](Q, MU, SG, H, 50, SEED)


class TestQuantile:
    def test_mediana(self):
        assert _F["mh372_quantile"]([3, 1, 2], 0.5) == pytest.approx(2.0)

    def test_interpolazione(self):
        # pos = 0.25*3 = 0.75 -> 1 + (2-1)*0.75
        assert _F["mh372_quantile"]([1, 2, 3, 4], 0.25) == \
            pytest.approx(1.75)

    def test_estremi(self):
        assert _F["mh372_quantile"]([1, 2, 3], 0.0) == pytest.approx(1.0)
        assert _F["mh372_quantile"]([1, 2, 3], 1.0) == pytest.approx(3.0)

    def test_q_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_quantile"]([1, 2], 1.5)

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_quantile"]([], 0.5)


class TestVar:
    def test_forma_chiusa(self):
        # quantile(..., 0.2): pos=0.8 -> -10+5*0.8 = -6 -> var=6
        assert _F["mh372_var"]([-10, -5, 0, 5, 10],
                               0.8) == pytest.approx(6.0)

    def test_demo(self):
        assert _F["mh372_var"](_F["mh372_paths"](Q, MU, SG, H, N,
                                                SEED),
                               ALPHA) == pytest.approx(VAR)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_var"]([1, 2, 3], 1.0)


class TestEs:
    def test_forma_chiusa(self):
        # quantile(..., 0.2): pos=0.8 -> -10+5*0.8 = -6 -> tail=[-10] -> 10.0
        assert _F["mh372_es"]([-10, -5, 0, 5, 10],
                              0.8) == pytest.approx(10.0)

    def test_demo(self):
        assert _F["mh372_es"](_F["mh372_paths"](Q, MU, SG, H, N,
                                               SEED),
                              ALPHA) == pytest.approx(ES)

    def test_es_maggiore_var(self):
        p = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert _F["mh372_es"](p, ALPHA) >= _F["mh372_var"](p, ALPHA)


class TestProbPerdita:
    def test_forma_chiusa(self):
        assert _F["mh372_prob_perdita"]([-1, 0, 1]) == \
            pytest.approx(1.0 / 3.0)

    def test_demo(self):
        # mu=0 simmetrico -> ~0.5
        assert _F["mh372_prob_perdita"](_F["mh372_paths"](
            Q, MU, SG, H, N, SEED)) == pytest.approx(PROB, abs=0.02)


class TestQuotaVar:
    def test_demo(self):
        assert _F["mh372_quota_var"](VAR, Q * PREZZO) == \
            pytest.approx(QUOTA)

    def test_notionale_nullo(self):
        assert _F["mh372_quota_var"](100.0, 0.0) is None


class TestVerdetto:
    def test_demo(self):
        assert _F["mh372_verdetto"](QUOTA) == VERDETTO
        assert _F["mh372_verdetto"](QUOTA).startswith("MODERATO")

    def test_soglie(self):
        assert _F["mh372_verdetto"](0.01).startswith("BASSO")
        assert _F["mh372_verdetto"](0.02).startswith("MODERATO")
        assert _F["mh372_verdetto"](0.05).startswith("ELEVATO")
        assert _F["mh372_verdetto"](0.10).startswith("CRITICO")
        assert _F["mh372_verdetto"](0.15).startswith("CRITICO")

    def test_none(self):
        assert _F["mh372_verdetto"](None).startswith("DATI INSUFFICIENTI")


class TestVarTeorico:
    def test_demo(self):
        # 100*1.5*sqrt(1)*z_0.95 = 150*1.6448536269...
        assert _F["mh372_var_teorico"](Q, SG, H,
                                       ALPHA) == pytest.approx(VARTEO)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(0.99)
        assert _F["mh372_var_teorico"](10.0, 2.0, 4,
                                       0.99) == pytest.approx(10.0 * 2.0 *
                                                              2.0 * z)

    def test_mc_vicino_teorico(self):
        # con 20000 path il MC deve stare entro 5 EUR dal teorico
        p = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert abs(_F["mh372_var"](p, ALPHA) -
                   _F["mh372_var_teorico"](Q, SG, H, ALPHA)) < 5.0

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_var_teorico"](Q, 0.0, H, ALPHA)


class TestAnalisi:
    def test_demo(self):
        a = _F["mh372_analisi"](Q, PREZZO, MU, SG, H, N, SEED, ALPHA)
        assert a["notionale"] == pytest.approx(Q * PREZZO)
        assert a["var"] == pytest.approx(VAR)
        assert a["es"] == pytest.approx(ES)
        assert a["quota_var"] == pytest.approx(QUOTA)
        assert a["var_teorico"] == pytest.approx(VARTEO)
        assert a["verdetto"] == VERDETTO
        assert a["prob_perdita"] == pytest.approx(PROB, abs=0.02)
        assert abs(a["pnl_medio"]) < 15.0
        assert a["pnl_min"] < a["pnl_max"]
        assert a["es"] >= a["var"]

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_analisi"](Q, PREZZO, MU, SG, H, N, SEED, 1.5)

    def test_prezzo_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_analisi"](Q, 0.0, MU, SG, H, N, SEED, ALPHA)
