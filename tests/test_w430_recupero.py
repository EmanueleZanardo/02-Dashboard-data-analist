
"""Test tab430 '🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh430_num", "mh430_parse_serie", "mh430_equity",
           "mh430_drawdowns", "mh430_rebound", "mh430_episodes",
           "mh430_recovery", "mh430_worst", "mh430_verdetto",
           "mh430_mappa",
           "mh429_num", "mh429_equity", "mh429_drawdowns",
           "mh429_worst", "mh429_attribution",
           "mh428_num", "mh428_equity", "mh428_drawdowns",
           "mh428_episodes", "mh428_durations",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain")

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
TITLE428 = "⏱️ Tempo sott'acqua: durata dei drawdown e recupero"
TITLE427 = "🛡 CDaR: la perdita media dei peggiori drawdown"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
REBOUND = 79.05799976312166
NEP = 1
NCHIUSI = 0
NAPERTI = 1
PEAKPER = 30
TROUGH = 36
FASTREC = 1
SLOWREC = 5
REB10 = 11.11111111111111
REB20 = 25.0
REB50 = 100.0
REB80 = 400.0
REB90 = 900.0


class TestRegistry430:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 556
        assert "tab430" in dvars
        assert "tab430" in withs

    def test_titoli_allineati_424_425_426_427_428_429_430(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426
        assert titoli[dvars.index("tab427")] == TITLE427
        assert titoli[dvars.index("tab428")] == TITLE428
        assert titoli[dvars.index("tab429")] == TITLE429
        assert titoli[dvars.index("tab430")] == TITLE430

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


class TestRecupero430:
    def _xs(self):
        return _F["mh430_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh430_mappa"](xs, 50.0)
        r = m["rec"]
        w = r["worst"]
        assert abs(r["max_dd"] - MAXDD) < 1e-12
        assert abs(r["mean"] - MEAN) < 1e-12
        assert abs(r["pain"] - PAIN) < 1e-12
        assert abs(r["rebound"] - REBOUND) < 1e-12
        assert r["n_ep"] == NEP
        assert r["n_chiusi"] == NCHIUSI
        assert r["n_aperti"] == NAPERTI
        assert w["peak_per"] == PEAKPER
        assert w["trough_per"] == TROUGH
        # demo: picco periodo 30, minimo periodo 36, 1 episodio
        # APERTO, rimbalzo 79.0580%, verdetto ESTREMO
        assert w["peak_idx"] == 29
        assert w["trough_idx"] == 35
        assert w["peak_per"] == 30
        assert w["trough_per"] == 36
        assert w["durata"] == 6
        assert w["chiuso"] is False
        assert w["rec_periods"] is None
        assert r["n_ep"] == 1
        assert r["n_chiusi"] == 0
        assert r["n_aperti"] == 1
        assert r["rec_medio"] is None
        assert r["rec_max"] is None
        assert abs(r["rebound"] - 79.0580) < 1e-3
        assert abs(w["rebound"] - 79.0580) < 1e-3
        assert abs(r["mean"] - 1.3417) < 1e-3
        assert abs(r["max_dd"] - 44.1522) < 1e-3
        assert abs(r["pain"] - 4.6950) < 1e-3
        assert m["soglia"] == 50.0
        assert m["verdetto"].startswith("ESTREMO")
        assert abs(w["peak_eq"] - 276.6130) < 1e-3
        assert abs(w["trough_eq"] - 154.4824) < 1e-3
        # identita' del rimbalzo sulla demo
        assert abs((1.0 - r["max_dd"] / 100.0)
                   * (1.0 + r["rebound"] / 100.0) - 1.0) < 1e-9
        assert abs(w["trough_eq"] * (1.0 + w["rebound"] / 100.0)
                   - w["peak_eq"]) < 1e-9

    def test_definizione_a_mano(self):
        # equity composta -> running max (peak iniziale 100) ->
        # drawdown punto per punto -> episodi massimali dd > 0 ->
        # picco (primo massimo) / minimo / rimbalzo per episodio
        xs = list(self._xs())
        eq = 100.0
        peak = 100.0
        dds = []
        eqs = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            eqs.append(eq)
            peak = max(peak, eq)
            dds.append((peak - eq) / peak * 100.0)
        n = len(xs)
        max_dd = max(dds)
        # episodi a mano
        mano = []
        i = 0
        while i < n:
            if dds[i] > 0.0:
                s = i
                pk_eq = 100.0
                pk_idx = -1
                for k in range(s):
                    if eqs[k] > pk_eq:
                        pk_eq = eqs[k]
                        pk_idx = k
                while i < n and dds[i] > 0.0:
                    i += 1
                e = i - 1
                seg = eqs[s:e + 1]
                tr_off = seg.index(min(seg))
                tr = s + tr_off
                tr_eq = seg[tr_off]
                dd = (pk_eq - tr_eq) / pk_eq * 100.0
                chiuso = e + 1 < n
                mano.append({"peak_idx": pk_idx,
                             "peak_per": pk_idx + 1,
                             "trough_idx": tr, "trough_per": tr + 1,
                             "start": s, "end": e,
                             "durata": e - s + 1,
                             "peak_eq": pk_eq, "trough_eq": tr_eq,
                             "max_dd": dd,
                             "rebound": dd / (100.0 - dd) * 100.0,
                             "chiuso": chiuso,
                             "rec_periods": (e + 1 - tr)
                             if chiuso else None})
            else:
                i += 1
        r = _F["mh430_recovery"](tuple(xs))
        assert abs(r["max_dd"] - max_dd) < 1e-12
        assert abs(r["pain"] - sum(dds) / n) < 1e-12
        assert abs(r["mean"] - sum(xs) / n) < 1e-12
        dd = _F["mh430_drawdowns"](tuple(xs))
        assert len(dd) == n
        for x, y in zip(dd, dds):
            assert abs(x - y) < 1e-9
        eqs2 = _F["mh430_equity"](tuple(xs))
        assert abs(eqs2[-1] - eq) < 1e-9
        eps = r["episodi"]
        assert len(eps) == len(mano) == 1
        for x, y in zip(eps, mano):
            for kk in ("peak_idx", "peak_per", "trough_idx",
                       "trough_per", "start", "end", "durata",
                       "chiuso", "rec_periods"):
                assert x[kk] == y[kk], kk
            for kk in ("peak_eq", "trough_eq", "max_dd", "rebound"):
                assert abs(x[kk] - y[kk]) < 1e-9, kk
            # CHIAVE 1: identita' del rimbalzo per episodio
            assert abs((1.0 - x["max_dd"] / 100.0)
                       * (1.0 + x["rebound"] / 100.0) - 1.0) < 1e-9
            assert abs(x["trough_eq"] * (1.0 + x["rebound"] / 100.0)
                       - x["peak_eq"]) < 1e-9
        # somma durate episodi == periodi sott'acqua
        uw = sum(1 for d in dds if d > 0.0)
        assert sum(e["durata"] for e in eps) == uw == 6
        # worst == episodio con max_dd massimo
        w = _F["mh430_worst"](tuple(xs))
        assert w["peak_idx"] == mano[0]["peak_idx"]
        assert w["trough_idx"] == mano[0]["trough_idx"]
        assert abs(w["max_dd"] - max_dd) < 1e-12
        assert abs(w["rebound"] - r["rebound"]) < 1e-12
        assert w["chiuso"] == mano[0]["chiuso"]
        assert w["rec_periods"] == mano[0]["rec_periods"]

    def test_chiave_stesso_rimbalzo_recupero_diverso(self):
        # CHIAVE TEORICA 2: STESSO maxDD (20%) e STESSO rimbalzo
        # (25%), recupero opposto: 1 periodo, 5 periodi, MAI.
        fast = tuple([0.0] * 19 + [-20.0, 25.0])
        slow = tuple([0.0] * 17 + [-20.0] + [5.0] * 5)
        opn = tuple([0.0] * 19 + [-20.0])
        r_f = _F["mh430_recovery"](fast)
        r_s = _F["mh430_recovery"](slow)
        r_o = _F["mh430_recovery"](opn)
        for xs_, r_ in ((fast, r_f), (slow, r_s), (opn, r_o)):
            assert abs(r_["max_dd"] - 20.0) < 1e-12
            assert abs(r_["rebound"] - 25.0) < 1e-12
            assert r_["n_ep"] == 1
            # stesso rimbalzo -> stesso verdetto (MODERATO, r = 0.5)
            assert _F["mh430_mappa"](xs_, 50.0)["verdetto"].startswith("MODERATO")
        assert r_f["worst"]["chiuso"] is True
        assert r_f["worst"]["rec_periods"] == FASTREC == 1
        assert r_s["worst"]["chiuso"] is True
        assert r_s["worst"]["rec_periods"] == SLOWREC == 5
        assert r_o["worst"]["chiuso"] is False
        assert r_o["worst"]["rec_periods"] is None
        assert r_o["n_aperti"] == 1
        # due episodi: rec_medio / rec_max sui chiusi
        two = tuple([0.0] * 19 + [-10.0, 12.0] + [0.0] * 5
                    + [-30.0, 10.0, 10.0, 10.0, 10.0])
        r_t = _F["mh430_recovery"](two)
        assert r_t["n_ep"] == 2
        assert r_t["n_chiusi"] == 2
        assert r_t["n_aperti"] == 0
        assert abs(r_t["rec_medio"] - 2.5) < 1e-12
        assert r_t["rec_max"] == 4
        e1, e2 = r_t["episodi"]
        assert e1["peak_per"] == 0
        assert e1["trough_per"] == 20
        assert abs(e1["max_dd"] - 10.0) < 1e-12
        assert abs(e1["rebound"] - 11.1111) < 1e-3
        assert e1["rec_periods"] == 1
        assert e2["peak_per"] == 21
        assert e2["trough_per"] == 27
        assert abs(e2["max_dd"] - 30.0) < 1e-12
        assert abs(e2["rebound"] - 42.8571) < 1e-3
        assert e2["rec_periods"] == 4
        assert r_t["worst"]["trough_per"] == 27
        assert abs(r_t["worst"]["rebound"] - 42.8571) < 1e-3

    def test_chiave_convessita(self):
        # CHIAVE TEORICA 3: il rimbalzo e' CONVESSO nel drawdown.
        F = _F
        assert abs(F["mh430_rebound"](0.0) - 0.0) < 1e-12
        assert abs(F["mh430_rebound"](10.0) - REB10) < 1e-12
        assert abs(F["mh430_rebound"](20.0) - REB20) < 1e-12
        assert abs(F["mh430_rebound"](50.0) - REB50) < 1e-12
        assert abs(F["mh430_rebound"](80.0) - REB80) < 1e-12
        assert abs(F["mh430_rebound"](90.0) - REB90) < 1e-12
        assert abs(F["mh430_rebound"](10.0) - 11.1111) < 1e-3
        assert abs(F["mh430_rebound"](20.0) - 25.0) < 1e-12
        assert abs(F["mh430_rebound"](50.0) - 100.0) < 1e-12
        assert abs(F["mh430_rebound"](80.0) - 400.0) < 1e-12
        assert abs(F["mh430_rebound"](90.0) - 900.0) < 1e-12
        # R(80)/R(20) = 16x a fronte di un rapporto drawdown 4x
        assert abs(F["mh430_rebound"](80.0)
                   / F["mh430_rebound"](20.0) - 16.0) < 1e-12
        # monotonia stretta
        assert F["mh430_rebound"](30.0) < F["mh430_rebound"](60.0)
        assert F["mh430_rebound"](60.0) < F["mh430_rebound"](90.0)
        # identita' per ogni d
        for d in (5.0, 33.3333, 66.6667, 99.0):
            rb = F["mh430_rebound"](d)
            assert abs((1.0 - d / 100.0) * (1.0 + rb / 100.0)
                       - 1.0) < 1e-9

    def test_crosscheck_gemelli(self):
        # tab429 attribuzione: stessi maxDD/mean/pain e stesso
        # picco/minimo dell'episodio peggiore; tab428 durate:
        # stessi episodi / periodi sott'acqua / aperto;
        # tab427 path/CDaR e tab424 Pain: stessi numeri
        # (stessa convenzione peak iniziale = 100).
        xs = self._xs()
        r = _F["mh430_mappa"](xs, 50.0)["rec"]
        att = _F["mh429_attribution"](xs)
        assert abs(att["max_dd"] - r["max_dd"]) < 1e-12
        assert abs(att["mean"] - r["mean"]) < 1e-12
        assert abs(att["pain"] - r["pain"]) < 1e-12
        assert att["peak_per"] == r["worst"]["peak_per"]
        assert att["trough_per"] == r["worst"]["trough_per"]
        dur = _F["mh428_durations"](xs)
        assert dur["n_episodi"] == r["n_ep"]
        assert dur["underwater"] == r["worst"]["durata"]
        assert dur["aperto"] == (not r["worst"]["chiuso"])
        assert abs(dur["max_dd"] - r["max_dd"]) < 1e-12
        assert abs(dur["pain"] - r["pain"]) < 1e-12
        eps428 = _F["mh428_episodes"](xs)
        assert len(eps428) == r["n_ep"]
        assert eps428[0]["durata"] == r["worst"]["durata"]
        p427 = _F["mh427_path"](xs)
        assert abs(p427["mean"] - r["mean"]) < 1e-12
        assert abs(p427["max_dd"] - r["max_dd"]) < 1e-12
        assert abs(p427["pain"] - r["pain"]) < 1e-12
        c427 = _F["mh427_cdar"](xs, 10.0)
        assert abs(c427["max_dd"] - r["max_dd"]) < 1e-12
        pain424 = _F["mh424_pain"](xs)
        assert abs(pain424["pain"] - r["pain"]) < 1e-12
        assert abs(pain424["max_dd"] - r["max_dd"]) < 1e-12

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh430_verdetto"](0.0, 50.0).startswith("ROBUSTO")
        assert F["mh430_verdetto"](24.9, 50.0).startswith("FACILE")
        assert F["mh430_verdetto"](25.0, 50.0).startswith("MODERATO")
        assert F["mh430_verdetto"](49.9, 50.0).startswith("MODERATO")
        assert F["mh430_verdetto"](50.0, 50.0).startswith("DURO")
        assert F["mh430_verdetto"](74.9, 50.0).startswith("DURO")
        assert F["mh430_verdetto"](75.0, 50.0).startswith("ESTREMO")
        assert F["mh430_verdetto"](99.9, 50.0).startswith("ESTREMO")
        assert F["mh430_verdetto"](100.0, 50.0).startswith("CRITICO")
        assert F["mh430_verdetto"](120.0, 50.0).startswith("CRITICO")
        assert F["mh430_verdetto"](900.0, 50.0).startswith("CRITICO")
        for _bad in (lambda: F["mh430_verdetto"](-1.0, 50.0),
                     lambda: F["mh430_verdetto"](float("nan"), 50.0),
                     lambda: F["mh430_verdetto"](float("inf"), 50.0),
                     lambda: F["mh430_verdetto"](10.0, 0.0),
                     lambda: F["mh430_verdetto"](10.0, 101.0),
                     lambda: F["mh430_verdetto"](10.0, True),
                     lambda: F["mh430_verdetto"]("x", 50.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_casi_degeneri(self):
        F = _F
        # serie piatta: maxDD 0, rimbalzo 0, 0 episodi, ROBUSTO
        r = F["mh430_recovery"](tuple([0.0] * 25))
        assert r["max_dd"] == 0.0 and r["rebound"] == 0.0
        assert r["n_ep"] == 0 and r["episodi"] == ()
        assert r["worst"]["peak_idx"] == -1
        assert r["worst"]["trough_idx"] == -1
        assert r["rec_medio"] is None and r["rec_max"] is None
        m = F["mh430_mappa"](tuple([0.0] * 25), 50.0)
        assert m["verdetto"].startswith("ROBUSTO")
        # solo guadagni: maxDD 0
        g = F["mh430_recovery"](tuple([1.0] * 25))
        assert g["max_dd"] == 0.0 and g["rebound"] == 0.0
        assert g["n_ep"] == 0
        # rendimento <= -100%: equity azzerata, rimbalzo indefinito
        for _bad in (lambda: F["mh430_recovery"](
                         tuple([0.0] * 19 + [-100.0])),
                     lambda: F["mh430_recovery"](
                         tuple([0.0] * 19 + [-150.0])),
                     lambda: F["mh430_episodes"](
                         tuple([0.0] * 19 + [-100.0])),
                     lambda: F["mh430_worst"](
                         tuple([0.0] * 19 + [-100.0])),
                     lambda: F["mh430_rebound"](100.0),
                     lambda: F["mh430_rebound"](150.0),
                     lambda: F["mh430_rebound"](-1.0),
                     lambda: F["mh430_verdetto"](-0.5, 50.0),
                     lambda: F["mh430_verdetto"](10.0, 0.0),
                     lambda: F["mh430_verdetto"](10.0, 101.0),
                     lambda: F["mh430_mappa"](self._xs(), 0.0),
                     lambda: F["mh430_mappa"](self._xs(), 101.0),
                     lambda: F["mh430_mappa"]((1.0,) * 19, 50.0),
                     lambda: F["mh430_mappa"](None, 50.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_validatori(self):
        for _bad in (lambda: _F["mh430_recovery"](None),
                     lambda: _F["mh430_recovery"]((1.0,) * 19),
                     lambda: _F["mh430_recovery"](self._xs()[:5]),
                     lambda: _F["mh430_worst"]((1.0,) * 19),
                     lambda: _F["mh430_worst"](None),
                     lambda: _F["mh430_episodes"]((1.0,) * 19),
                     lambda: _F["mh430_episodes"](None),
                     lambda: _F["mh430_drawdowns"]((1.0,) * 19),
                     lambda: _F["mh430_equity"]((1.0,) * 19),
                     lambda: _F["mh430_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh430_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh430_parse_serie"](None),
                     lambda: _F["mh430_num"](True, "x"),
                     lambda: _F["mh430_num"](float("nan"), "x"),
                     lambda: _F["mh430_num"](float("inf"), "x"),
                     lambda: _F["mh430_num"]("x", "x"),
                     lambda: _F["mh430_mappa"]((1.0,) * 19, 50.0),
                     lambda: _F["mh430_mappa"](None, 50.0)):
            with pytest.raises(ValueError):
                _bad()

