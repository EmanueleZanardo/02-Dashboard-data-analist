
"""Test tab428 '⏱️ Tempo sott'acqua: durata dei drawdown e recupero': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh428_num", "mh428_parse_serie", "mh428_equity",
           "mh428_drawdowns", "mh428_episodes", "mh428_durations",
           "mh428_verdetto", "mh428_mappa",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain")

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
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
TUW = 16.666666666666664
NEP = 1
UW = 6
MEANDUR = 6.0
MAXDUR = 6.0
MEDDUR = 6.0
MEANREC = 0.0
MAXREC = 0.0
NCHIUSI = 0
CURDD = 44.15217408197824
CURDUR = 6.0
LONGESTDD = 44.15217408197824
PAIN = 4.694975808579396
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
CONCTUW = 50.0
CONCNEP = 1
CONCMEANDUR = 10.0
CONCMAXDUR = 10.0
CONCPAIN = 11.880009227646003
RIMTUW = 50.0
RIMNEP = 10
RIMMEANDUR = 1.0
RIMMAXDUR = 1.0
RIMMEANREC = 1.0
RIMNCHIUSI = 10
RIMPAIN = 2.5000000000000027
ALTTUW = 95.0
ALTNEP = 1
ALTMAXDUR = 19.0
ALTPAIN = 15.035665573198646


class TestRegistry428:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 533
        assert "tab428" in dvars
        assert "tab428" in withs

    def test_titoli_allineati_422_423_424_425_426_427_428(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab422")] == TITLE422
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426
        assert titoli[dvars.index("tab427")] == TITLE427
        assert titoli[dvars.index("tab428")] == TITLE428

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


class TestDurata428:
    def _xs(self):
        return _F["mh428_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh428_mappa"](xs, 40.0)
        d = m["demo"]
        assert abs(d["tuw"] - TUW) < 1e-12
        assert d["n_episodi"] == NEP
        assert d["underwater"] == UW
        assert abs(d["mean_dur"] - MEANDUR) < 1e-12
        assert abs(d["max_dur"] - MAXDUR) < 1e-12
        assert abs(d["median_dur"] - MEDDUR) < 1e-12
        assert abs(d["mean_recovery"] - MEANREC) < 1e-12
        assert abs(d["max_recovery"] - MAXREC) < 1e-12
        assert d["n_chiusi"] == NCHIUSI
        assert abs(d["current_dd"] - CURDD) < 1e-12
        assert abs(d["current_dur"] - CURDUR) < 1e-12
        assert abs(d["longest_max_dd"] - LONGESTDD) < 1e-12
        assert abs(d["pain"] - PAIN) < 1e-12
        assert abs(d["max_dd"] - MAXDD) < 1e-12
        assert abs(d["mean"] - MEAN) < 1e-12
        # demo: 1 episodio, 6 sott'acqua su 36, TUW 16.6667%,
        # durate 6/6/6, nessun chiuso, APERTO, corrente = maxDD
        assert d["n_episodi"] == 1
        assert d["underwater"] == 6
        assert abs(d["tuw"] - 16.6667) < 1e-3
        assert d["mean_dur"] == 6.0
        assert d["max_dur"] == 6.0
        assert d["median_dur"] == 6.0
        assert d["mean_recovery"] == 0.0
        assert d["n_chiusi"] == 0
        assert d["aperto"] is True
        assert abs(d["current_dd"] - 44.1522) < 1e-3
        assert d["current_dur"] == 6.0
        assert abs(d["longest_max_dd"] - 44.1522) < 1e-3
        assert abs(d["mean"] - 1.3417) < 1e-3
        assert abs(d["max_dd"] - 44.1522) < 1e-3
        assert abs(d["pain"] - 4.6950) < 1e-3
        assert m["soglia"] == 40.0
        assert m["verdetto"].startswith("CONTROLLATO")

    def test_definizione_a_mano(self):
        # equity composta -> running max (peak iniziale 100) ->
        # drawdown punto per punto -> episodi a mano (run di dd > 0)
        xs = list(self._xs())
        eq = 100.0
        peak = 100.0
        dds = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            peak = max(peak, eq)
            dds.append((peak - eq) / peak * 100.0)
        n = len(xs)
        # episodi a mano
        eps_mano = []
        i = 0
        while i < n:
            if dds[i] > 0.0:
                s = i
                while i < n and dds[i] > 0.0:
                    i += 1
                e = i - 1
                seg = dds[s:e + 1]
                eps_mano.append({"start": s, "end": e,
                                 "durata": e - s + 1,
                                 "max_dd": max(seg),
                                 "mean_dd": sum(seg) / len(seg),
                                 "chiuso": e + 1 < n})
            else:
                i += 1
        eps = _F["mh428_episodes"](tuple(xs))
        assert len(eps) == len(eps_mano) == 1
        for a, b in zip(eps, eps_mano):
            assert a["start"] == b["start"]
            assert a["end"] == b["end"]
            assert a["durata"] == b["durata"]
            assert abs(a["max_dd"] - b["max_dd"]) < 1e-9
            assert abs(a["mean_dd"] - b["mean_dd"]) < 1e-9
            assert a["chiuso"] == b["chiuso"]
        d = _F["mh428_durations"](tuple(xs))
        # CHIAVE 1 (partizione): somma durate == periodi sott'acqua
        uw_mano = sum(1 for v in dds if v > 0.0)
        assert sum(e["durata"] for e in eps) == uw_mano == d["underwater"]
        assert abs(d["tuw"] - uw_mano / n * 100.0) < 1e-12
        assert abs(d["mean_dur"] - uw_mano / len(eps)) < 1e-12
        # Pain scomposto per episodi
        pain_ep = sum(e["mean_dd"] * e["durata"] for e in eps) / n
        assert abs(pain_ep - d["pain"]) < 1e-9
        assert abs(d["pain"] - sum(dds) / n) < 1e-12
        assert abs(d["max_dd"] - max(dds)) < 1e-12
        assert abs(d["mean"] - sum(xs) / n) < 1e-12
        dd = _F["mh428_drawdowns"](tuple(xs))
        assert len(dd) == n
        for a, b in zip(dd, dds):
            assert abs(a - b) < 1e-9
        eqs = _F["mh428_equity"](tuple(xs))
        assert abs(eqs[-1] - eq) < 1e-9

    def test_chiave_stesso_tuw_struttura_opposta(self):
        # CHIAVE TEORICA 2: STESSO TUW (50%), struttura opposta.
        # Rimbalzo: 10 episodi x 1, tutti chiusi, recupero medio 1.
        # Concentrata: 1 episodio x 10, APERTO, nessun recupero.
        conc = tuple([2.0] * 10 + [-5.0] * 10)
        rimb = tuple([-5.0, 6.0] * 10)
        dc = _F["mh428_durations"](conc)
        dr = _F["mh428_durations"](rimb)
        assert abs(dc["tuw"] - CONCTUW) < 1e-12
        assert dc["n_episodi"] == CONCNEP
        assert abs(dc["mean_dur"] - CONCMEANDUR) < 1e-12
        assert abs(dc["max_dur"] - CONCMAXDUR) < 1e-12
        assert abs(dc["pain"] - CONCPAIN) < 1e-12
        assert abs(dr["tuw"] - RIMTUW) < 1e-12
        assert dr["n_episodi"] == RIMNEP
        assert abs(dr["mean_dur"] - RIMMEANDUR) < 1e-12
        assert abs(dr["max_dur"] - RIMMAXDUR) < 1e-12
        assert abs(dr["mean_recovery"] - RIMMEANREC) < 1e-12
        assert dr["n_chiusi"] == RIMNCHIUSI
        assert abs(dr["pain"] - RIMPAIN) < 1e-12
        assert abs(dc["tuw"] - 50.0) < 1e-12
        assert abs(dr["tuw"] - 50.0) < 1e-12
        assert dc["tuw"] == dr["tuw"]
        assert dc["n_episodi"] == 1
        assert dr["n_episodi"] == 10
        assert dc["mean_dur"] == 10.0
        assert dr["mean_dur"] == 1.0
        assert dc["max_dur"] == 10.0
        assert dr["max_dur"] == 1.0
        assert dc["aperto"] is True
        assert dr["aperto"] is False
        assert dc["n_chiusi"] == 0
        assert dr["n_chiusi"] == 10
        assert dc["mean_recovery"] == 0.0
        assert dr["mean_recovery"] == 1.0
        assert dc["current_dur"] == 10.0
        assert dr["current_dur"] == 0.0
        assert abs(dc["pain"] - 11.8800) < 1e-3
        assert abs(dr["pain"] - 2.5000) < 1e-3

    def test_chiave_aperto_chiuso_e_alternate(self):
        # CHIAVE TEORICA 3: episodio aperto <=> drawdown finale > 0.
        # Demo: aperto (finale = maxDD). Rimbalzo: tutto chiuso.
        # Alternate: 1 episodio da 19, TUW 95% (persistenza).
        xs = self._xs()
        d = _F["mh428_durations"](xs)
        assert d["aperto"] is True
        assert d["current_dd"] > 0.0
        assert abs(d["current_dd"] - d["max_dd"]) < 1e-12
        rimb = _F["mh428_durations"](tuple([-5.0, 6.0] * 10))
        assert rimb["aperto"] is False
        assert rimb["current_dd"] == 0.0
        # piatta / solo guadagni: 0 episodi, TUW 0, ROBUSTO
        for _serie in (tuple([0.0] * 25), tuple([1.0] * 25)):
            _d = _F["mh428_durations"](_serie)
            assert _d["n_episodi"] == 0
            assert _d["underwater"] == 0
            assert _d["tuw"] == 0.0
            assert _d["mean_dur"] == 0.0
            assert _d["max_dur"] == 0.0
            assert _d["aperto"] is False
            _m = _F["mh428_mappa"](_serie, 40.0)
            assert _m["verdetto"].startswith("ROBUSTO")
        # alternate: 19 periodi sott'acqua su 20
        alt = tuple([2.0, -5.0] * 10)
        da = _F["mh428_durations"](alt)
        assert abs(da["tuw"] - ALTTUW) < 1e-12
        assert da["n_episodi"] == ALTNEP
        assert abs(da["max_dur"] - ALTMAXDUR) < 1e-12
        assert abs(da["pain"] - ALTPAIN) < 1e-12
        assert abs(da["tuw"] - 95.0) < 1e-12
        assert da["n_episodi"] == 1
        assert da["max_dur"] == 19.0
        assert da["aperto"] is True
        assert abs(da["pain"] - 15.0357) < 1e-3
        # solo perdite: 1 episodio aperto lungo n, TUW 100%
        lo = _F["mh428_durations"](tuple([-2.0] * 25))
        assert lo["n_episodi"] == 1
        assert lo["tuw"] == 100.0
        assert lo["max_dur"] == 25.0
        assert lo["aperto"] is True
        assert lo["current_dur"] == 25.0

    def test_crosscheck_gemelli(self):
        # tab427 path/CDaR e tab424 Pain sulla demo: stessi numeri
        # (stessa convenzione peak iniziale = 100).
        xs = self._xs()
        d = _F["mh428_mappa"](xs, 40.0)["demo"]
        p427 = _F["mh427_path"](xs)
        assert abs(p427["mean"] - d["mean"]) < 1e-12
        assert abs(p427["max_dd"] - d["max_dd"]) < 1e-12
        assert abs(p427["pain"] - d["pain"]) < 1e-12
        c427 = _F["mh427_cdar"](xs, 10.0)
        assert abs(c427["max_dd"] - d["max_dd"]) < 1e-12
        pain424 = _F["mh424_pain"](xs)
        assert abs(pain424["pain"] - d["pain"]) < 1e-12
        assert abs(pain424["max_dd"] - d["max_dd"]) < 1e-12
        # max_dd sugli episodi = maxDD di percorso
        assert abs(max(e["max_dd"] for e in d["episodi"])
                   - d["max_dd"]) < 1e-12

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh428_verdetto"](0.0, 40.0).startswith("ROBUSTO")
        assert F["mh428_verdetto"](16.6667, 40.0).startswith("CONTROLLATO")
        assert F["mh428_verdetto"](19.9, 40.0).startswith("CONTROLLATO")
        assert F["mh428_verdetto"](20.0, 40.0).startswith("SENSIBILE")
        assert F["mh428_verdetto"](39.9, 40.0).startswith("SENSIBILE")
        assert F["mh428_verdetto"](40.0, 40.0).startswith("FRAGILE")
        assert F["mh428_verdetto"](59.9, 40.0).startswith("FRAGILE")
        assert F["mh428_verdetto"](60.0, 40.0).startswith("MOLTO FRAGILE")
        assert F["mh428_verdetto"](79.9, 40.0).startswith("MOLTO FRAGILE")
        assert F["mh428_verdetto"](80.0, 40.0).startswith("CRITICO")
        assert F["mh428_verdetto"](100.0, 40.0).startswith("CRITICO")
        for _bad in (lambda: F["mh428_verdetto"](-1.0, 40.0),
                     lambda: F["mh428_verdetto"](100.5, 40.0),
                     lambda: F["mh428_verdetto"](float("nan"), 40.0),
                     lambda: F["mh428_verdetto"](10.0, 0.0),
                     lambda: F["mh428_verdetto"](10.0, 101.0),
                     lambda: F["mh428_verdetto"](10.0, True),
                     lambda: F["mh428_verdetto"]("x", 40.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_casi_degeneri(self):
        F = _F
        # serie piatta: 0 episodi, TUW 0, verdetto ROBUSTO
        d = F["mh428_durations"](tuple([0.0] * 25))
        assert d["n_episodi"] == 0 and d["tuw"] == 0.0
        assert d["mean_dur"] == 0.0 and d["max_dur"] == 0.0
        assert d["mean_recovery"] == 0.0 and d["n_chiusi"] == 0
        m = F["mh428_mappa"](tuple([0.0] * 25), 40.0)
        assert m["verdetto"].startswith("ROBUSTO")
        # solo guadagni: 0 episodi
        g = F["mh428_durations"](tuple([1.0] * 25))
        assert g["n_episodi"] == 0 and g["tuw"] == 0.0
        # solo perdite: 1 episodio aperto, TUW 100%
        lo = F["mh428_durations"](tuple([-2.0] * 25))
        assert lo["n_episodi"] == 1 and lo["tuw"] == 100.0
        assert lo["aperto"] is True
        # tuw / soglia fuori dominio
        for _bad in (lambda: F["mh428_verdetto"](-0.5, 40.0),
                     lambda: F["mh428_verdetto"](100.5, 40.0),
                     lambda: F["mh428_verdetto"](10.0, 0.0),
                     lambda: F["mh428_verdetto"](10.0, 101.0),
                     lambda: F["mh428_mappa"](self._xs(), 0.0),
                     lambda: F["mh428_mappa"](self._xs(), 101.0),
                     lambda: F["mh428_mappa"]((1.0,) * 19, 40.0),
                     lambda: F["mh428_mappa"](None, 40.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_validatori(self):
        for _bad in (lambda: _F["mh428_durations"](None),
                     lambda: _F["mh428_durations"]((1.0,) * 19),
                     lambda: _F["mh428_durations"](self._xs()[:5]),
                     lambda: _F["mh428_episodes"]((1.0,) * 19),
                     lambda: _F["mh428_episodes"](None),
                     lambda: _F["mh428_drawdowns"]((1.0,) * 19),
                     lambda: _F["mh428_equity"]((1.0,) * 19),
                     lambda: _F["mh428_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh428_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh428_parse_serie"](None),
                     lambda: _F["mh428_num"](True, "x"),
                     lambda: _F["mh428_num"](float("nan"), "x"),
                     lambda: _F["mh428_num"](float("inf"), "x"),
                     lambda: _F["mh428_num"]("x", "x"),
                     lambda: _F["mh428_mappa"]((1.0,) * 19, 40.0),
                     lambda: _F["mh428_mappa"](None, 40.0)):
            with pytest.raises(ValueError):
                _bad()

