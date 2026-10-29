"""Test tab466 '💸 Costi veri: l'edge sopravvive al netto?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh466_num", "mh466_costi", "mh466_verdetto", "mh466_mappa")

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
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE467 = "📅 L'edge annualizzato: il trade si ripete?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"

# Trade demo deterministici: (nome, edge_lordo, qty_mwh, capitale)
TRADES = (("B", 21300.0, 8500.0, 400000.0),
          ("C", 34322.0, 11500.0, 450000.0),
          ("D", 5000.0, 9000.0, 150000.0))
BIDASK = 0.35
COMM = 150.0
FUNDING_BPS = 400.0
GIORNI = 45.0

NET_B = 16052.397260273972
FR_B = 0.7536336741912663
NET_C = 27777.82191780822
FR_C = 0.8093299317582956
NET_D = 810.2739726027394
FR_D = 0.16205479452054788
EDGE_TOT = 60622.0
COSTI_TOT = 15981.506849315068
NET_TOT = 44640.49315068493
FR_TOT = 0.7363744705005597
VERD_B = "REGGE — resta 75% dell'edge"
VERD_C = "REGGE — resta 81% dell'edge"
VERD_D = "MARGINE SOTTILE — resta 16% dell'edge"
VERD_PTF = "REGGE — resta 74% dell'edge"

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh466_mappa"](TRADES, BIDASK, COMM, FUNDING_BPS, GIORNI)
    return _DEMO


class TestRegistry466:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 789
        assert "tab466" in dvars
        assert "tab466" in withs

    def test_titoli_allineati_454_455_456_457_458_459_460_461_462_463_464_465_466(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {454: TITLE454, 455: TITLE455, 456: TITLE456,
                  457: TITLE457, 458: TITLE458, 459: TITLE459,
                  460: TITLE460, 461: TITLE461, 462: TITLE462,
                  463: TITLE463, 464: TITLE464, 465: TITLE465,
                  466: TITLE466}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestCosti466:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_trade"] == 3
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D"]
        rB, rC, rD = m["righe"]
        assert rB["costi"]["netto"] == pytest.approx(NET_B, rel=1e-12)
        assert rB["costi"]["frazione"] == pytest.approx(FR_B, rel=1e-12)
        assert rC["costi"]["netto"] == pytest.approx(NET_C, rel=1e-12)
        assert rC["costi"]["frazione"] == pytest.approx(FR_C, rel=1e-12)
        assert rD["costi"]["netto"] == pytest.approx(NET_D, rel=1e-12)
        assert rD["costi"]["frazione"] == pytest.approx(FR_D, rel=1e-12)
        assert rB["verdetto"] == VERD_B
        assert rC["verdetto"] == VERD_C
        assert rD["verdetto"] == VERD_D
        assert m["edge_lordo_tot"] == pytest.approx(EDGE_TOT, rel=1e-12)
        assert m["costi_tot"] == pytest.approx(COSTI_TOT, rel=1e-12)
        assert m["netto_tot"] == pytest.approx(NET_TOT, rel=1e-12)
        assert m["frazione_tot"] == pytest.approx(FR_TOT, rel=1e-12)
        assert m["verdetto"] == VERD_PTF
        # disegno: B e C tengono bene, D ha margine sottile
        assert rB["verdetto"].startswith("REGGE")
        assert rC["verdetto"].startswith("REGGE")
        assert rD["verdetto"].startswith("MARGINE SOTTILE")
        assert m["verdetto"].startswith("REGGE")

    def test_formula_a_mano(self):
        # edge 1000, qty 100, bidask 0.5, comm 10, funding 100 bps,
        # 73 giorni, capitale 10000:
        # spread 50 + comm 20 + funding 10000*0.01*73/365 = 20
        c = _F["mh466_costi"](1000.0, 100.0, 0.5, 10.0, 100.0, 73.0,
                              10000.0)
        assert c["costo_spread"] == pytest.approx(50.0)
        assert c["costo_comm"] == pytest.approx(20.0)
        assert c["costo_funding"] == pytest.approx(20.0)
        assert c["costi_totali"] == pytest.approx(90.0)
        assert c["netto"] == pytest.approx(910.0)
        assert c["frazione"] == pytest.approx(0.91)
        assert c["costo_per_mwh"] == pytest.approx(0.9)
        assert c["breakeven_per_mwh"] == pytest.approx(0.9)

    def test_breakeven(self):
        # edge esattamente pari ai costi -> netto 0 -> NON REGGE
        c = _F["mh466_costi"](90.0, 100.0, 0.5, 10.0, 100.0, 73.0,
                              10000.0)
        assert abs(c["netto"]) < 1e-9
        assert _F["mh466_verdetto"](
            c["netto"], c["edge_lordo"]) == "NON REGGE"
        # un euro sopra -> netto positivo ma margine sottile
        c2 = _F["mh466_costi"](91.0, 100.0, 0.5, 10.0, 100.0, 73.0,
                               10000.0)
        assert c2["netto"] == pytest.approx(1.0)
        assert _F["mh466_verdetto"](
            c2["netto"], c2["edge_lordo"]).startswith("MARGINE SOTTILE")

    def test_verdetti_4_stati(self):
        V = _F["mh466_verdetto"]
        assert V(0.0, 0.0) == "SENZA EDGE"
        assert V(-10.0, -5.0) == "SENZA EDGE"
        assert V(-1.0, 100.0) == "NON REGGE"
        assert V(0.0, 100.0) == "NON REGGE"
        assert V(30.0, 100.0).startswith("MARGINE SOTTILE")
        assert V(49.9, 100.0).startswith("MARGINE SOTTILE")
        assert V(50.0, 100.0).startswith("REGGE")
        assert V(80.0, 100.0).startswith("REGGE")
        # soglia custom: con 0.3 basta il 30%
        assert V(40.0, 100.0, soglia=0.3).startswith("REGGE")
        assert V(20.0, 100.0, soglia=0.3).startswith("MARGINE SOTTILE")

    def test_funding_pro_rata(self):
        C = _F["mh466_costi"]
        # 0 giorni -> nessun funding
        c0 = C(1000.0, 100.0, 0.0, 0.0, 400.0, 0.0, 100000.0)
        assert c0["costo_funding"] == 0.0
        # 365 giorni -> bps pieni sul capitale
        c1 = C(1000.0, 100.0, 0.0, 0.0, 400.0, 365.0, 100000.0)
        assert c1["costo_funding"] == pytest.approx(4000.0)
        # linearita': 182.5 giorni = meta'
        c2 = C(1000.0, 100.0, 0.0, 0.0, 400.0, 182.5, 100000.0)
        assert c2["costo_funding"] == pytest.approx(2000.0)

    def test_commissione_doppia(self):
        c = _F["mh466_costi"](1000.0, 100.0, 0.0, 100.0, 0.0, 0.0,
                              10000.0)
        assert c["costo_comm"] == pytest.approx(200.0)

    def test_mappa_totali(self):
        m = _demo()
        assert m["edge_lordo_tot"] == pytest.approx(
            sum(r["costi"]["edge_lordo"] for r in m["righe"]))
        assert m["costi_tot"] == pytest.approx(
            sum(r["costi"]["costi_totali"] for r in m["righe"]))
        assert m["netto_tot"] == pytest.approx(
            sum(r["costi"]["netto"] for r in m["righe"]))
        # singolo trade senza edge: frazione None, SENZA EDGE
        m0 = _F["mh466_mappa"]([("Z", 0.0, 100.0, 10000.0)],
                               0.35, 150.0, 400.0, 45.0)
        assert m0["righe"][0]["costi"]["frazione"] is None
        assert m0["righe"][0]["verdetto"] == "SENZA EDGE"
        assert m0["frazione_tot"] is None
        assert m0["verdetto"] == "SENZA EDGE"

    def test_degeneri(self):
        C, V, M = (_F["mh466_costi"], _F["mh466_verdetto"],
                   _F["mh466_mappa"])
        for bad in (lambda: C(1, 0, 0.1, 1, 1, 1, 1),
                    lambda: C(1, -5, 0.1, 1, 1, 1, 1),
                    lambda: C(1, 5, -0.1, 1, 1, 1, 1),
                    lambda: C(1, 5, 0.1, -1, 1, 1, 1),
                    lambda: C(1, 5, 0.1, 1, -1, 1, 1),
                    lambda: C(1, 5, 0.1, 1, 1, -1, 1),
                    lambda: C(1, 5, 0.1, 1, 1, 1, -1),
                    lambda: C("x", 5, 0.1, 1, 1, 1, 1),
                    lambda: C(True, 5, 0.1, 1, 1, 1, 1),
                    lambda: C(1, 5, 0.1, 1, 1, 1, float("nan")),
                    lambda: V(1, 1, soglia=0.0),
                    lambda: V(1, 1, soglia=1.0),
                    lambda: V(1, 1, soglia=-0.5),
                    lambda: M([], 0.1, 1, 1, 1),
                    lambda: M("B", 0.1, 1, 1, 1),
                    lambda: M([("B", 1, 2)], 0.1, 1, 1, 1),
                    lambda: M([(123, 1, 2, 3)], 0.1, 1, 1, 1),
                    lambda: M([("", 1, 2, 3)], 0.1, 1, 1, 1)):
            with pytest.raises(ValueError):
                bad()

    def test_determinismo(self):
        m1 = _F["mh466_mappa"](TRADES, BIDASK, COMM, FUNDING_BPS, GIORNI)
        m2 = _F["mh466_mappa"](TRADES, BIDASK, COMM, FUNDING_BPS, GIORNI)
        assert m1 == m2
