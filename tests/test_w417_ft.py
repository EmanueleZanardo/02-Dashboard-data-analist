"""Test tab417 '🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh417_num", "mh417_parse_serie", "mh417_upm", "mh417_lpm",
           "mh417_ft", "mh417_verdetto", "mh417_mappa", "mh412_omega",
           "mh412_num")

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
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
DEMO_P = 1
DEMO_Q = 2
DEMO_T = 0.0
FT = 0.737440705837383
FT11 = 1.8734177215189876
UPR = 0.737440705837383
OMEGA = 1.8734177215189876
DOWN_POT = 3.9023853104365682


class TestRegistry417:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 587
        assert "tab417" in dvars
        assert "tab417" in withs

    def test_titoli_allineati_412_413_414_415_416_417(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413
        assert titoli[dvars.index("tab414")] == TITLE414
        assert titoli[dvars.index("tab415")] == TITLE415
        assert titoli[dvars.index("tab416")] == TITLE416
        assert titoli[dvars.index("tab417")] == TITLE417

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


class TestFT417:
    def _xs(self):
        return _F["mh417_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh417_mappa"](xs, DEMO_T, DEMO_P, DEMO_Q)
        assert m["p"] == DEMO_P
        assert m["q"] == DEMO_Q
        assert m["soglia"] == DEMO_T
        assert abs(m["ft"] - FT) < 1e-12
        assert abs(m["ft11"] - FT11) < 1e-12
        assert abs(m["upr"] - UPR) < 1e-12
        assert abs(m["ft"] - UPR) < 1e-15  # demo con p=1, q=2
        assert abs(m["omega"] - OMEGA) < 1e-12
        assert abs(m["down_pot"] - DOWN_POT) < 1e-12
        assert abs(m["p_sopra"] - 30.0 / 36.0) < 1e-12
        assert abs(m["excess"] - (m["upm_1"] - m["lpm_1"])) < 1e-12
        # Omega accettabile ma FT(p=1,q=2) negativo: punire di piu' il
        # downside mangia il profilo
        assert m["verdetto"].startswith("NEGATIVO")
        assert 1.85 < m["ft11"] < 1.90
        assert 0.70 < m["upr"] < 0.78

    def test_definizione_ft_a_mano(self):
        # FT_{p,q} = UPM_p^(1/p) / LPM_q^(1/q)
        xs = list(self._xs())
        n = len(xs)
        T = 0.0
        for P, Q in ((1, 1), (1, 2), (2, 2), (2, 3)):
            upm = sum(max(x - T, 0.0) ** P for x in xs) / n
            lpm = sum(max(T - x, 0.0) ** Q for x in xs) / n
            ft = (upm ** (1.0 / P)) / (lpm ** (1.0 / Q))
            k = _F["mh417_ft"](tuple(xs), T, P, Q)
            assert abs(k["upm_p"] - upm) < 1e-12, (P, Q)
            assert abs(k["lpm_q"] - lpm) < 1e-12, (P, Q)
            assert abs(k["ft"] - ft) < 1e-12, (P, Q)
            assert abs(k["up_pot"] - upm ** (1.0 / P)) < 1e-12, (P, Q)
            assert abs(k["down_pot"] - lpm ** (1.0 / Q)) < 1e-12, (P, Q)
            assert abs(_F["mh417_upm"](tuple(xs), T, P) - upm) < 1e-12
            assert abs(_F["mh417_lpm"](tuple(xs), T, Q) - lpm) < 1e-12

    def test_ft11_eq_omega(self):
        # FT_{1,1} = upside/downside = Omega, esatto (tab412)
        xs = self._xs()
        k = _F["mh417_ft"](xs, 0.0, 1, 1)
        o = _F["mh412_omega"](xs, 0.0)
        assert abs(k["ft11"] - o["omega"]) < 1e-12
        assert abs(k["omega"] - o["omega"]) < 1e-12
        assert abs(k["ft"] - o["omega"]) < 1e-12
        assert abs(k["upm_1"] - o["upside"]) < 1e-12
        assert abs(k["lpm_1"] - o["downside"]) < 1e-12

    def test_upr_a_mano(self):
        # Upside potential ratio = upside / downside deviation
        xs = list(self._xs())
        n = len(xs)
        up = sum(max(x - 0.0, 0.0) for x in xs) / n
        dd = math.sqrt(sum(max(0.0 - x, 0.0) ** 2 for x in xs) / n)
        k = _F["mh417_ft"](tuple(xs), 0.0, 1, 2)
        assert abs(k["upr"] - up / dd) < 1e-12
        assert abs(k["up_pot"] - up) < 1e-12
        assert abs(k["down_pot"] - dd) < 1e-12

    def test_monotonia_q(self):
        # a parita' di p, punire di piu' il downside (q alto) mangia FT
        F = _F
        xs = self._xs()
        fts = [F["mh417_ft"](xs, 0.0, 1, Q)["ft"] for Q in (1, 2, 3, 4)]
        assert fts[0] > fts[1] > fts[2] > fts[3]
        # a parita' di q, premiare di piu' l'upside (p alto) alza FT
        # (norma L^p crescente in p su misura di probabilita')
        ftp = [F["mh417_ft"](xs, 0.0, P, 1)["ft"] for P in (1, 2, 3)]
        assert ftp[0] < ftp[1] < ftp[2]

    def test_infinito_senza_downside(self):
        # tutti sopra la soglia: nessun downside -> +inf
        k = _F["mh417_ft"](tuple([1.0] * 25), 0.0, 1, 2)
        assert math.isinf(k["ft"])
        assert math.isinf(k["ft11"])
        assert math.isinf(k["upr"])
        assert _F["mh417_verdetto"](k["ft"]).startswith("MOLTO FORTE")

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh417_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh417_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh417_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh417_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh417_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh417_verdetto"](2.0).startswith("BUONO")
        assert F["mh417_verdetto"](2.99).startswith("BUONO")
        assert F["mh417_verdetto"](3.0).startswith("FORTE")
        assert F["mh417_verdetto"](4.99).startswith("FORTE")
        assert F["mh417_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh417_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh417_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh417_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta sulla soglia -> ValueError
        with pytest.raises(ValueError):
            F["mh417_ft"](tuple([0.0] * 25), 0.0, 1, 2)
        with pytest.raises(ValueError):
            F["mh417_mappa"](tuple([1.0] * 25), 1.0, 1, 2)
        with pytest.raises(ValueError):
            F["mh417_mappa"]((1.0,) * 19)
        # p, q non interi o fuori [1, 6] -> ValueError (separati: ogni
        # ordine cattivo va testato contro la sua funzione, non in
        # coppia con un ordine buono che non solleva)
        for _p in (0, 7, 1.5, True, "x", float("nan")):
            with pytest.raises(ValueError):
                F["mh417_ft"](self._xs(), 0.0, _p, 2)
            with pytest.raises(ValueError):
                F["mh417_upm"](self._xs(), 0.0, _p)
        for _q in (0, 7, 2.5, "x", float("nan")):
            with pytest.raises(ValueError):
                F["mh417_ft"](self._xs(), 0.0, 1, _q)
            with pytest.raises(ValueError):
                F["mh417_lpm"](self._xs(), 0.0, _q)

    def test_validatori(self):
        for _bad in (lambda: _F["mh417_ft"](None),
                     lambda: _F["mh417_ft"]((1.0,) * 19),
                     lambda: _F["mh417_ft"]((1.0,) * 25,
                                            float("nan")),
                     lambda: _F["mh417_ft"](tuple([0.0] * 25), 0.0, 1, 2),
                     lambda: _F["mh417_ft"](self._xs(), 0.0, 0, 2),
                     lambda: _F["mh417_ft"](self._xs(), 0.0, 1, 7),
                     lambda: _F["mh417_ft"](self._xs(), 0.0, 1.5, 2),
                     lambda: _F["mh417_upm"](None, 0.0, 1),
                     lambda: _F["mh417_upm"]((1.0,) * 19, 0.0, 1),
                     lambda: _F["mh417_upm"](self._xs(), 0.0, 0),
                     lambda: _F["mh417_lpm"](None, 0.0, 2),
                     lambda: _F["mh417_lpm"]((1.0,) * 19, 0.0, 2),
                     lambda: _F["mh417_lpm"](self._xs(), 0.0, 7),
                     lambda: _F["mh417_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh417_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh417_parse_serie"](None),
                     lambda: _F["mh417_num"](True, "x"),
                     lambda: _F["mh417_num"](float("nan"), "x"),
                     lambda: _F["mh417_mappa"]((1.0,) * 19),
                     lambda: _F["mh417_mappa"](None),
                     lambda: _F["mh417_mappa"](
                         tuple([0.0] * 25), 0.0, 1, 2),
                     lambda: _F["mh417_mappa"](self._xs(), 0.0, 0, 2)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh417_mappa"](DEMO, DEMO_T, DEMO_P, DEMO_Q)
        assert abs(m["ft"] - FT) < 1e-12

