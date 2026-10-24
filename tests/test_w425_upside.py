
"""Test tab425 '🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh425_num", "mh425_parse_serie", "mh425_updown",
           "mh425_ratio", "mh425_verdetto", "mh425_curva",
           "mh425_mappa", "mh420_num", "mh420_gain_loss",
           "mh417_num", "mh417_ft")

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
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
UPR = 0.737440705837383
UP = 2.8777777777777778
DD = 3.9023853104365682
ELOSS = 1.536111111111111
GL = 1.8734177215189873


class TestRegistry425:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 685
        assert "tab425" in dvars
        assert "tab425" in withs

    def test_titoli_allineati_419_420_421_422_423_424_425(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab419")] == TITLE419
        assert titoli[dvars.index("tab420")] == TITLE420
        assert titoli[dvars.index("tab421")] == TITLE421
        assert titoli[dvars.index("tab422")] == TITLE422
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425

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


class TestUPR425:
    def _xs(self):
        return _F["mh425_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh425_mappa"](xs, 0.0)
        assert abs(m["upr"] - UPR) < 1e-12
        assert abs(m["up"] - UP) < 1e-12
        assert abs(m["dd"] - DD) < 1e-12
        assert abs(m["e_loss"] - ELOSS) < 1e-12
        assert abs(m["gain_loss"] - GL) < 1e-12
        # E[guadagno+]=2.8778% (lo stesso del Gain-Loss tab420),
        # DD=3.9024% > E[perdita-]=1.5361%
        assert abs(m["up"] - 2.8778) < 1e-3
        assert abs(m["dd"] - 3.9024) < 1e-3
        assert abs(m["e_loss"] - 1.5361) < 1e-3
        assert m["dd"] > m["e_loss"]
        assert m["n_up"] == 30
        assert m["n_dn"] == 6
        assert m["upr"] < 1.0
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.7 < m["upr"] < 0.8
        # definizione: upr = up / dd
        assert abs(m["upr"] - m["up"] / m["dd"]) < 1e-12
        # dd >= e_loss >= 0 (RMS >= AM)
        assert m["dd"] >= m["e_loss"] >= 0.0
        assert m["upr"] >= 0.0

    def test_definizione_a_mano(self):
        # per-periodo, indipendente dall'helper: guadagni positivi e
        # quadrati delle perdite, media su TUTTI gli N periodi
        xs = list(self._xs())
        n = len(xs)
        up_mano = sum(x for x in xs if x > 0.0) / n
        dd_mano = math.sqrt(sum(x * x for x in xs if x < 0.0) / n)
        el_mano = sum(-x for x in xs if x < 0.0) / n
        k = _F["mh425_ratio"](tuple(xs), 0.0)
        assert abs(k["up"] - up_mano) < 1e-12
        assert abs(k["dd"] - dd_mano) < 1e-12
        assert abs(k["e_loss"] - el_mano) < 1e-12
        assert abs(k["upr"] - up_mano / dd_mano) < 1e-12
        u = _F["mh425_updown"](tuple(xs))
        assert abs(u["up"] - up_mano) < 1e-12
        assert abs(u["dd"] - dd_mano) < 1e-12
        assert abs(u["e_loss"] - el_mano) < 1e-12
        assert u["n_up"] == 30 and u["n_dn"] == 6

    def test_chiave_teorica_upr_uguale_ft12(self):
        # CHIAVE TEORICA 1: UPR(T) = FT_{1,2}(T) ESATTO.
        # tab417 calcola gia' "upr" = upm_1 / dd: l'UPR e' il
        # Farinelli-Tibiletti con p=1, q=2. Ottavo gemello ancorato
        # alla radice della famiglia.
        xs = self._xs()
        for T in (-2.0, 0.0, 1.5):
            mio = _F["mh425_ratio"](xs, T)["upr"]
            ft = _F["mh417_ft"](xs, T, 1, 2)
            assert abs(mio - ft["upr"]) < 1e-12
            assert abs(_F["mh425_mappa"](xs, T)["ft21"]
                       - ft["upr"]) < 1e-12
        # sulla demo a T=0: UPR = 0.7374
        assert abs(_F["mh417_ft"](xs, 0.0, 1, 2)["upr"]
                   - 0.7374) < 1e-3

    def test_chiave_teorica_upr_minore_uguale_gainloss(self):
        # CHIAVE TEORICA 2: per eccesso > 0 vale SEMPRE
        #   UPR <= Gain-Loss (tab420),
        # perche' DD = RMS(perdite) >= E[perdite] (RMS >= AM).
        # Gemello quadratico del Gain-Loss: STESSO numeratore
        # (E[guadagno+]), denominatore piu' "severo".
        # Sulla demo: UPR 0.7374 < GL 1.8734.
        xs = self._xs()
        upr = _F["mh425_ratio"](xs, 0.0)["upr"]
        gl = _F["mh420_gain_loss"](xs)["gl"]
        assert 0.0 < upr < gl
        assert abs(upr - 0.7374) < 0.005
        assert abs(gl - 1.8734) < 0.005
        # stesso numeratore esatto
        assert abs(_F["mh425_ratio"](xs, 0.0)["up"]
                   - _F["mh420_gain_loss"](xs)["e_gain"]) < 1e-12
        # rapporto dei ratio = rapporto inverso dei denominatori
        k = _F["mh425_ratio"](xs, 0.0)
        assert abs(gl / upr - k["dd"] / k["e_loss"]) < 1e-9
        # con la convenzione su tutti gli N periodi (zeri inclusi),
        # dd > e_loss in modo STRETTO su ogni serie mista: gli zeri
        # dei periodi di guadagno rendono RMS > AM stretto, quindi
        # UPR < GL stretto (l'uguaglianza RMS==AM vorrebbe tutte le
        # parti di perdita uguali, impossibile con guadagni presenti)
        mix2 = tuple([3.0] * 30 + [-2.0] * 6)
        km2 = _F["mh425_ratio"](mix2, 0.0)
        assert km2["dd"] > km2["e_loss"]
        assert km2["upr"] < _F["mh420_gain_loss"](mix2)["gl"]
        # caso degenere: solo perdite uguali -> up=0 -> upr == gl == 0
        allloss = tuple([-2.0] * 25)
        assert _F["mh425_ratio"](allloss, 0.0)["upr"] == 0.0
        assert _F["mh420_gain_loss"](allloss)["gl"] == 0.0

    def test_chiave_teorica_upr_maggiore_uguale_sortino(self):
        # CHIAVE TEORICA 3: UPR(T=0) >= Sortino(T=0) SEMPRE.
        # Stesso denominatore DD, numeratore E[R+] >= E[R]
        # (uguaglianza sse nessuna perdita).
        xs = self._xs()
        k = _F["mh425_ratio"](xs, 0.0)
        sortino_mano = (sum(xs) / len(xs)) / k["dd"]
        assert k["upr"] >= sortino_mano
        # 1.3417 e' la media arrotondata a 4 decimali: tolleranza
        # coerente con l'arrotondamento
        assert abs(sortino_mano - 1.3417 / k["dd"]) < 1e-4
        # serie mista: il guadagno atteso domina la media
        mix = tuple([4.0] * 18 + [-1.0] * 18)
        km = _F["mh425_ratio"](mix, 0.0)
        assert km["upr"] > (sum(mix) / len(mix)) / km["dd"]

    def test_invarianza_di_scala(self):
        # CHIAVE TEORICA 4 (proprieta' intenzionale, non bug): l'UPR
        # lavora sui momenti per-periodo, non sul percorso
        # dell'equity -> UPR(2x, T=0) == UPR(x, T=0) ESATTO.
        # A differenza dei 4 gemelli drawdown-di-percorso (Pain,
        # UPI, Calmar, MAR: drawdown non lineare nell'equity
        # composta, test di non-invarianza in tab421-424).
        xs = self._xs()
        base = _F["mh425_ratio"](xs, 0.0)["upr"]
        sc = tuple(2.0 * x for x in xs)
        assert abs(_F["mh425_ratio"](sc, 0.0)["upr"] - base) < 1e-12
        assert abs(_F["mh425_ratio"](tuple(0.5 * x for x in xs), 0.0)
                   ["upr"] - base) < 1e-12

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        base = F["mh425_ratio"](xs, 0.0)["upr"]
        # alzare i rendimenti di +1: up sale, dd cala -> UPR sale
        up = tuple(x + 1.0 for x in xs)
        assert F["mh425_ratio"](up, 0.0)["upr"] > base
        # approfondire i crash: dd sale -> UPR scende
        dn = tuple(x - 1.0 if x < 0.0 else x for x in xs)
        assert F["mh425_ratio"](dn, 0.0)["upr"] < base
        # alzare il target: up cala, dd sale -> UPR scende
        assert F["mh425_ratio"](xs, 2.5)["upr"] < base
        assert F["mh425_ratio"](xs, -2.5)["upr"] > base

    def test_infinito_senza_downside(self):
        # mai sotto la soglia: dd=0, up>0 -> +inf
        k = _F["mh425_ratio"](tuple([1.0] * 25), 0.0)
        assert math.isinf(k["upr"]) and k["upr"] > 0
        assert k["dd"] == 0.0
        assert _F["mh425_verdetto"](k["upr"]).startswith("MOLTO FORTE")
        # serie piatta sulla soglia: up=0, dd=0 -> non definito
        with pytest.raises(ValueError):
            _F["mh425_ratio"](tuple([0.0] * 25), 0.0)
        # nessun guadagno ma downside presente: upr=0.0 (NON inf)
        k0 = _F["mh425_ratio"](tuple([2.0] * 25), 5.0)
        assert k0["upr"] == 0.0
        assert k0["dd"] == 3.0
        assert _F["mh425_verdetto"](k0["upr"]).startswith("NEGATIVO")
        # -inf impossibile: il numeratore e' sempre >= 0
        k2 = _F["mh425_ratio"](tuple([2.0] * 25), 0.0)
        assert math.isinf(k2["upr"]) and k2["upr"] > 0

    def test_curva(self):
        F = _F
        xs = self._xs()
        c = F["mh425_curva"](xs, -2.0, 2.0, 1.0)
        assert len(c) == 5
        assert [t for t, _ in c] == [-2.0, -1.0, 0.0, 1.0, 2.0]
        # il punto a T=0 e' l'UPR della demo
        assert abs(dict(c)[0.0] - UPR) < 1e-12
        # monotona decrescente in T (up cala, dd sale)
        uu = [u for _, u in c]
        assert all(u is not None for u in uu)
        assert all(a > b for a, b in zip(uu, uu[1:]))
        # ogni punto coincide con upr al target T
        for t, u in c:
            mio = F["mh425_ratio"](xs, t)["upr"]
            assert abs(u - mio) < 1e-12
        with pytest.raises(ValueError):
            F["mh425_curva"](None)
        with pytest.raises(ValueError):
            F["mh425_curva"](xs, 2.0, -2.0, 1.0)
        with pytest.raises(ValueError):
            F["mh425_curva"](xs, -2.0, 2.0, 0.0)

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh425_verdetto"](0.0).startswith("NEGATIVO")
        assert F["mh425_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh425_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh425_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh425_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh425_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh425_verdetto"](2.0).startswith("BUONO")
        assert F["mh425_verdetto"](2.99).startswith("BUONO")
        assert F["mh425_verdetto"](3.0).startswith("FORTE")
        assert F["mh425_verdetto"](4.99).startswith("FORTE")
        assert F["mh425_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh425_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh425_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh425_verdetto"](True)
        with pytest.raises(ValueError):
            F["mh425_verdetto"](-0.5)

    def test_casi_degeneri(self):
        F = _F
        with pytest.raises(ValueError):
            F["mh425_ratio"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh425_mappa"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh425_mappa"]((1.0,) * 19, 0.0)
        with pytest.raises(ValueError):
            F["mh425_mappa"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh425_updown"]((1.0,) * 19)
        # target cattivo contro la sua funzione (lezione tab417)
        for _t in (True, "x", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                F["mh425_ratio"](self._xs(), _t)

    def test_validatori(self):
        for _bad in (lambda: _F["mh425_ratio"](None, 0.0),
                     lambda: _F["mh425_ratio"]((1.0,) * 19, 0.0),
                     lambda: _F["mh425_ratio"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh425_ratio"](self._xs(), True),
                     lambda: _F["mh425_ratio"](self._xs(),
                                               float("nan")),
                     lambda: _F["mh425_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh425_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh425_parse_serie"](None),
                     lambda: _F["mh425_num"](True, "x"),
                     lambda: _F["mh425_num"](float("nan"), "x"),
                     lambda: _F["mh425_mappa"]((1.0,) * 19, 0.0),
                     lambda: _F["mh425_mappa"](None, 0.0),
                     lambda: _F["mh425_mappa"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh425_mappa"](self._xs(), True),
                     lambda: _F["mh425_curva"](None),
                     lambda: _F["mh425_curva"](self._xs(), 1.0, -1.0),
                     lambda: _F["mh425_curva"](self._xs(), 0.0, 1.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh425_mappa"](DEMO, 0.0)
        assert abs(m["upr"] - UPR) < 1e-12
        assert abs(m["gain_loss"] - _F["mh420_gain_loss"](
            self._xs())["gl"]) < 1e-12
        assert abs(m["ft21"] - _F["mh417_ft"](self._xs(), 0.0, 1, 2)
                   ["upr"]) < 1e-12
        # a T != 0 il confronto col Gain-Loss non e' definito
        m2 = _F["mh425_mappa"](self._xs(), 2.0)
        assert m2["gain_loss"] is None
        assert abs(m2["ft21"] - _F["mh417_ft"](self._xs(), 2.0, 1, 2)
                   ["upr"]) < 1e-12

