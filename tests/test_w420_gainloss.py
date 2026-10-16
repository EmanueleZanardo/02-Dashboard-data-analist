
"""Test tab420 '📈 Gain-Loss ratio: guadagno atteso contro perdita attesa': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh420_num", "mh420_parse_serie", "mh420_gain_loss",
           "mh420_omega_thr", "mh420_verdetto", "mh420_curva",
           "mh420_mappa", "mh412_omega", "mh412_num",
           "mh419_star", "mh419_check_delta", "mh419_num")

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
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
GL = 1.8734177215189873
E_GAIN = 2.8777777777777778
E_LOSS = 1.536111111111111


class TestRegistry420:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 501
        assert "tab420" in dvars
        assert "tab420" in withs

    def test_titoli_allineati_415_416_417_418_419_420(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab415")] == TITLE415
        assert titoli[dvars.index("tab416")] == TITLE416
        assert titoli[dvars.index("tab417")] == TITLE417
        assert titoli[dvars.index("tab418")] == TITLE418
        assert titoli[dvars.index("tab419")] == TITLE419
        assert titoli[dvars.index("tab420")] == TITLE420

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


class TestGainLoss420:
    def _xs(self):
        return _F["mh420_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh420_mappa"](xs)
        assert abs(m["gl"] - GL) < 1e-12
        assert abs(m["e_gain"] - E_GAIN) < 1e-12
        assert abs(m["e_loss"] - E_LOSS) < 1e-12
        assert abs(m["gl"] - 103.6 / 55.3) < 1e-12
        assert abs(m["e_gain"] - 103.6 / 36.0) < 1e-12
        assert abs(m["e_loss"] - 55.3 / 36.0) < 1e-12
        assert m["n_pos"] == 30
        assert m["n_neg"] == 6
        assert abs(m["p_sopra"] - 30.0 / 36.0) < 1e-12
        # ACCETTABILE: 1.5 <= gl < 2.0
        assert m["verdetto"].startswith("ACCETTABILE")
        assert 1.87 < m["gl"] < 1.88
        assert abs(m["gl"] - m["e_gain"] / m["e_loss"]) < 1e-12
        # il cross-check interno: omega0 e' il Gain-Loss stesso
        assert abs(m["omega0"] - m["gl"]) < 1e-12

    def test_definizione_a_mano(self):
        # GL = E[max(r,0)] / E[max(-r,0)], indipendente dall'helper
        xs = list(self._xs())
        n = len(xs)
        sp = sum(x for x in xs if x > 0.0)
        sl = sum(-x for x in xs if x < 0.0)
        k = _F["mh420_gain_loss"](tuple(xs))
        assert abs(k["gl"] - (sp / n) / (sl / n)) < 1e-12
        assert abs(k["e_gain"] - sp / n) < 1e-12
        assert abs(k["e_loss"] - sl / n) < 1e-12
        assert k["n_pos"] == 30 and k["n_neg"] == 6
        assert abs(k["sum_pos"] - 103.6) < 1e-12
        assert abs(k["sum_neg"] - 55.3) < 1e-12

    def test_crosscheck_tab412_omega(self):
        # Gain-Loss = Omega tab412 con soglia T = 0.0 (stessa
        # definizione, per costruzione e per teorema)
        xs = self._xs()
        om0 = _F["mh412_omega"](xs, 0.0)["omega"]
        assert abs(_F["mh420_gain_loss"](xs)["gl"] - om0) < 1e-12
        # omega_thr self-contained coincide con tab412 per ogni T
        for T in (-10.0, -5.0, -1.5, 0.0, 2.5, 7.0):
            mio = _F["mh420_omega_thr"](xs, T)["omega"]
            loro = _F["mh412_omega"](xs, T)["omega"]
            assert abs(mio - loro) < 1e-12, T
            if not math.isinf(mio):
                _om = _F["mh420_omega_thr"](xs, T)
                eup = sum(x - T for x in xs if x > T) / len(xs)
                edn = sum(T - x for x in xs if x < T) / len(xs)
                assert abs(_om["omega"] - eup / edn) < 1e-12
                assert abs(_om["e_up"] - eup) < 1e-12
                assert abs(_om["e_dn"] - edn) < 1e-12
        # a T=0 omega_thr coincide con FT_11 di tab417 (Omega per
        # definizione): triplo ancoraggio 412/417/420
        assert abs(_F["mh420_omega_thr"](xs, 0.0)["omega"] - GL) < 1e-12

    def test_crosscheck_tab419_gl_vs_star(self):
        # GL usa la perdita MEDIA, STAR usa la perdita di CODA:
        # sulla demo GL=1.87>1.0 mentre STAR=0.11<1.0 (la coda domina
        # ma la media no) -> la media delle perdite e' piccola
        xs = self._xs()
        gl = _F["mh420_gain_loss"](xs)["gl"]
        star = _F["mh419_star"](xs, 0.05)["star"]
        assert gl > 1.0 > star
        e_loss = _F["mh420_gain_loss"](xs)["e_loss"]
        etl = _F["mh419_star"](xs, 0.05)["etl"]
        assert e_loss < etl  # perdita media << perdita di coda

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        base = F["mh420_gain_loss"](xs)["gl"]
        # alzare i guadagni: GL sale
        up = tuple(x + 1.0 if x > 0.0 else x for x in xs)
        assert F["mh420_gain_loss"](up)["gl"] > base
        # approfondire le perdite: GL scende
        dn = tuple(x - 1.0 if x < 0.0 else x for x in xs)
        assert F["mh420_gain_loss"](dn)["gl"] < base
        # scala: moltiplicare tutti i rendimenti per 2 non cambia GL
        sc = tuple(2.0 * x for x in xs)
        assert abs(F["mh420_gain_loss"](sc)["gl"] - base) < 1e-12
        # omega_thr: alzare T abbassa omega (upside shrink, downside
        # grow) sulla demo
        o0 = F["mh420_omega_thr"](xs, 0.0)["omega"]
        o5 = F["mh420_omega_thr"](xs, 5.0)["omega"]
        o_5 = F["mh420_omega_thr"](xs, -5.0)["omega"]
        assert o5 < o0 < o_5

    def test_infinito_senza_perdite(self):
        # tutti sopra lo 0: nessuna perdita -> +inf
        k = _F["mh420_gain_loss"](tuple([1.0] * 25))
        assert math.isinf(k["gl"])
        assert k["e_loss"] == 0.0
        assert _F["mh420_verdetto"](k["gl"]).startswith("MOLTO FORTE")
        # nessun guadagno: gl = 0.0, valido (NEGATIVO)
        k2 = _F["mh420_gain_loss"](tuple([-1.0] * 25))
        assert k2["gl"] == 0.0
        assert _F["mh420_verdetto"](k2["gl"]).startswith("NEGATIVO")

    def test_curva(self):
        F = _F
        xs = self._xs()
        c = F["mh420_curva"](xs, -2.0, 2.0, 1.0)
        assert len(c) == 5
        assert [t for t, _ in c] == [-2.0, -1.0, 0.0, 1.0, 2.0]
        # il punto a T=0 e' il Gain-Loss
        assert abs(dict(c)[0.0] - GL) < 1e-12
        # ogni punto coincide con omega_thr
        for t, o in c:
            mio = F["mh420_omega_thr"](xs, t)["omega"]
            assert (o is None) == math.isinf(mio)
            if o is not None:
                assert abs(o - mio) < 1e-12
        # monotona decrescente in T (sulla demo, omega finito)
        oo = [o for _, o in c if o is not None]
        assert all(a > b for a, b in zip(oo, oo[1:]))
        with pytest.raises(ValueError):
            F["mh420_curva"](None)
        with pytest.raises(ValueError):
            F["mh420_curva"](xs, 2.0, -2.0, 1.0)
        with pytest.raises(ValueError):
            F["mh420_curva"](xs, -2.0, 2.0, 0.0)

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh420_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh420_verdetto"](0.0).startswith("NEGATIVO")
        assert F["mh420_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh420_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh420_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh420_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh420_verdetto"](2.0).startswith("BUONO")
        assert F["mh420_verdetto"](2.99).startswith("BUONO")
        assert F["mh420_verdetto"](3.0).startswith("FORTE")
        assert F["mh420_verdetto"](4.99).startswith("FORTE")
        assert F["mh420_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh420_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh420_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh420_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta su 0 -> ValueError
        with pytest.raises(ValueError):
            F["mh420_gain_loss"](tuple([0.0] * 25))
        with pytest.raises(ValueError):
            F["mh420_mappa"](tuple([0.0] * 25))
        with pytest.raises(ValueError):
            F["mh420_mappa"]((1.0,) * 19)
        with pytest.raises(ValueError):
            F["mh420_mappa"](None)
        with pytest.raises(ValueError):
            F["mh420_omega_thr"](tuple([2.0] * 25), 2.0)
        # soglia cattiva contro la sua funzione (lezione tab417)
        for _t in (True, "x", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                F["mh420_omega_thr"](self._xs(), _t)

    def test_validatori(self):
        for _bad in (lambda: _F["mh420_gain_loss"](None),
                     lambda: _F["mh420_gain_loss"]((1.0,) * 19),
                     lambda: _F["mh420_gain_loss"](tuple([0.0] * 25)),
                     lambda: _F["mh420_omega_thr"](None, 0.0),
                     lambda: _F["mh420_omega_thr"]((1.0,) * 19, 0.0),
                     lambda: _F["mh420_omega_thr"](tuple([2.0] * 25), 2.0),
                     lambda: _F["mh420_omega_thr"](self._xs(), True),
                     lambda: _F["mh420_omega_thr"](self._xs(),
                                                  float("nan")),
                     lambda: _F["mh420_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh420_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh420_parse_serie"](None),
                     lambda: _F["mh420_num"](True, "x"),
                     lambda: _F["mh420_num"](float("nan"), "x"),
                     lambda: _F["mh420_mappa"]((1.0,) * 19),
                     lambda: _F["mh420_mappa"](None),
                     lambda: _F["mh420_mappa"](
                         tuple([0.0] * 25)),
                     lambda: _F["mh420_curva"](None),
                     lambda: _F["mh420_curva"](self._xs(), 1.0, -1.0),
                     lambda: _F["mh420_curva"](self._xs(), 0.0, 1.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh420_mappa"](DEMO)
        assert abs(m["gl"] - GL) < 1e-12

