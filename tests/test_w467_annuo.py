"""Test tab467 '📅 L'edge annualizzato: il trade si ripete?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh467_num", "mh467_phi", "mh467_annuo", "mh467_verdetto",
           "mh467_mappa")

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
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"

# Segnali demo deterministici: (nome, lam, mu, sigma)
SEGNALI = (("B", 12.0, 17000.0, 8000.0),
           ("C", 8.0, 27000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0))

MEDIA_B = 204000.0
STD_B = 65084.56038109192
PNEG_B = 0.0008610768551002845
NT_B = 1
VERD_B = 'SOLIDO — P(anno in rosso) = 0.1%'
MEDIA_C = 216000.0
STD_C = 83570.32966310471
PNEG_C = 0.004873903550586978
NT_C = 1
VERD_C = 'SOLIDO — P(anno in rosso) = 0.5%'
MEDIA_D = 5000.0
STD_D = 22388.613177238112
PNEG_D = 0.41164019139350316
NT_D = 1083
VERD_D = 'MARGINALE — P(anno in rosso) = 41%'
MEDIA_TOT = 425000.0
STD_TOT = 108264.72186266402
PNEG_TOT = 4.326353692346574e-05
VERD_PTF = 'SOLIDO — P(anno in rosso) = 0.0%'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh467_mappa"](SEGNALI)
    return _DEMO


class TestRegistry467:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 667
        assert "tab467" in dvars
        assert "tab467" in withs

    def test_titoli_allineati_455_456_457_458_459_460_461_462_463_464_465_466_467(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {455: TITLE455, 456: TITLE456, 457: TITLE457,
                  458: TITLE458, 459: TITLE459, 460: TITLE460,
                  461: TITLE461, 462: TITLE462, 463: TITLE463,
                  464: TITLE464, 465: TITLE465, 466: TITLE466,
                  467: TITLE467}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestAnnuo467:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D"]
        rB, rC, rD = m["righe"]
        assert rB["annuo"]["media_annua"] == pytest.approx(MEDIA_B)
        assert rB["annuo"]["std_annua"] == pytest.approx(STD_B, rel=1e-9)
        assert rB["annuo"]["p_neg"] == pytest.approx(PNEG_B, rel=1e-9)
        assert rB["annuo"]["n_target"] == NT_B
        assert rC["annuo"]["media_annua"] == pytest.approx(MEDIA_C)
        assert rC["annuo"]["std_annua"] == pytest.approx(STD_C, rel=1e-9)
        assert rC["annuo"]["p_neg"] == pytest.approx(PNEG_C, rel=1e-9)
        assert rC["annuo"]["n_target"] == NT_C
        assert rD["annuo"]["media_annua"] == pytest.approx(MEDIA_D)
        assert rD["annuo"]["std_annua"] == pytest.approx(STD_D, rel=1e-9)
        assert rD["annuo"]["p_neg"] == pytest.approx(PNEG_D, rel=1e-9)
        assert rD["annuo"]["n_target"] == NT_D
        assert rB["verdetto"] == VERD_B
        assert rC["verdetto"] == VERD_C
        assert rD["verdetto"] == VERD_D
        assert m["media_tot"] == pytest.approx(MEDIA_TOT)
        assert m["std_tot"] == pytest.approx(STD_TOT, rel=1e-9)
        assert m["p_neg_tot"] == pytest.approx(PNEG_TOT, rel=1e-9)
        assert m["verdetto"] == VERD_PTF
        # disegno: B e C solidi, D marginale, portafoglio solido
        assert rB["verdetto"].startswith("SOLIDO")
        assert rC["verdetto"].startswith("SOLIDO")
        assert rD["verdetto"].startswith("MARGINALE")
        assert m["verdetto"].startswith("SOLIDO")

    def test_formula_a_mano(self):
        # lam=10, mu=100, sigma=50: media=1000,
        # var=10*(2500+10000)=125000, std=353.5534,
        # p_neg=Phi(-1000/353.5534)=Phi(-2.8284)=0.00234
        a = _F["mh467_annuo"](10.0, 100.0, 50.0)
        assert a["media_annua"] == pytest.approx(1000.0)
        assert a["var_annua"] == pytest.approx(125000.0)
        assert a["std_annua"] == pytest.approx(353.5533905932738,
                                              rel=1e-9)
        assert a["p_neg"] == pytest.approx(0.002338867490523582,
                                           rel=1e-6)

    def test_n_target(self):
        A = _F["mh467_annuo"]
        # mu=10, sigma=50 -> ceil((1.6449*5)^2) = ceil(67.68) = 68
        assert A(10.0, 10.0, 50.0)["n_target"] == 68
        # sigma=0, mu>0 -> basta un segnale
        assert A(5.0, 100.0, 0.0)["n_target"] == 1
        # mu<=0 -> nessun n rende P(rosso)<=5%
        assert A(5.0, -1.0, 50.0)["n_target"] is None
        assert A(5.0, 0.0, 50.0)["n_target"] is None

    def test_verdetti_4_stati(self):
        V = _F["mh467_verdetto"]
        assert V(100.0, 0.001).startswith("SOLIDO")
        assert V(100.0, 0.05).startswith("SOLIDO")
        assert V(100.0, 0.0501).startswith("ACCETTABILE")
        assert V(100.0, 0.24).startswith("ACCETTABILE")
        assert V(100.0, 0.30).startswith("ACCETTABILE")
        assert V(100.0, 0.3001).startswith("MARGINALE")
        assert V(100.0, 0.46).startswith("MARGINALE")
        assert V(-5.0, 0.9) == "SENZA EDGE"
        assert V(0.0, 0.5) == "SENZA EDGE"
        # soglie custom: piu' severe
        assert V(100.0, 0.04, soglia_acc=0.01).startswith("ACCETTABILE")
        assert V(100.0, 0.005, soglia_acc=0.01).startswith("SOLIDO")

    def test_sigma_zero_resta_rischio_arrivi(self):
        # sigma=0 ma lam finito: resta la varianza degli arrivi
        # lam=3, mu=100 -> p_neg = Phi(-sqrt(3)) = 0.04163
        a = _F["mh467_annuo"](3.0, 100.0, 0.0)
        assert a["var_annua"] == pytest.approx(30000.0)
        assert a["p_neg"] == pytest.approx(0.041632258331775196,
                                          rel=1e-9)

    def test_mappa_totali(self):
        m = _demo()
        assert m["media_tot"] == pytest.approx(
            sum(r["annuo"]["media_annua"] for r in m["righe"]))
        assert m["var_tot"] == pytest.approx(
            sum(r["annuo"]["var_annua"] for r in m["righe"]))
        assert m["std_tot"] == pytest.approx(
            math.sqrt(sum(r["annuo"]["var_annua"] for r in m["righe"])))
        # singolo segnale senza edge
        m0 = _F["mh467_mappa"]([("Z", 5.0, -10.0, 100.0)])
        assert m0["righe"][0]["verdetto"] == "SENZA EDGE"
        assert m0["verdetto"] == "SENZA EDGE"

    def test_degeneri(self):
        A, V, M, P = (_F["mh467_annuo"], _F["mh467_verdetto"],
                      _F["mh467_mappa"], _F["mh467_phi"])
        for bad in (lambda: A(0, 100, 10),
                    lambda: A(-2, 100, 10),
                    lambda: A(5, 100, -1),
                    lambda: A("x", 100, 10),
                    lambda: A(True, 100, 10),
                    lambda: A(5, 100, float("nan")),
                    lambda: P(float("inf")),
                    lambda: V(100, -0.1),
                    lambda: V(100, 1.1),
                    lambda: V(100, 0.1, soglia_acc=0.0),
                    lambda: V(100, 0.1, soglia_acc=0.3, soglia_marg=0.2),
                    lambda: V(100, 0.1, soglia_acc=0.5, soglia_marg=1.0),
                    lambda: M([], ),
                    lambda: M("B"),
                    lambda: M([("B", 1, 2)]),
                    lambda: M([(123, 1, 2, 3)]),
                    lambda: M([("", 1, 2, 3)])):
            with pytest.raises(ValueError):
                bad()

    def test_determinismo(self):
        m1 = _F["mh467_mappa"](SEGNALI)
        m2 = _F["mh467_mappa"](SEGNALI)
        assert m1 == m2
