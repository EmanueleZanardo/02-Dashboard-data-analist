"""Test tab472 '🔔 Drift dei budget: quando ribilanciare?': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh472_num", "mh472_drift", "mh472_verdetto",
           "mh470_num", "mh470_shortfall",
           "mh468_num", "mh468_phi_inv")

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

# Segnali demo deterministici: (nome, lam, mu, sigma) con i pesi
# convergenti tab471; shock vol B +40%, C -20%, D fermo; tol 30%:
# B (+107.2%) e C (-79.6%) da ribilanciare, D (-27.6%) tiene
SEGNALI = (("B", 12.0, 2000.0, 8000.0),
           ("C", 8.0, 3000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0))
PESI = (1.08667581, 0.83448255, 1.07884163)
SHOCK = (1.4, 0.8, 1.0)
TOL = 0.30

ES_ATT = 79048.22063083155
ES_CORR = 94903.74461955775
VAR_ES = 0.20058040348275713
COMP_B = 65552.86994615065
TGT_B = 31634.58153985258
DEV_B = 1.0721902031031616
FLAG_B = True
COMP_C = 6439.2538408046275
TGT_C = 31634.58153985258
DEV_C = -0.7964489009379627
FLAG_C = True
COMP_D = 22911.62083260248
TGT_D = 31634.58153985258
DEV_D = -0.27574130216519854
FLAG_D = False
FUORI = 67836.57681259612
NFLAG = 2
COSTO = 1000.0
TOP = 'B'
DEV_TOP = 1.0721902031031616
VERD = "DRIFT — da ribilanciare: B, C (2 su 3); il peggiore e' B (+107.2% sul budget). Costo stimato 1,000 EUR contro 67,837 EUR fuori budget: conviene ribilanciare."

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL)
    return _DEMO


class TestRegistry472:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 550
        assert "tab472" in dvars
        assert "tab472" in withs

    def test_titoli_allineati_460_461_462_463_464_465_466_467_468_469_470_471_472(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {460: TITLE460, 461: TITLE461, 462: TITLE462,
                  463: TITLE463, 464: TITLE464, 465: TITLE465,
                  466: TITLE466, 467: TITLE467, 468: TITLE468,
                  469: TITLE469, 470: TITLE470, 471: TITLE471,
                  472: TITLE472}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestDrift472:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        assert m["nomi"] == ["B", "C", "D"]
        assert m["pesi"] == pytest.approx(list(PESI))
        assert m["shock_vol"] == pytest.approx(list(SHOCK))
        assert m["budget"] == pytest.approx([1.0 / 3.0] * 3)
        rB, rC, rD = m["righe"]
        for r, comp, tgt, dev, flag in (
                (rB, COMP_B, TGT_B, DEV_B, FLAG_B),
                (rC, COMP_C, TGT_C, DEV_C, FLAG_C),
                (rD, COMP_D, TGT_D, DEV_D, FLAG_D)):
            assert r["componente"] == comp
            assert r["target"] == tgt
            assert r["deviazione"] == dev
            assert r["flag"] is flag
        assert m["es_atteso"] == ES_ATT
        assert m["es_corrente"] == ES_CORR
        assert m["variazione_es"] == VAR_ES
        assert m["fuori_budget_eur"] == FUORI
        assert m["n_ribilanciare"] == NFLAG == 2
        assert m["costo_ribil_tot"] == COSTO
        assert m["top_drift"] == TOP == "B"
        assert m["deviazione_top_drift"] == DEV_TOP
        assert m["tol"] == pytest.approx(TOL)

    def test_shock_nullo_budget_stabili(self):
        # coerenza coi pesi convergenti tab471: a shock nulli le
        # deviazioni sono ~0 e nessun segnale va ribilanciato
        m = _F["mh472_drift"](SEGNALI, PESI)
        assert m["n_ribilanciare"] == 0
        assert max(abs(r["deviazione"]) for r in m["righe"]) < 1e-6
        assert abs(m["es_corrente"] - m["es_atteso"]) < 1e-6
        v = _F["mh472_verdetto"](m)
        assert v.startswith("BUDGET STABILI")

    def test_somma_componenti_uguale_es(self):
        m = _demo()
        assert abs(sum(r["componente"] for r in m["righe"])
                   - m["es_corrente"]) < 1e-6

    def test_flag_selettivi(self):
        m = _demo()
        rB, rC, rD = m["righe"]
        assert rB["flag"] is True and rC["flag"] is True
        assert rD["flag"] is False
        assert abs(rB["deviazione"]) > TOL
        assert abs(rC["deviazione"]) > TOL
        assert abs(rD["deviazione"]) < TOL

    def test_componente_indipendente(self):
        # comp_B ricalcolata a mano: k via statistics.NormalDist (niente
        # helper 472/470), media/var dai segnali, shock sulla varianza
        m = _demo()
        nd = statistics.NormalDist()
        z = nd.inv_cdf(0.01)
        k = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi) / 0.01
        med = [12.0 * 2000.0, 8.0 * 3000.0, 20.0 * 250.0]
        var = [12.0 * (8000.0 ** 2 + 2000.0 ** 2),
               8.0 * (12000.0 ** 2 + 3000.0 ** 2),
               20.0 * (5000.0 ** 2 + 250.0 ** 2)]
        w = list(PESI)
        sh = list(SHOCK)
        V = sum(w[i] ** 2 * var[i] * sh[i] ** 2 for i in range(3))
        std = math.sqrt(V)
        es = k * std - sum(w[i] * med[i] for i in range(3))
        comp_b = k * w[0] ** 2 * var[0] * sh[0] ** 2 / std - w[0] * med[0]
        assert abs(es - m["es_corrente"]) < 1e-6
        assert abs(comp_b - m["righe"][0]["componente"]) < 1e-6

    def test_costo_ribilanciamento(self):
        m = _demo()
        assert m["costo_ribil_tot"] == pytest.approx(
            m["n_ribilanciare"] * 500.0)
        m2 = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL,
                               costo_ribil=250.0)
        assert m2["costo_ribil_tot"] == pytest.approx(2 * 250.0)

    def test_fuori_budget(self):
        m = _demo()
        assert abs(m["fuori_budget_eur"] - sum(
            abs(r["componente"] - r["target"]) for r in m["righe"])) < 1e-9

    def test_budget_default_e_normalizzazione(self):
        m = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL)
        assert m["budget"] == pytest.approx([1.0 / 3.0] * 3)
        mn = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL,
                               budget=(50, 30, 20))
        assert mn["budget"] == pytest.approx([0.5, 0.3, 0.2])

    def test_variazione_es(self):
        m = _demo()
        assert abs(m["variazione_es"] - (m["es_corrente"] - m["es_atteso"])
                   / m["es_atteso"]) < 1e-12
        assert m["variazione_es"] > 0.0

    def test_top_drift(self):
        m = _demo()
        assert m["top_drift"] == "B"
        imax = max(range(3),
                   key=lambda i: abs(m["righe"][i]["deviazione"]))
        assert m["righe"][imax]["nome"] == "B"

    def test_verdetto(self):
        v = _F["mh472_verdetto"](_demo())
        assert v == VERD
        assert v.startswith("DRIFT")
        assert "B" in v and "C" in v

    def test_verdetto_stabile_e_degeneri(self):
        V = _F["mh472_verdetto"]
        sv = V({"righe": [{"nome": "B", "deviazione": 0.05,
                           "flag": False}],
                "n_ribilanciare": 0, "fuori_budget_eur": 100.0,
                "es_corrente": 80000.0})
        assert sv.startswith("BUDGET STABILI")
        for bad in (lambda: V({}),
                    lambda: V({"righe": []}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": -1}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": True}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": 0,
                               "fuori_budget_eur": -5.0})):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        D = _F["mh472_drift"]
        V = _F["mh472_verdetto"]
        N = _F["mh472_num"]
        for fn in (lambda: D([], []),
                   lambda: D([("B", 12, 2000)], [1.0]),
                   lambda: D([(123, 1, 2, 3)], [1.0]),
                   lambda: D([("", 1, 2, 3)], [1.0]),
                   lambda: D(SEGNALI, [1.0, 1.0]),
                   lambda: D(SEGNALI, [1.0, -1.0, 1.0]),
                   lambda: D(SEGNALI, [1.0, 0.0, 1.0]),
                   lambda: D(SEGNALI, PESI, budget=(0.5, 0.5)),
                   lambda: D(SEGNALI, PESI, budget=(0.0, 0.5, 0.5)),
                   lambda: D(SEGNALI, PESI, budget=(-1.0, 0.5, 0.5)),
                   lambda: D(SEGNALI, PESI, shock_vol=(1.0, 1.0)),
                   lambda: D(SEGNALI, PESI, shock_vol=(1.0, 0.0, 1.0)),
                   lambda: D(SEGNALI, PESI, shock_vol=(1.0, -2.0, 1.0)),
                   lambda: D(SEGNALI, PESI, shock_vol=("x", 1.0, 1.0)),
                   lambda: D(SEGNALI, PESI, tol=0.0),
                   lambda: D(SEGNALI, PESI, tol=1.5),
                   lambda: D(SEGNALI, PESI, alpha=0.0),
                   lambda: D(SEGNALI, PESI, alpha=0.5),
                   lambda: D(SEGNALI, PESI, mult=0.9),
                   lambda: D(SEGNALI, PESI, costo_ribil=-1.0),
                   # ES <= 0 con questi shock: drift senza senso
                   lambda: D([("S", 10.0, 100000.0, 100.0)], [1.0]),
                   lambda: V({}),
                   lambda: V({"righe": []}),
                   lambda: N(True, "x"),
                   lambda: N(float("inf"), "x"),
                   lambda: N(float("nan"), "x")):
            with pytest.raises(ValueError):
                fn()

    def test_determinismo(self):
        a = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL)
        b = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL)
        assert a["es_corrente"] == b["es_corrente"]
        assert [r["componente"] for r in a["righe"]] == \
               [r["componente"] for r in b["righe"]]
