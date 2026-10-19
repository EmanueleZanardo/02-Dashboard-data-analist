"""Test tab382 'Hedge VaR: copertura ottimale con futures': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh382_num", "mh382_z", "mh382_hedge_ratio",
           "mh382_sigma_hedged", "mh382_sigma_ottimale", "mh382_var",
           "mh382_riduzione", "mh382_efficacia", "mh382_costo",
           "mh382_verdetto", "mh382_mappa")

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
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
E = 10000.0
SS = 0.2
SF = 0.22
RHO = 0.85
SPREAD = 10.0
ALPHA = 0.95
Z = 1.6448536269514715
HSTAR = 0.7727272727272728
SIGH = 0.10535653752852742
VARU = 3289.707253902943
VARH = 1732.9608287684716
RID = 0.47321731235736286
EFF = 0.7224999999999999
COSTO = 7.7272727272727275
NOTH = 7727.272727272728


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry382:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 575
        assert "tab382" in dvars
        assert "tab382" in withs

    def test_titoli_allineati_377_378_379_380_381_382(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab377")] == TITLE377
        assert titoli[dvars.index("tab378")] == TITLE378
        assert titoli[dvars.index("tab379")] == TITLE379
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh382_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_num"](float("inf"), "x")


class TestZ:
    def test_z_demo(self):
        assert _F["mh382_z"](ALPHA) == pytest.approx(Z)

    def test_z_95_forma_nota(self):
        assert _F["mh382_z"](0.95) == pytest.approx(1.6448536269514715)

    def test_z_99_forma_nota(self):
        assert _F["mh382_z"](0.99) == pytest.approx(2.3263478740408408)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_z"](0.4)
        with pytest.raises(ValueError):
            _F["mh382_z"](1.0)


class TestHedgeRatio:
    def test_demo(self):
        assert _F["mh382_hedge_ratio"](SS, SF, RHO) == pytest.approx(HSTAR)

    def test_forma_chiusa(self):
        assert HSTAR == pytest.approx(RHO * SS / SF)

    def test_rho_zero_nessun_hedge(self):
        assert _F["mh382_hedge_ratio"](SS, SF, 0.0) == pytest.approx(0.0)

    def test_rho_negativo_segno(self):
        assert _F["mh382_hedge_ratio"](SS, SF, -0.5) == pytest.approx(
            -0.5 * SS / SF)

    def test_sigma_f_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_hedge_ratio"](SS, 0.0, RHO)

    def test_sigma_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_hedge_ratio"](-0.1, SF, RHO)

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_hedge_ratio"](SS, SF, 1.5)


class TestSigmaHedged:
    def test_demo_in_h_star(self):
        assert _F["mh382_sigma_hedged"](SS, SF, RHO, HSTAR) == pytest.approx(
            SIGH)

    def test_h_zero_torna_spot(self):
        assert _F["mh382_sigma_hedged"](SS, SF, RHO, 0.0) == pytest.approx(SS)

    def test_forma_generale(self):
        h = 0.4
        var = SS ** 2 + (h * SF) ** 2 - 2.0 * h * RHO * SS * SF
        assert _F["mh382_sigma_hedged"](SS, SF, RHO, h) == pytest.approx(
            math.sqrt(var))

    def test_correlazione_perfetta_zero_residuo(self):
        h1 = SS / SF
        assert _F["mh382_sigma_hedged"](SS, SF, 1.0, h1) == pytest.approx(0.0)

    def test_minimo_in_h_star(self):
        sh_star = _F["mh382_sigma_hedged"](SS, SF, RHO, HSTAR)
        for dh in (-0.2, -0.05, 0.05, 0.2):
            assert _F["mh382_sigma_hedged"](
                SS, SF, RHO, HSTAR + dh) >= sh_star

    def test_sigma_f_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_sigma_hedged"](SS, 0.0, RHO, HSTAR)


class TestSigmaOttimale:
    def test_demo(self):
        assert _F["mh382_sigma_ottimale"](SS, SF, RHO) == pytest.approx(SIGH)

    def test_forma_chiusa(self):
        assert SIGH == pytest.approx(SS * math.sqrt(1.0 - RHO ** 2))

    def test_demo_efficacia_7225(self):
        assert 1.0 - (SIGH / SS) ** 2 == pytest.approx(0.7225)

    def test_rho_zero(self):
        assert _F["mh382_sigma_ottimale"](SS, SF, 0.0) == pytest.approx(SS)

    def test_rho_uno(self):
        assert _F["mh382_sigma_ottimale"](SS, SF, 1.0) == pytest.approx(0.0)

    def test_coerenza_generale(self):
        for rr in (-0.7, 0.0, 0.3, 0.99):
            hs = _F["mh382_hedge_ratio"](SS, SF, rr)
            assert _F["mh382_sigma_ottimale"](SS, SF, rr) == pytest.approx(
                _F["mh382_sigma_hedged"](SS, SF, rr, hs))

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_sigma_ottimale"](SS, SF, 2.0)


class TestVar:
    def test_demo_scoperto(self):
        assert _F["mh382_var"](E, SS, Z) == pytest.approx(VARU)

    def test_demo_coperto(self):
        assert _F["mh382_var"](E, SIGH, Z) == pytest.approx(VARH)

    def test_forma_chiusa(self):
        assert VARU == pytest.approx(Z * E * SS)
        assert VARH == pytest.approx(Z * E * SIGH)

    def test_E_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_var"](0.0, SS, Z)
        with pytest.raises(ValueError):
            _F["mh382_var"](-100.0, SS, Z)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_var"](E, -0.1, Z)

    def test_z_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_var"](E, SS, 0.0)


class TestRiduzione:
    def test_demo(self):
        assert _F["mh382_riduzione"](VARU, VARH) == pytest.approx(RID)

    def test_forma_chiusa(self):
        assert RID == pytest.approx(1.0 - VARH / VARU)

    def test_demo_efficace(self):
        assert 0.30 <= RID < 0.50

    def test_var_u_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_riduzione"](0.0, VARH)
        with pytest.raises(ValueError):
            _F["mh382_riduzione"](-1.0, VARH)

    def test_var_h_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_riduzione"](VARU, -1.0)


class TestEfficacia:
    def test_demo(self):
        assert _F["mh382_efficacia"](SS, SIGH) == pytest.approx(EFF)

    def test_forma_chiusa(self):
        assert EFF == pytest.approx(1.0 - (SIGH / SS) ** 2)

    def test_hedge_nullo(self):
        assert _F["mh382_efficacia"](SS, SS) == pytest.approx(0.0)

    def test_hedge_perfetto(self):
        assert _F["mh382_efficacia"](SS, 0.0) == pytest.approx(1.0)

    def test_sigma_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_efficacia"](0.0, SIGH)
        with pytest.raises(ValueError):
            _F["mh382_efficacia"](-0.1, SIGH)


class TestCosto:
    def test_demo(self):
        assert _F["mh382_costo"](E, HSTAR, SPREAD) == pytest.approx(COSTO)

    def test_forma_chiusa(self):
        assert COSTO == pytest.approx(E * HSTAR * SPREAD / 10000.0)

    def test_spread_zero(self):
        assert _F["mh382_costo"](E, HSTAR, 0.0) == pytest.approx(0.0)

    def test_h_negativo_valore_assoluto(self):
        assert _F["mh382_costo"](E, -HSTAR, SPREAD) == pytest.approx(COSTO)

    def test_E_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_costo"](0.0, HSTAR, SPREAD)

    def test_spread_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_costo"](E, HSTAR, -1.0)


class TestVerdetto:
    def test_inefficace(self):
        assert _F["mh382_verdetto"](0.0).startswith("INEFFICACE")
        assert _F["mh382_verdetto"](0.1499).startswith("INEFFICACE")

    def test_limitata(self):
        assert _F["mh382_verdetto"](0.15).startswith("LIMITATA")
        assert _F["mh382_verdetto"](0.2999).startswith("LIMITATA")

    def test_efficace(self):
        assert _F["mh382_verdetto"](0.30).startswith("EFFICACE")
        assert _F["mh382_verdetto"](0.4999).startswith("EFFICACE")

    def test_ottimale(self):
        assert _F["mh382_verdetto"](0.50).startswith("OTTIMALE")
        assert _F["mh382_verdetto"](0.9).startswith("OTTIMALE")

    def test_demo_efficace(self):
        assert _F["mh382_verdetto"](RID).startswith("EFFICACE")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh382_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh382_verdetto"](-0.1)


class TestMappa:
    def _b(self):
        return _F["mh382_mappa"](E, SS, SF, RHO, SPREAD, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["h_star"] == pytest.approx(HSTAR)
        assert b["sigma_h"] == pytest.approx(SIGH)
        assert b["var_u"] == pytest.approx(VARU)
        assert b["var_h"] == pytest.approx(VARH)
        assert b["riduzione"] == pytest.approx(RID)
        assert b["efficacia"] == pytest.approx(EFF)
        assert b["costo"] == pytest.approx(COSTO)
        assert b["notional_hedge"] == pytest.approx(NOTH)
        assert b["verdetto"].startswith("EFFICACE")

    def test_coerenza(self):
        b = self._b()
        assert b["var_u"] == pytest.approx(b["z"] * b["E"] * b["sigma_s"])
        assert b["var_h"] == pytest.approx(b["z"] * b["E"] * b["sigma_h"])
        assert b["riduzione"] == pytest.approx(1.0 - b["var_h"] / b["var_u"])
        assert b["efficacia"] == pytest.approx(
            1.0 - (b["sigma_h"] / b["sigma_s"]) ** 2)
        assert b["h_star"] == pytest.approx(
            b["rho"] * b["sigma_s"] / b["sigma_f"])
        assert b["costo"] == pytest.approx(
            b["E"] * abs(b["h_star"]) * b["spread_bps"] / 10000.0)
        assert b["alpha"] == pytest.approx(ALPHA)

    def test_echo_input(self):
        b = self._b()
        assert b["E"] == E
        assert b["sigma_s"] == SS
        assert b["sigma_f"] == SF
        assert b["rho"] == RHO
        assert b["spread_bps"] == SPREAD
