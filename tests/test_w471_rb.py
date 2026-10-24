"""Test tab471 '🎯 Risk budgeting: ogni segnale si guadagna il suo capitale': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh471_num", "mh471_risk_budget", "mh471_verdetto",
           "mh470_num", "mh470_shortfall",
           "mh468_num", "mh468_phi_inv")

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
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"

# Segnali demo deterministici: (nome, lam, mu, sigma)
# B/C/D: a pesi unitari C mangia il 50.1% piu' del budget (top
# sovrappeso), B e' sotto del 29.4% (top sottopeso)
SEGNALI = (("B", 12.0, 2000.0, 8000.0),
           ("C", 8.0, 3000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0))

PESO_B = 1.0866758147155502
COMP_B = 26349.4070158925
TARGET_B = 26349.40696065243
SCARTO_B = 5.524006701307371e-05
COMP0_B = 19141.8321424214
SC0_B = -0.29414217798284736
PESO_C = 0.8344825510791638
COMP_C = 26349.40691118513
TARGET_C = 26349.40696065243
SCARTO_C = -4.946730041410774e-05
COMP0_C = 40712.748213632105
SC0_C = 0.5012884643743334
PESO_D = 1.0788416342052856
COMP_D = 26349.406954879654
TARGET_D = 26349.40696065243
SCARTO_D = -5.772777512902394e-06
COMP0_D = 21501.03353111364
SC0_D = -0.20714628639148505
ES_INIZ = 81355.61388716713
CAP_INIZ = 81355.61388716713
ES_FIN = 79048.2208819573
CAP_FIN = 79048.2208819573
ITER = 24
DEV = 6.988148043909008e-10
TOP_OVER = 'C'
TOP_UNDER = 'B'
SC_OVER = 0.5012884643743334
SC_UNDER = -0.29414217798284736
VERD = 'BUDGET RISPETTATI — a taglie correnti C mangia il +50.1% del suo budget di ES (troppo): va ridimensionato a 0.83x; B ha ancora spazio (-29.4% sul budget): può salire a 1.09x. Capitale finale 79,048 EUR in 24 iterazioni.'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh471_risk_budget"](SEGNALI)
    return _DEMO


class TestRegistry471:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 685
        assert "tab471" in dvars
        assert "tab471" in withs

    def test_titoli_allineati_459_460_461_462_463_464_465_466_467_468_469_470_471(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {459: TITLE459, 460: TITLE460, 461: TITLE461,
                  462: TITLE462, 463: TITLE463, 464: TITLE464,
                  465: TITLE465, 466: TITLE466, 467: TITLE467,
                  468: TITLE468, 469: TITLE469, 470: TITLE470,
                  471: TITLE471}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestRiskBudget471:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D"]
        rB, rC, rD = m["righe"]
        for r, peso, comp, target, scarto in (
                (rB, PESO_B, COMP_B, TARGET_B, SCARTO_B),
                (rC, PESO_C, COMP_C, TARGET_C, SCARTO_C),
                (rD, PESO_D, COMP_D, TARGET_D, SCARTO_D)):
            assert r["peso"] == peso
            assert r["componente"] == comp
            assert r["target"] == target
            assert r["scarto"] == scarto
            assert r["budget"] == pytest.approx(1.0 / 3.0)
        assert m["componenti_iniziali"] == [COMP0_B, COMP0_C, COMP0_D]
        assert m["scarti_rel_iniziali"] == pytest.approx(
            [SC0_B, SC0_C, SC0_D])
        assert m["es_iniziale"] == ES_INIZ
        assert m["capitale_iniziale"] == CAP_INIZ
        assert m["es_finale"] == ES_FIN
        assert m["capitale_finale"] == CAP_FIN
        assert m["iterazioni"] == ITER
        assert m["deviazione_finale"] == DEV
        assert m["top_sovrappeso"] == TOP_OVER == "C"
        assert m["top_sottopeso"] == TOP_UNDER == "B"
        assert m["scarto_top_sovrappeso"] == SC_OVER
        assert m["scarto_top_sottopeso"] == SC_UNDER
        assert m["convergenza"] is True

    def test_somma_componenti_uguale_es(self):
        m = _demo()
        assert abs(sum(r["componente"] for r in m["righe"])
                   - m["es_finale"]) < 1e-6

    def test_budget_sommano_uno(self):
        m = _demo()
        assert abs(sum(m["budget"]) - 1.0) < 1e-12

    def test_budget_rispettati(self):
        m = _demo()
        dev = max(abs(r["componente"] - r["budget"] * m["es_finale"])
                  for r in m["righe"]) / m["es_finale"]
        assert dev < 1e-6

    def test_pesi(self):
        m = _demo()
        assert abs(sum(m["pesi"]) - 3.0) < 1e-9
        assert all(p > 0.0 for p in m["pesi"])
        # direzione: il sovrappesato (C) si riduce, i sottopeso crescono
        rB, rC, rD = m["righe"]
        assert rC["peso"] < 1.0 < rB["peso"]
        assert rD["peso"] > 1.0

    def test_convergenza_reale(self):
        m = _demo()
        assert m["convergenza"] is True
        assert m["iterazioni"] < 500
        assert m["deviazione_finale"] < 1e-9

    def test_budget_custom(self):
        m = _F["mh471_risk_budget"](SEGNALI, budget=(0.5, 0.3, 0.2))
        assert m["convergenza"] is True
        assert m["budget"] == pytest.approx([0.5, 0.3, 0.2])
        for i, r in enumerate(m["righe"]):
            assert abs(r["componente"] - m["budget"][i] *
                       m["es_finale"]) / m["es_finale"] < 1e-6

    def test_default_equal_e_normalizzazione(self):
        m = _F["mh471_risk_budget"](SEGNALI)
        assert m["budget"] == pytest.approx([1.0 / 3.0] * 3)
        mn = _F["mh471_risk_budget"](SEGNALI, budget=(50, 30, 20))
        mc = _F["mh471_risk_budget"](SEGNALI, budget=(0.5, 0.3, 0.2))
        assert mn["pesi"] == mc["pesi"]

    def test_euler_differenze_finite(self):
        # comp_i = w_i * d(es)/d(w_i) ai pesi convergenti; k indipendente
        # via statistics.NormalDist().pdf (niente helper 471)
        m = _demo()
        nd = statistics.NormalDist()
        k = nd.pdf(nd.inv_cdf(0.01)) / 0.01
        med = [12.0 * 2000.0, 8.0 * 3000.0, 20.0 * 250.0]
        var = [12.0 * (8000.0 ** 2 + 2000.0 ** 2),
               8.0 * (12000.0 ** 2 + 3000.0 ** 2),
               20.0 * (5000.0 ** 2 + 250.0 ** 2)]

        def es_w(w):
            mw = sum(w[i] * med[i] for i in range(3))
            vw = sum(w[i] ** 2 * var[i] for i in range(3))
            return k * math.sqrt(vw) - mw

        w = [r["peso"] for r in m["righe"]]
        eps = 1e-6
        for i, r in enumerate(m["righe"]):
            wp = list(w)
            wm = list(w)
            wp[i] += eps
            wm[i] -= eps
            fd = w[i] * (es_w(wp) - es_w(wm)) / (2 * eps)
            assert abs(r["componente"] - fd) < 1e-3 * max(
                1.0, abs(fd)), r["nome"]

    def test_mult(self):
        m = _F["mh471_risk_budget"](SEGNALI, mult=1.25)
        assert abs(m["capitale_finale"]
                   - m["es_finale"] * 1.25) < 1e-9
        assert m["capitale_finale"] > _demo()["capitale_finale"]

    def test_verdetto(self):
        v = _F["mh471_verdetto"](_demo())
        assert v == VERD
        assert v.startswith("BUDGET RISPETTATI")
        assert "C" in v and "B" in v

    def test_verdetto_nonconverge_e_nessun_capitale(self):
        nv = _F["mh471_verdetto"]({
            "righe": [{"nome": "X"}], "convergenza": False,
            "iterazioni": 7, "deviazione_finale": 0.05,
            "capitale_finale": 100.0})
        assert nv.startswith("BUDGET NON RAGGIUNTI")
        nc = _F["mh471_verdetto"]({
            "righe": [{"nome": "X"}], "convergenza": True,
            "capitale_finale": 0.0})
        assert nc.startswith("NESSUN CAPITALE DA RIPARTIRE")

    def test_degeneri(self):
        RB = _F["mh471_risk_budget"]
        V = _F["mh471_verdetto"]
        N = _F["mh471_num"]
        for fn in (lambda: RB([]),
                   lambda: RB([("B", 12, 2000)]),
                   lambda: RB([(123, 1, 2, 3)]),
                   lambda: RB([("", 1, 2, 3)]),
                   lambda: RB([("B", 0, 2, 3)]),
                   lambda: RB([("B", -1, 2, 3)]),
                   lambda: RB([("B", 1, 2, -3)]),
                   lambda: RB([("B", 1, 2, 3)], budget=(0.5, 0.5)),
                   lambda: RB([("B", 1, 2, 3)], budget=(0.0,)),
                   lambda: RB([("B", 1, 2, 3)], budget=(-1.0,)),
                   lambda: RB([("B", 1, 2, 3)], alpha=0.0),
                   lambda: RB([("B", 1, 2, 3)], alpha=0.5),
                   lambda: RB([("B", 1, 2, 3)], mult=0.9),
                   lambda: RB([("B", 1, 2, 3)], damp=0.0),
                   lambda: RB([("B", 1, 2, 3)], damp=1.5),
                   lambda: RB([("B", 1, 2, 3)], max_iter=0),
                   lambda: RB([("B", 1, 2, 3)], tol=0.0),
                   lambda: RB([("B", 1, 2, "x")]),
                   lambda: RB([("B", 1, 2, float("nan"))]),
                   # componente <= 0: non puo' assorbire budget positivo
                   lambda: RB((("S", 0.5, 10000.0, 100.0),
                               ("C", 8.0, 3000.0, 12000.0))),
                   # ES <= 0 a pesi unitari: budgeting senza senso
                   lambda: RB([("S", 10.0, 100000.0, 100.0)]),
                   lambda: V({}),
                   lambda: V({"righe": []}),
                   lambda: V({"righe": [{"nome": "X"}],
                              "convergenza": True,
                              "capitale_finale": -5.0}),
                   lambda: N(True, "x"),
                   lambda: N(float("inf"), "x")):
            with pytest.raises(ValueError):
                fn()

    def test_determinismo(self):
        a = _F["mh471_risk_budget"](SEGNALI)
        b = _F["mh471_risk_budget"](SEGNALI)
        assert a["pesi"] == b["pesi"]
        assert a["es_finale"] == b["es_finale"]
