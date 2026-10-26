"""Test tab374 'Component VaR: contributo al rischio per posizione': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh374_num", "mh374_z", "mh374_cov", "mh374_vol_port",
           "mh374_dot", "mh374_marginal", "mh374_component",
           "mh374_standalone", "mh374_verdetto", "mh374_analisi")

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
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
E1 = 10000.0
E2 = 8000.0
E3 = 6000.0
S1 = 0.15
S2 = 0.2
S3 = 0.1
R12 = 0.6
R13 = 0.3
R23 = 0.4
ALPHA = 0.95
Z = 1.6448536269514715
V1 = 1500.0
V2 = 1600.0
V3 = 600.0
SIGMAP = 3059.0848304680926
VARP = 5031.746778547669
DOT1 = 2640.0
DOT2 = 2740.0
DOT3 = 1690.0
M1 = 0.21292709171883706
M2 = 0.2946566824796028
M3 = 0.09087040025374614
M1FC = 0.16448536269514716
SP0 = 2273.7634001804145
C1 = 2129.2709171883707
C2 = 2357.2534598368225
C3 = 545.2224015224768
SA1 = 2467.2804404272074
SA2 = 2631.7658031223546
SA3 = 986.912176170883
BENEFIT = 1054.2116411727757
BENPCT = 0.17322031608970478
TOPI = 1
TOPSHARE = 0.46847617012182097
VERDETTO = 'MODERATO: il maggior contribuente pesa tra 45% e 60%'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry374:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 720
        assert "tab374" in dvars
        assert "tab374" in withs

    def test_titoli_allineati_369_370_371_372_373_374(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh374_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](float("inf"), "x")


class TestZ:
    def test_demo(self):
        assert _F["mh374_z"](ALPHA) == pytest.approx(Z)

    def test_z95_noto(self):
        from statistics import NormalDist
        assert _F["mh374_z"](0.95) == pytest.approx(
            NormalDist().inv_cdf(0.95))

    def test_alpha_basso_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_z"](0.5)

    def test_alpha_alto_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_z"](1.0)


class TestCov:
    def test_demo_v(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["v"] == pytest.approx((V1, V2, V3))
        # v_i = E_i * s_i in forma chiusa
        assert c["v"][0] == pytest.approx(E1 * S1)
        assert c["v"][1] == pytest.approx(E2 * S2)
        assert c["v"][2] == pytest.approx(E3 * S3)

    def test_demo_c(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["c11"] == pytest.approx(V1 * V1)
        assert c["c22"] == pytest.approx(V2 * V2)
        assert c["c12"] == pytest.approx(V1 * V2 * R12)
        assert c["c13"] == pytest.approx(V1 * V3 * R13)
        assert c["c23"] == pytest.approx(V2 * V3 * R23)

    def test_posizione_singola(self):
        c = _F["mh374_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        assert c["v"][0] == pytest.approx(1500.0)
        assert c["c11"] == pytest.approx(1500.0 ** 2)
        assert c["c22"] == pytest.approx(0.0)
        assert c["c12"] == pytest.approx(0.0)

    def test_corr_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, S1, S2, S3, 1.5, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, -1.01, R23)

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, -0.05, S2, S3, R12, R13, R23)


class TestVol:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh374_vol_port"](c) == pytest.approx(SIGMAP)

    def test_posizione_singola(self):
        c = _F["mh374_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        assert _F["mh374_vol_port"](c) == pytest.approx(1500.0)

    def test_non_correlate(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, 0.0, 0.0, 0.0)
        assert _F["mh374_vol_port"](c) == pytest.approx(SP0)
        assert SP0 == pytest.approx(math.sqrt(V1 ** 2 + V2 ** 2 + V3 ** 2))

    def test_vol_nulla_ko(self):
        c = _F["mh374_cov"](0.0, 0.0, 0.0, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_vol_port"](c)

    def test_non_psd_ko(self):
        c = _F["mh374_cov"](1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                            -1.0, -1.0, -1.0)
        with pytest.raises(ValueError):
            _F["mh374_vol_port"](c)


class TestDot:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh374_dot"](c, 0) == pytest.approx(DOT1)
        assert _F["mh374_dot"](c, 1) == pytest.approx(DOT2)
        assert _F["mh374_dot"](c, 2) == pytest.approx(DOT3)
        # forma chiusa: riga 0 = v1 + r12*v2 + r13*v3
        assert _F["mh374_dot"](c, 0) == pytest.approx(
            V1 + R12 * V2 + R13 * V3)

    def test_indice_ko(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_dot"](c, 3)


class TestMarginal:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        sp = _F["mh374_vol_port"](c)
        assert _F["mh374_marginal"](Z, S1, DOT1, sp) == pytest.approx(M1)
        assert _F["mh374_marginal"](Z, S2, DOT2, sp) == pytest.approx(M2)
        assert _F["mh374_marginal"](Z, S3, DOT3, sp) == pytest.approx(M3)

    def test_posizione_singola(self):
        # dot = v1, sigma_p = v1 -> m = z * s1
        assert M1FC == pytest.approx(Z * 0.10)

    def test_sigma_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_marginal"](Z, S1, DOT1, 0.0)


class TestComponent:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        sp = _F["mh374_vol_port"](c)
        m = [_F["mh374_marginal"](Z, c["s"][i], _F["mh374_dot"](c, i), sp)
             for i in range(3)]
        cv = [_F["mh374_component"](c["e"][i], m[i]) for i in range(3)]
        assert cv == pytest.approx((C1, C2, C3))

    def test_eulero(self):
        # somma Component VaR = VaR di portafoglio
        assert C1 + C2 + C3 == pytest.approx(VARP)

    def test_esposizione_nulla(self):
        assert _F["mh374_component"](0.0, M1) == 0.0


class TestStandalone:
    def test_demo(self):
        assert _F["mh374_standalone"](Z, V1) == pytest.approx(SA1)
        assert _F["mh374_standalone"](Z, V2) == pytest.approx(SA2)
        assert _F["mh374_standalone"](Z, V3) == pytest.approx(SA3)

    def test_valore_assoluto(self):
        assert _F["mh374_standalone"](Z, -500.0) == pytest.approx(Z * 500.0)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh374_verdetto"](TOPSHARE) == VERDETTO
        assert VERDETTO.startswith("MODERATO")

    def test_concentrato(self):
        assert _F["mh374_verdetto"](0.65).startswith("CONCENTRATO")
        assert _F["mh374_verdetto"](0.60).startswith("CONCENTRATO")

    def test_moderato(self):
        assert _F["mh374_verdetto"](0.59).startswith("MODERATO")
        assert _F["mh374_verdetto"](0.45).startswith("MODERATO")

    def test_bilanciato(self):
        assert _F["mh374_verdetto"](0.449).startswith("BILANCIATO")
        assert _F["mh374_verdetto"](0.10).startswith("BILANCIATO")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh374_verdetto"](-0.1)


class TestAnalisi:
    def test_demo(self):
        a = _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (R12, R13, R23), ALPHA)
        assert a["z"] == pytest.approx(Z)
        assert a["sigma_p"] == pytest.approx(SIGMAP)
        assert a["var_p"] == pytest.approx(VARP)
        assert a["marginal"] == pytest.approx((M1, M2, M3))
        assert a["cvar"] == pytest.approx((C1, C2, C3))
        assert a["standalone"] == pytest.approx((SA1, SA2, SA3))
        assert a["benefit"] == pytest.approx(BENEFIT)
        assert a["benefit_pct"] == pytest.approx(BENPCT)
        assert a["top_i"] == TOPI
        assert a["top_share"] == pytest.approx(TOPSHARE)
        assert a["verdetto"] == VERDETTO
        # Eulero + quote a somma 1
        assert sum(a["cvar"]) == pytest.approx(a["var_p"])
        assert sum(a["quote"]) == pytest.approx(1.0)
        # la demo ha correlazioni < 1: beneficio positivo, top = Power
        assert a["benefit"] > 0.0
        assert a["top_i"] == 1
        assert a["verdetto"].startswith("MODERATO")

    def test_non_correlate(self):
        a = _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (0.0, 0.0, 0.0), ALPHA)
        assert a["benefit"] == pytest.approx(
            SA1 + SA2 + SA3 - a["var_p"])
        assert a["benefit"] > 0.0

    def test_posizione_singola(self):
        a = _F["mh374_analisi"]((10000.0, 0.0, 0.0), (0.15, 0.0, 0.0),
                                (0.0, 0.0, 0.0), ALPHA)
        assert a["benefit"] == pytest.approx(0.0)
        assert a["top_share"] == pytest.approx(1.0)
        assert a["cvar"][0] == pytest.approx(a["var_p"])
        assert a["verdetto"].startswith("CONCENTRATO")

    def test_corr_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (1.5, R13, R23), ALPHA)

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2), (S1, S2, S3),
                                (R12, R13, R23), ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (R12, R13, R23), 1.5)
