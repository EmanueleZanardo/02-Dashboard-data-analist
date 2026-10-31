"""Test tab438 '🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh438_num", "mh438_parse_serie", "mh438_equity",
           "mh438_drawdowns", "mh438_max_dd", "mh438_ann_return",
           "mh438_pain", "mh438_pain_ratio", "mh438_verdetto",
           "mh438_mappa",
           "mh437_num", "mh437_parse_serie", "mh437_equity",
           "mh437_drawdowns", "mh437_max_dd",
           "mh437_ann_return", "mh437_yearly_max_dds",
           "mh437_avg_max_dd", "mh437_sterling",
           "mh437_verdetto", "mh437_mappa",
           "mh436_num", "mh436_parse_serie", "mh436_equity",
           "mh436_drawdowns", "mh436_max_dd", "mh436_ulcer",
           "mh436_ann_return", "mh436_martin", "mh436_verdetto",
           "mh436_mappa",
           "mh435_num", "mh435_parse_serie", "mh435_equity",
           "mh435_drawdowns", "mh435_max_dd", "mh435_ann_return",
           "mh435_lpm", "mh435_kappa", "mh435_verdetto",
           "mh435_mappa",
           "mh434_num", "mh434_parse_serie", "mh434_equity",
           "mh434_drawdowns", "mh434_max_dd", "mh434_ann_return",
           "mh434_burke", "mh434_verdetto", "mh434_mappa",
           "mh433_num", "mh433_parse_serie", "mh433_equity",
           "mh433_drawdowns", "mh433_max_dd",
           "mh433_upside_potential", "mh433_downside_potential",
           "mh433_omega", "mh433_verdetto", "mh433_mappa",
           "mh432_num", "mh432_parse_serie", "mh432_equity",
           "mh432_drawdowns", "mh432_max_dd", "mh432_ann_return",
           "mh432_downside_dev", "mh432_sortino", "mh432_verdetto",
           "mh432_mappa",
           "mh431_num", "mh431_equity", "mh431_drawdowns",
           "mh431_max_dd", "mh431_ann_return", "mh431_calmar",
           "mh431_verdetto", "mh431_mappa",
           "mh430_num", "mh430_equity", "mh430_drawdowns",
           "mh430_rebound", "mh430_episodes", "mh430_recovery",
           "mh430_worst", "mh430_verdetto", "mh430_mappa",
           "mh429_num", "mh429_equity", "mh429_drawdowns",
           "mh429_worst", "mh429_attribution",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain",
           "mh421_num", "mh421_equity", "mh421_drawdowns",
           "mh421_ulcer", "mh421_martin")

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
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
TITLE429 = "🎯 Attribuzione del drawdown: chi ha causato il peggior calo"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
ANN = 17.342816782940005
PAINRATIO = 3.6939097218027177
PAINRATIO_PPY1 = 0.28576647066316285
PAINRATIO_PPY52 = 21.294284694774188
PAINRATIO_A = 16.0540825025149
PAINRATIO_B = 0.9443577942655823
PAIN_A = 1.0
PAIN_B = 17.0
ANN_AB = 16.0540825025149
MAXDD_AB = 20.0
MEAN_AB = 1.5
CALMAR_AB = 0.802704125125745
STERLING = 1.1783893189997336
MARTIN = 1.385902649301104
KAPPA = 1.389386420473165
BURKE = 0.23098377488351735
OMEGA = 1.8734177215189876
SORTINO = 1.2829179004131461
CALMAR = 0.3927964396665778


class TestRegistry438:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 834
        assert "tab438" in dvars
        assert "tab438" in withs

    def test_titoli_allineati_429_430_431_432_433_434_435_436_437_438(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab429")] == TITLE429
        assert titoli[dvars.index("tab430")] == TITLE430
        assert titoli[dvars.index("tab431")] == TITLE431
        assert titoli[dvars.index("tab432")] == TITLE432
        assert titoli[dvars.index("tab433")] == TITLE433
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438

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


class TestPainRatio438:
    def _xs(self):
        return _F["mh438_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh438_mappa"](xs, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["pain_ratio"] - PAINRATIO) < 1e-9
        assert m["verdetto"].startswith("OTTIMO")
        # demo: ann 17.3428%, Pain 4.6950%, Pain ratio 3.6939 OTTIMO
        assert m["ppy"] == 12.0
        assert m["n_dd"] == 6
        # Pain <= maxDD, e <= media dei maxDD annui (Sterling)
        assert m["pain"] <= m["max_dd"]
        s437 = _F["mh437_mappa"](xs, 12.0)
        assert m["pain"] <= s437["avg_max_dd"]
        assert m["pain_ratio"] >= s437["sterling"]

    def test_identita_pain_ratio(self):
        xs = self._xs()
        m = _F["mh438_mappa"](xs, 12.0)
        assert abs(m["pain_ratio"] - m["ann"] / m["pain"]) < 1e-12
        assert abs(m["ann"] - ((1.0 + m["mean"] / 100.0) ** 12.0 - 1.0) * 100.0) < 1e-9
        # Pain a mano: media dei drawdown punto per punto
        dds = _F["mh438_drawdowns"](xs)
        assert abs(sum(dds) / len(dds) - m["pain"]) < 1e-12
        assert abs(_F["mh438_pain"](xs) - m["pain"]) < 1e-12
        # Pain <= Ulcer (media <= media quadratica, Jensen)
        ulcer = math.sqrt(sum(d * d for d in dds) / len(dds))
        assert m["pain"] <= ulcer + 1e-12
        # gerarchia per ann >= 0: Pain ratio >= Martin, Sterling, Calmar
        ma436 = _F["mh436_mappa"](xs, 12.0)
        assert abs(ma436["martin"] - MARTIN) < 1e-9
        assert m["pain_ratio"] >= ma436["martin"]
        s437 = _F["mh437_mappa"](xs, 12.0)
        assert abs(s437["sterling"] - STERLING) < 1e-9
        assert m["pain_ratio"] >= s437["sterling"]
        c431 = _F["mh431_mappa"](xs, 12.0)
        assert abs(c431["calmar"] - CALMAR) < 1e-9
        assert m["pain_ratio"] >= c431["calmar"]

    def test_crosscheck_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh438_mappa"](xs, 12.0)
        s437 = _F["mh437_mappa"](xs, 12.0)
        assert abs(s437["sterling"] - STERLING) < 1e-9
        assert abs(s437["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(s437["mean"] - m["mean"]) < 1e-12
        assert abs(s437["pain"] - m["pain"]) < 1e-12
        ma436 = _F["mh436_mappa"](xs, 12.0)
        assert abs(ma436["martin"] - MARTIN) < 1e-9
        assert abs(ma436["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(ma436["mean"] - m["mean"]) < 1e-12
        assert abs(ma436["pain"] - m["pain"]) < 1e-12
        k435 = _F["mh435_mappa"](xs, 12.0)
        assert abs(k435["kappa"] - KAPPA) < 1e-9
        assert abs(k435["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(k435["mean"] - m["mean"]) < 1e-12
        assert abs(k435["pain"] - m["pain"]) < 1e-12
        b434 = _F["mh434_mappa"](xs, 12.0)
        assert abs(b434["burke"] - BURKE) < 1e-9
        assert abs(b434["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(b434["mean"] - m["mean"]) < 1e-12
        o433 = _F["mh433_mappa"](xs, 0.0)
        assert abs(o433["omega"] - OMEGA) < 1e-9
        assert abs(o433["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(o433["mean"] - m["mean"]) < 1e-12
        assert abs(o433["pain"] - m["pain"]) < 1e-12
        s432 = _F["mh432_mappa"](xs, 0.0, 12.0)
        assert abs(s432["sortino"] - SORTINO) < 1e-9
        assert abs(s432["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(s432["mean"] - m["mean"]) < 1e-12
        c431 = _F["mh431_mappa"](xs, 12.0)
        assert abs(c431["calmar"] - CALMAR) < 1e-9
        assert abs(c431["max_dd"] - m["max_dd"]) < 1e-12
        # confronto famiglia: Pain ratio OTTIMO, Sterling BUONO,
        # Martin BUONO, Kappa-3 BUONO, Sortino BUONO, Omega BUONO,
        # Burke DISCRETO, Calmar DEBOLE
        assert m["verdetto"].startswith("OTTIMO")
        assert _F["mh437_verdetto"](STERLING).startswith("BUONO")
        assert _F["mh436_verdetto"](MARTIN).startswith("BUONO")
        assert _F["mh435_verdetto"](KAPPA).startswith("BUONO")
        assert _F["mh434_verdetto"](BURKE).startswith("DISCRETO")
        assert _F["mh433_verdetto"](OMEGA).startswith("BUONO")
        assert _F["mh432_verdetto"](SORTINO).startswith("BUONO")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        rec = _F["mh430_recovery"](xs)
        assert abs(rec["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(rec["mean"] - m["mean"]) < 1e-12
        assert abs(rec["pain"] - m["pain"]) < 1e-12
        att = _F["mh429_attribution"](xs)
        assert abs(att["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(att["mean"] - m["mean"]) < 1e-12
        p427 = _F["mh427_path"](xs)
        assert abs(p427["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(p427["mean"] - m["mean"]) < 1e-12
        p424 = _F["mh424_pain"](xs)
        assert abs(p424["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(p424["pain"] - m["pain"]) < 1e-12
        u421 = _F["mh421_ulcer"](xs)
        assert abs(u421["max_dd"] - m["max_dd"]) < 1e-12

    def test_stesso_maxdd_media_painratio_diverso(self):
        a = tuple([25.0, -20.0, 25.0] + [0.0] * 17)
        b = tuple([25.0, -20.0] + [0.0] * 16 + [25.0, 0.0])
        ma = _F["mh438_mappa"](a, 10.0)
        mb = _F["mh438_mappa"](b, 10.0)
        assert abs(ma["max_dd"] - MAXDD_AB) < 1e-12
        assert abs(mb["max_dd"] - MAXDD_AB) < 1e-12
        assert abs(ma["mean"] - MEAN_AB) < 1e-12
        assert abs(mb["mean"] - MEAN_AB) < 1e-12
        assert abs(ma["ann"] - ANN_AB) < 1e-9
        assert abs(mb["ann"] - ANN_AB) < 1e-9
        assert abs(ma["pain"] - PAIN_A) < 1e-12
        assert abs(mb["pain"] - PAIN_B) < 1e-12
        assert abs(ma["pain_ratio"] - PAINRATIO_A) < 1e-12
        assert abs(mb["pain_ratio"] - PAINRATIO_B) < 1e-12
        assert abs(ma["pain_ratio"] / mb["pain_ratio"] - 17.0) < 1e-9
        assert _F["mh438_verdetto"](PAINRATIO_A).startswith("ECCEZIONALE")
        assert _F["mh438_verdetto"](PAINRATIO_B).startswith("DISCRETO")
        # il Calmar vede le due serie IDENTICHE, il Pain ratio no
        ca = _F["mh431_mappa"](a, 10.0)
        cb = _F["mh431_mappa"](b, 10.0)
        assert abs(ca["calmar"] - cb["calmar"]) < 1e-12
        assert abs(ca["calmar"] - CALMAR_AB) < 1e-9

    def test_sensibilita_annualizzazione(self):
        xs = self._xs()
        s1 = _F["mh438_pain_ratio"](xs, 1.0)
        s12 = _F["mh438_pain_ratio"](xs, 12.0)
        s52 = _F["mh438_pain_ratio"](xs, 52.0)
        assert abs(s1 - PAINRATIO_PPY1) < 1e-9
        assert abs(s12 - PAINRATIO) < 1e-9
        assert abs(s52 - PAINRATIO_PPY52) < 1e-9
        assert s1 < s12 < s52
        assert _F["mh438_verdetto"](s1).startswith("DEBOLE")
        assert _F["mh438_verdetto"](s52).startswith("ECCEZIONALE")
        # il Pain NON dipende da ppy: cambia solo l'annualizzazione
        assert abs(_F["mh438_mappa"](xs, 1.0)["pain"] - PAIN) < 1e-12
        assert abs(_F["mh438_mappa"](xs, 52.0)["pain"] - PAIN) < 1e-12
        # ppy non intero AMMESSO (nessun blocco annuo, a differenza
        # dello Sterling): pain ratio = ann(12.5) / Pain
        s125 = _F["mh438_pain_ratio"](xs, 12.5)
        assert abs(s125 - _F["mh438_ann_return"](xs, 12.5) / PAIN) < 1e-9

    def test_verdetto_soglie(self):
        assert _F["mh438_verdetto"](-0.1).startswith("NEGATIVO")
        assert _F["mh438_verdetto"](0.0).startswith("DEBOLE")
        assert _F["mh438_verdetto"](0.499).startswith("DEBOLE")
        assert _F["mh438_verdetto"](0.5).startswith("DISCRETO")
        assert _F["mh438_verdetto"](0.999).startswith("DISCRETO")
        assert _F["mh438_verdetto"](1.0).startswith("BUONO")
        assert _F["mh438_verdetto"](1.999).startswith("BUONO")
        assert _F["mh438_verdetto"](2.0).startswith("OTTIMO")
        assert _F["mh438_verdetto"](3.999).startswith("OTTIMO")
        assert _F["mh438_verdetto"](4.0).startswith("ECCEZIONALE")
        assert _F["mh438_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh438_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh438_mappa"](flat, 12.0)
        assert mf["pain"] == 0.0
        assert mf["ann"] == 0.0
        assert mf["pain_ratio"] == 0.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh438_mappa"](gains, 12.0)
        assert mg["pain"] == 0.0
        assert mg["ann"] > 0.0
        assert mg["pain_ratio"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        for bad in (lambda: _F["mh438_mappa"]((1.0,) * 19, 12.0),
                    lambda: _F["mh438_mappa"](None, 12.0),
                    lambda: _F["mh438_mappa"](tuple([0.0] * 19 + [-100.0]), 12.0),
                    lambda: _F["mh438_pain_ratio"](self._xs(), 0.0),
                    lambda: _F["mh438_pain_ratio"](self._xs(), -12.0),
                    lambda: _F["mh438_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh438_verdetto"](float("nan"))):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh438_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh438_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh438_parse_serie"]("1\n2\n")

