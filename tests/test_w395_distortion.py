"""Test tab395 '🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh395_num", "mh395_check_alpha", "mh395_check_family",
           "mh395_check_param", "mh395_g", "mh395_rho_chiusa",
           "_mh395_quad", "mh395_rho", "mh395_rho_quad",
           "mh395_concava_ok", "mh395_benchmarks", "mh395_verdetto",
           "mh395_mappa")

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
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
FAM = 'wang'
PARAM = 0.5
RHO = 5000.0
VAR = 19599.639845400536
ES = 23378.027922014157
_FAMS = ("var", "es", "wang", "ph", "dp")
_PAR = {"var": None, "es": None, "wang": 0.5, "ph": 0.5, "dp": 2.0}


class TestRegistry395:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 690
        assert "tab395" in dvars
        assert "tab395" in withs

    def test_titoli_allineati_390_391_392_393_394_395(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395

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
        assert _F["mh395_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_num"](float("inf"), "x")


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh395_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh395_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_check_alpha"](float("nan"))


class TestFamilyParam:
    @pytest.mark.parametrize("fam", ["var", "es", "wang", "ph", "dp"])
    def test_family_ok(self, fam):
        assert _F["mh395_check_family"](fam) == fam

    @pytest.mark.parametrize("fam", ["x", "", None, 5, True])
    def test_family_ko(self, fam):
        with pytest.raises(ValueError):
            _F["mh395_check_family"](fam)

    @pytest.mark.parametrize("p", [0.0, 0.5, 2.0])
    def test_param_wang_ok(self, p):
        assert _F["mh395_check_param"]("wang", p) == p

    @pytest.mark.parametrize("p", [-0.1, float("nan"), float("inf"),
                                   "0.5", True])
    def test_param_wang_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh395_check_param"]("wang", p)

    @pytest.mark.parametrize("p", [0.05, 0.5, 1.0])
    def test_param_ph_ok(self, p):
        assert _F["mh395_check_param"]("ph", p) == p

    @pytest.mark.parametrize("p", [0.0, 1.5, -1.0])
    def test_param_ph_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh395_check_param"]("ph", p)

    @pytest.mark.parametrize("p", [1.0, 2.0, 5.0])
    def test_param_dp_ok(self, p):
        assert _F["mh395_check_param"]("dp", p) == p

    @pytest.mark.parametrize("p", [0.5, 0.99, -2.0])
    def test_param_dp_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh395_check_param"]("dp", p)

    def test_param_var_es_ignorato(self):
        assert _F["mh395_check_param"]("var", "qualsiasi") is None
        assert _F["mh395_check_param"]("es", 999) is None


class TestG:
    @pytest.mark.parametrize("fam", ["var", "es", "wang", "ph", "dp"])
    def test_estremi(self, fam):
        assert _F["mh395_g"](0.0, fam, _PAR[fam], ALPHA) == 0.0
        assert _F["mh395_g"](1.0, fam, _PAR[fam], ALPHA) == 1.0

    def test_var_gradino(self):
        assert _F["mh395_g"](0.02, "var", None, 0.975) == 0.0
        assert _F["mh395_g"](0.025, "var", None, 0.975) == 0.0
        assert _F["mh395_g"](0.03, "var", None, 0.975) == 1.0

    def test_es_valore_noto(self):
        # 1-alpha = 0.025000000000000022 in floating point: confronto
        # approssimato, non esatto
        assert abs(_F["mh395_g"](0.0125, "es", None, 0.975) - 0.5) < 1e-12
        assert _F["mh395_g"](0.5, "es", None, 0.975) == 1.0

    def test_wang_lambda_zero_identita(self):
        assert abs(_F["mh395_g"](0.3, "wang", 0.0, ALPHA) - 0.3) < 1e-12

    def test_wang_valore_noto(self):
        assert abs(_F["mh395_g"](0.5, "wang", 0.5, ALPHA) -
                   0.6914624612740131) < 1e-12

    def test_ph_valore_noto(self):
        assert _F["mh395_g"](0.25, "ph", 0.5, ALPHA) == 0.5

    def test_dp_valore_noto(self):
        assert _F["mh395_g"](0.5, "dp", 2.0, ALPHA) == 0.75

    def test_ph_dp_uno_identita(self):
        assert abs(_F["mh395_g"](0.37, "ph", 1.0, ALPHA) - 0.37) < 1e-12
        assert abs(_F["mh395_g"](0.37, "dp", 1.0, ALPHA) - 0.37) < 1e-12

    @pytest.mark.parametrize("u", [-0.1, 1.1, float("nan")])
    def test_u_ko(self, u):
        with pytest.raises(ValueError):
            _F["mh395_g"](u, "es", None, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_g"](0.5, "es", None, 1.5)

    def test_family_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_g"](0.5, "xx", None, ALPHA)


class TestRhoChiusa:
    def test_demo_var(self):
        assert _F["mh395_rho_chiusa"](MU, SIG, "var", None, ALPHA) == VAR

    def test_demo_es(self):
        assert _F["mh395_rho_chiusa"](MU, SIG, "es", None, ALPHA) == ES

    def test_demo_wang(self):
        assert _F["mh395_rho_chiusa"](MU, SIG, FAM, PARAM, ALPHA) == RHO

    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh395_rho_chiusa"](MU, SIG, "var", None, ALPHA) -
                   (MU + SIG * z)) < 1e-9

    def test_es_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh395_rho_chiusa"](MU, SIG, "es", None, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    @pytest.mark.parametrize("lam", [0.0, 0.25, 0.5, 1.0, 2.0])
    def test_wang_mu_piu_lambda_sig(self, lam):
        assert _F["mh395_rho_chiusa"](MU, SIG, "wang", lam, ALPHA) == \
            MU + lam * SIG

    def test_identita_ph_dp(self):
        assert _F["mh395_rho_chiusa"](MU, SIG, "ph", 1.0, ALPHA) == MU
        assert _F["mh395_rho_chiusa"](MU, SIG, "dp", 1.0, ALPHA) == MU

    def test_ph_dp_generici_none(self):
        assert _F["mh395_rho_chiusa"](MU, SIG, "ph", 0.5, ALPHA) is None
        assert _F["mh395_rho_chiusa"](MU, SIG, "dp", 2.0, ALPHA) is None

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_rho_chiusa"](MU, -1.0, "es", None, ALPHA)


class TestRho:
    def test_demo(self):
        assert _F["mh395_rho"](MU, SIG, FAM, PARAM, ALPHA) == RHO

    def test_demo_meno_del_var(self):
        assert RHO < VAR

    @pytest.mark.parametrize("aa", [0.90, 0.95, 0.975])
    def test_es_quad_vs_chiusa(self, aa):
        c = _F["mh395_rho"](MU, SIG, "es", None, aa)
        q = _F["mh395_rho_quad"](MU, SIG, "es", None, aa)
        assert abs(c - q) / SIG < 1e-6

    @pytest.mark.parametrize("lam", [0.25, 0.5, 1.0])
    def test_wang_quad_vs_chiusa(self, lam):
        c = _F["mh395_rho"](MU, SIG, "wang", lam, ALPHA)
        q = _F["mh395_rho_quad"](MU, SIG, "wang", lam, ALPHA)
        assert abs(c - q) / SIG < 1e-6

    @pytest.mark.parametrize("r", [0.25, 0.5, 0.75])
    def test_ph_sopra_media(self, r):
        assert _F["mh395_rho"](MU, SIG, "ph", r, ALPHA) > MU

    def test_ph_monotonia_decrescente_in_r(self):
        assert _F["mh395_rho"](MU, SIG, "ph", 0.25, ALPHA) > \
            _F["mh395_rho"](MU, SIG, "ph", 0.5, ALPHA) > \
            _F["mh395_rho"](MU, SIG, "ph", 0.75, ALPHA) > MU

    def test_dp_monotonia_crescente_in_s(self):
        assert MU < _F["mh395_rho"](MU, SIG, "dp", 1.5, ALPHA) < \
            _F["mh395_rho"](MU, SIG, "dp", 2.0, ALPHA) < \
            _F["mh395_rho"](MU, SIG, "dp", 3.0, ALPHA)

    @pytest.mark.parametrize("fam", ["var", "es", "wang", "ph", "dp"])
    def test_sig_zero(self, fam):
        assert _F["mh395_rho"](2000.0, 0.0, fam, _PAR[fam], ALPHA) == 2000.0
        assert _F["mh395_rho_quad"](2000.0, 0.0, fam, _PAR[fam],
                                   ALPHA) == 2000.0

    def test_traslazione(self):
        assert abs(_F["mh395_rho"](5000.0, SIG, FAM, PARAM, ALPHA) -
                   (RHO + 5000.0)) < 1e-9

    def test_scaling(self):
        assert abs(_F["mh395_rho"](MU, 2.0 * SIG, FAM, PARAM, ALPHA) -
                   2.0 * RHO) < 1e-9

    def test_deterministico(self):
        assert _F["mh395_rho"](MU, SIG, "ph", 0.5, ALPHA) == \
            _F["mh395_rho"](MU, SIG, "ph", 0.5, ALPHA)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_rho"](MU, -1.0, FAM, PARAM, ALPHA)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_rho"](MU, SIG, FAM, PARAM, ALPHA, n=4)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_rho"](MU, SIG, FAM, PARAM, 2.0)

    def test_family_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_rho"](MU, SIG, "xx", PARAM, ALPHA)


class TestConcava:
    def test_var_non_concava(self):
        assert _F["mh395_concava_ok"]("var", None, ALPHA) is False

    @pytest.mark.parametrize("fp", [("es", None), ("wang", 0.5),
                                    ("ph", 0.5), ("dp", 2.0)])
    def test_concave(self, fp):
        assert _F["mh395_concava_ok"](fp[0], fp[1], ALPHA) is True

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_concava_ok"]("es", None, ALPHA, n=4)


class TestBenchmarks:
    def test_demo(self):
        b = _F["mh395_benchmarks"](MU, SIG, ALPHA)
        assert b["var"] == VAR
        assert b["es"] == ES

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_benchmarks"](MU, -1.0, ALPHA)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh395_verdetto"](RHO, VAR, ES).startswith("SOTTO-VaR")

    def test_bordi(self):
        assert _F["mh395_verdetto"](VAR, VAR, ES).startswith("TRA VaR")
        assert _F["mh395_verdetto"](ES, VAR, ES).startswith("TRA VaR")
        assert _F["mh395_verdetto"](VAR - 1.0, VAR,
                                   ES).startswith("SOTTO-VaR")
        assert _F["mh395_verdetto"](ES + 1.0, VAR,
                                   ES).startswith("OLTRE ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_verdetto"](float("nan"), VAR, ES)


class TestMappa:
    def _b(self):
        return _F["mh395_mappa"](MU, SIG, FAM, PARAM, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["family"] == FAM and b["param"] == PARAM
        assert b["rho"] == RHO
        assert b["var"] == VAR and b["es"] == ES
        assert b["coerente"] is True
        assert b["verdetto"].startswith("SOTTO-VaR")

    def test_coerenza_var(self):
        b = _F["mh395_mappa"](MU, SIG, "var", None, ALPHA)
        assert b["coerente"] is False
        assert b["rho"] == b["var"]
        assert b["verdetto"].startswith("TRA VaR")

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh395_mappa"](MU, SIG, FAM, PARAM, 2.0)
