
"""Test tab429 '🎯 Attribuzione del drawdown: chi ha causato il peggior calo': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh429_num", "mh429_parse_serie", "mh429_equity",
           "mh429_drawdowns", "mh429_worst", "mh429_attribution",
           "mh429_verdetto", "mh429_mappa",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain")

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
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
NATTR = 6
TOP1 = 25.890581986169998
TOP1PER = 33
TOP3 = 61.49426456756829
HHI = 0.18075338549526007
SOMMA = 99.99999999999997
NCAUS = 6
NMIT = 0
PEAKPER = 30
TROUGH = 36
SINGLEMAXDD = 20.0
SINGLENATTR = 1
SINGLETOP1 = 100.0
SINGLEHHI = 1.0
SINGLENCAUS = 1
DIFFMAXDD = 20.00000000000003
DIFFNATTR = 20
DIFFTOP1 = 4.999999999999993
DIFFTOP3 = 14.999999999999979
DIFFHHI = 0.05000000000000001
DIFFNCAUS = 20
MITMAXDD = 24.39999999999999
MITNATTR = 3
MITTOP1 = 79.77563827840325
MITTOP3 = 117.44288134432263
MITHHI = 0.5642767618653605
MITNCAUS = 2
MITNMIT = 1
MITNEG = -17.442881344322604


class TestRegistry429:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 597
        assert "tab429" in dvars
        assert "tab429" in withs

    def test_titoli_allineati_423_424_425_426_427_428_429(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426
        assert titoli[dvars.index("tab427")] == TITLE427
        assert titoli[dvars.index("tab428")] == TITLE428
        assert titoli[dvars.index("tab429")] == TITLE429

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


class TestAttribuzione429:
    def _xs(self):
        return _F["mh429_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh429_mappa"](xs, 50.0)
        a = m["attr"]
        assert abs(a["max_dd"] - MAXDD) < 1e-12
        assert abs(a["mean"] - MEAN) < 1e-12
        assert abs(a["pain"] - PAIN) < 1e-12
        assert a["n_attr"] == NATTR
        assert abs(a["top1"] - TOP1) < 1e-12
        assert a["top1_per"] == TOP1PER
        assert abs(a["top3"] - TOP3) < 1e-12
        assert abs(a["hhi"] - HHI) < 1e-12
        assert abs(a["somma"] - SOMMA) < 1e-12
        assert a["n_caus"] == NCAUS
        assert a["n_mit"] == NMIT
        assert a["peak_per"] == PEAKPER
        assert a["trough_per"] == TROUGH
        # demo: picco periodo 30, minimo periodo 36, 6 periodi,
        # top1 = periodo 33 (-14.0%) con quota 25.8906%,
        # top3 61.4943%, HHI 0.1808, verdetto EQUILIBRATA
        assert a["peak_idx"] == 29
        assert a["trough_idx"] == 35
        assert a["peak_per"] == 30
        assert a["trough_per"] == 36
        assert a["n_attr"] == 6
        assert abs(a["top1"] - 25.8906) < 1e-3
        assert a["top1_idx"] == 32
        assert a["top1_per"] == 33
        assert abs(a["top3"] - 61.4943) < 1e-3
        assert abs(a["hhi"] - 0.1808) < 1e-3
        assert abs(a["somma"] - 100.0) < 1e-9
        assert a["n_caus"] == 6
        assert a["n_mit"] == 0
        assert abs(a["mean"] - 1.3417) < 1e-3
        assert abs(a["max_dd"] - 44.1522) < 1e-3
        assert abs(a["pain"] - 4.6950) < 1e-3
        assert m["soglia"] == 50.0
        assert m["verdetto"].startswith("EQUILIBRATA")
        # contributi: 6 righe, periodo 31..36, quote note
        ct = a["contributi"]
        assert len(ct) == 6
        assert [c["per"] for c in ct] == [31, 32, 33, 34, 35, 36]
        assert abs(ct[0]["quota"] - 17.1354) < 1e-3
        assert abs(ct[1]["quota"] - 12.8272) < 1e-3
        assert abs(ct[2]["quota"] - 25.8906) < 1e-3
        assert abs(ct[5]["quota"] - 18.4683) < 1e-3
        assert abs(ct[-1]["dd_dopo"] - 44.1522) < 1e-3
        assert abs(ct[-1]["quota_cum"] - 100.0) < 1e-9

    def test_definizione_a_mano(self):
        # equity composta -> running max (peak iniziale 100) ->
        # drawdown punto per punto -> picco/minimo -> quote log
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
        trough = dds.index(max_dd)
        peak_idx = -1
        peak_eq = 100.0
        for i in range(trough + 1):
            if eqs[i] > peak_eq:
                peak_eq = eqs[i]
                peak_idx = i
        seg = xs[peak_idx + 1: trough + 1]
        tot = math.log(1.0 - max_dd / 100.0)
        # quote a mano (solo rendimenti != 0)
        mano = []
        eq2 = peak_eq
        cum = 0.0
        for k, r in enumerate(seg):
            if r == 0.0:
                continue
            q = math.log(1.0 + r / 100.0) / tot * 100.0
            cum += q
            eq2 *= 1.0 + r / 100.0
            mano.append({"idx": peak_idx + 1 + k,
                         "per": peak_idx + 2 + k, "r": r, "quota": q,
                         "quota_cum": cum,
                         "dd_dopo": (peak_eq - eq2) / peak_eq * 100.0})
        a = _F["mh429_attribution"](tuple(xs))
        assert abs(a["max_dd"] - max_dd) < 1e-12
        assert a["peak_idx"] == peak_idx
        assert a["trough_idx"] == trough
        assert a["n_attr"] == len(mano)
        ct = a["contributi"]
        assert len(ct) == len(mano)
        for x, y in zip(ct, mano):
            assert x["idx"] == y["idx"]
            assert x["per"] == y["per"]
            assert abs(x["r"] - y["r"]) < 1e-12
            assert abs(x["quota"] - y["quota"]) < 1e-9
            assert abs(x["quota_cum"] - y["quota_cum"]) < 1e-9
            assert abs(x["dd_dopo"] - y["dd_dopo"]) < 1e-9
        # CHIAVE 1: somma quote = 100% esatto
        assert abs(sum(c["quota"] for c in ct) - 100.0) < 1e-9
        assert abs(a["somma"] - 100.0) < 1e-9
        assert abs(ct[-1]["quota_cum"] - 100.0) < 1e-9
        assert abs(ct[-1]["dd_dopo"] - max_dd) < 1e-9
        # top1/top3/HHI dalle quote
        pos = sorted((c["quota"] for c in ct if c["quota"] > 0.0),
                     reverse=True)
        assert abs(a["top1"] - max(c["quota"] for c in ct)) < 1e-12
        assert abs(a["top3"] - sum(pos[:3])) < 1e-12
        s = sum(pos)
        assert abs(a["hhi"] - sum((q / s) ** 2 for q in pos)) < 1e-12
        assert a["n_caus"] == sum(1 for c in ct if c["quota"] > 0.0)
        assert a["n_mit"] == sum(1 for c in ct if c["quota"] < 0.0)
        assert abs(a["pain"] - sum(dds) / n) < 1e-12
        assert abs(a["mean"] - sum(xs) / n) < 1e-12
        dd = _F["mh429_drawdowns"](tuple(xs))
        assert len(dd) == n
        for x, y in zip(dd, dds):
            assert abs(x - y) < 1e-9
        eqs2 = _F["mh429_equity"](tuple(xs))
        assert abs(eqs2[-1] - eq) < 1e-9
        w = _F["mh429_worst"](tuple(xs))
        assert w["peak_idx"] == peak_idx
        assert w["trough_idx"] == trough
        assert abs(w["max_dd"] - max_dd) < 1e-12
        assert abs(w["peak_eq"] - peak_eq) < 1e-9

    def test_chiave_stesso_maxdd_attribuzione_opposta(self):
        # CHIAVE TEORICA 2: STESSO maxDD (20%), attribuzione opposta.
        # Singolo: 1 periodo, top1 100%, HHI 1.0, MONO-EVENTO.
        # Diffuso: 20 periodi, top1 5%, HHI 0.05, DIFFUSA.
        sing = tuple([0.0] * 19 + [-20.0])
        x_diff = 100.0 * (0.8 ** (1.0 / 20.0) - 1.0)
        diff = tuple([x_diff] * 20)
        a_s = _F["mh429_attribution"](sing)
        a_d = _F["mh429_attribution"](diff)
        assert abs(a_s["max_dd"] - SINGLEMAXDD) < 1e-12
        assert a_s["n_attr"] == SINGLENATTR
        assert abs(a_s["top1"] - SINGLETOP1) < 1e-12
        assert abs(a_s["hhi"] - SINGLEHHI) < 1e-12
        assert a_s["n_caus"] == SINGLENCAUS
        assert abs(a_d["max_dd"] - DIFFMAXDD) < 1e-12
        assert a_d["n_attr"] == DIFFNATTR
        assert abs(a_d["top1"] - DIFFTOP1) < 1e-12
        assert abs(a_d["top3"] - DIFFTOP3) < 1e-12
        assert abs(a_d["hhi"] - DIFFHHI) < 1e-12
        assert a_d["n_caus"] == DIFFNCAUS
        assert abs(a_s["max_dd"] - 20.0) < 1e-12
        assert abs(a_d["max_dd"] - 20.0) < 1e-12
        # uguaglianza solo entro tolleranza: la serie diffusa
        # accumula errore float (0.8^(1/20) applicato 20 volte =
        # 20.00000000000003, non 20.0 esatto)
        assert abs(a_s["max_dd"] - a_d["max_dd"]) < 1e-9
        assert a_s["n_attr"] == 1
        assert a_d["n_attr"] == 20
        assert abs(a_s["top1"] - 100.0) < 1e-12
        assert abs(a_d["top1"] - 5.0) < 1e-12
        assert abs(a_s["hhi"] - 1.0) < 1e-12
        assert abs(a_d["hhi"] - 0.05) < 1e-12
        assert abs(a_s["somma"] - 100.0) < 1e-9
        assert abs(a_d["somma"] - 100.0) < 1e-9
        m_s = _F["mh429_mappa"](sing, 50.0)
        m_d = _F["mh429_mappa"](diff, 50.0)
        assert m_s["verdetto"].startswith("MONO-EVENTO")
        assert m_d["verdetto"].startswith("DIFFUSA")

    def test_chiave_mitiganti(self):
        # CHIAVE TEORICA 3: il +5% dentro l'episodio peggiore e'
        # un mitigante (quota negativa): top3 > 100%.
        mit = tuple([0.0] * 17 + [-20.0, 5.0, -10.0])
        a = _F["mh429_attribution"](mit)
        assert abs(a["max_dd"] - MITMAXDD) < 1e-12
        assert a["n_attr"] == MITNATTR
        assert abs(a["top1"] - MITTOP1) < 1e-12
        assert abs(a["top3"] - MITTOP3) < 1e-12
        assert abs(a["hhi"] - MITHHI) < 1e-12
        assert a["n_caus"] == MITNCAUS
        assert a["n_mit"] == MITNMIT
        assert abs(a["max_dd"] - 24.4000) < 1e-3
        assert a["n_attr"] == 3
        assert abs(a["top1"] - 79.7756) < 1e-3
        assert abs(a["top3"] - 117.4429) < 1e-3
        assert a["top3"] > 100.0
        assert abs(a["hhi"] - 0.5643) < 1e-3
        assert a["n_caus"] == 2
        assert a["n_mit"] == 1
        assert abs(a["somma"] - 100.0) < 1e-9
        ct = a["contributi"]
        assert len(ct) == 3
        assert [c["per"] for c in ct] == [18, 19, 20]
        assert abs(ct[1]["quota"] - MITNEG) < 1e-12
        assert abs(ct[1]["quota"] - (-17.4429)) < 1e-3
        assert ct[1]["r"] == 5.0
        m = _F["mh429_mappa"](mit, 50.0)
        assert m["verdetto"].startswith("MOLTO CONCENTRATA")
        # solo perdite: tutti causativi, top1 = 100/n, HHI = 1/n
        lo = _F["mh429_attribution"](tuple([-2.0] * 25))
        assert lo["n_attr"] == 25
        assert abs(lo["top1"] - 4.0) < 1e-12
        assert abs(lo["hhi"] - 0.04) < 1e-12
        assert lo["n_caus"] == 25
        assert lo["n_mit"] == 0
        assert abs(lo["somma"] - 100.0) < 1e-9

    def test_crosscheck_gemelli(self):
        # tab427 path/CDaR e tab424 Pain sulla demo: stessi numeri
        # (stessa convenzione peak iniziale = 100).
        xs = self._xs()
        a = _F["mh429_mappa"](xs, 50.0)["attr"]
        p427 = _F["mh427_path"](xs)
        assert abs(p427["mean"] - a["mean"]) < 1e-12
        assert abs(p427["max_dd"] - a["max_dd"]) < 1e-12
        assert abs(p427["pain"] - a["pain"]) < 1e-12
        c427 = _F["mh427_cdar"](xs, 10.0)
        assert abs(c427["max_dd"] - a["max_dd"]) < 1e-12
        pain424 = _F["mh424_pain"](xs)
        assert abs(pain424["pain"] - a["pain"]) < 1e-12
        assert abs(pain424["max_dd"] - a["max_dd"]) < 1e-12

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh429_verdetto"](0.0, 50.0).startswith("ROBUSTO")
        assert F["mh429_verdetto"](24.9, 50.0).startswith("DIFFUSA")
        assert F["mh429_verdetto"](25.0, 50.0).startswith("EQUILIBRATA")
        assert F["mh429_verdetto"](49.9, 50.0).startswith("EQUILIBRATA")
        assert F["mh429_verdetto"](50.0, 50.0).startswith("CONCENTRATA")
        assert F["mh429_verdetto"](74.9, 50.0).startswith("CONCENTRATA")
        assert F["mh429_verdetto"](75.0, 50.0).startswith("MOLTO CONCENTRATA")
        assert F["mh429_verdetto"](89.9, 50.0).startswith("MOLTO CONCENTRATA")
        assert F["mh429_verdetto"](90.0, 50.0).startswith("DOMINATA")
        assert F["mh429_verdetto"](99.9, 50.0).startswith("DOMINATA")
        assert F["mh429_verdetto"](100.0, 50.0).startswith("MONO-EVENTO")
        assert F["mh429_verdetto"](120.0, 50.0).startswith("MONO-EVENTO")
        for _bad in (lambda: F["mh429_verdetto"](-1.0, 50.0),
                     lambda: F["mh429_verdetto"](float("nan"), 50.0),
                     lambda: F["mh429_verdetto"](10.0, 0.0),
                     lambda: F["mh429_verdetto"](10.0, 101.0),
                     lambda: F["mh429_verdetto"](10.0, True),
                     lambda: F["mh429_verdetto"]("x", 50.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_casi_degeneri(self):
        F = _F
        # serie piatta: maxDD 0, nessun contributo, ROBUSTO
        a = F["mh429_attribution"](tuple([0.0] * 25))
        assert a["max_dd"] == 0.0 and a["n_attr"] == 0
        assert a["top1"] == 0.0 and a["somma"] == 0.0
        assert a["contributi"] == () and a["top1_idx"] is None
        assert a["top1_per"] is None
        m = F["mh429_mappa"](tuple([0.0] * 25), 50.0)
        assert m["verdetto"].startswith("ROBUSTO")
        # solo guadagni: maxDD 0
        g = F["mh429_attribution"](tuple([1.0] * 25))
        assert g["max_dd"] == 0.0 and g["n_attr"] == 0
        # rendimento <= -100%: log indefinito
        for _bad in (lambda: F["mh429_attribution"](
                         tuple([0.0] * 19 + [-100.0])),
                     lambda: F["mh429_attribution"](
                         tuple([0.0] * 19 + [-150.0])),
                     lambda: F["mh429_verdetto"](-0.5, 50.0),
                     lambda: F["mh429_verdetto"](10.0, 0.0),
                     lambda: F["mh429_verdetto"](10.0, 101.0),
                     lambda: F["mh429_mappa"](self._xs(), 0.0),
                     lambda: F["mh429_mappa"](self._xs(), 101.0),
                     lambda: F["mh429_mappa"]((1.0,) * 19, 50.0),
                     lambda: F["mh429_mappa"](None, 50.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_validatori(self):
        for _bad in (lambda: _F["mh429_attribution"](None),
                     lambda: _F["mh429_attribution"]((1.0,) * 19),
                     lambda: _F["mh429_attribution"](self._xs()[:5]),
                     lambda: _F["mh429_worst"]((1.0,) * 19),
                     lambda: _F["mh429_worst"](None),
                     lambda: _F["mh429_drawdowns"]((1.0,) * 19),
                     lambda: _F["mh429_equity"]((1.0,) * 19),
                     lambda: _F["mh429_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh429_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh429_parse_serie"](None),
                     lambda: _F["mh429_num"](True, "x"),
                     lambda: _F["mh429_num"](float("nan"), "x"),
                     lambda: _F["mh429_num"](float("inf"), "x"),
                     lambda: _F["mh429_num"]("x", "x"),
                     lambda: _F["mh429_mappa"]((1.0,) * 19, 50.0),
                     lambda: _F["mh429_mappa"](None, 50.0)):
            with pytest.raises(ValueError):
                _bad()

