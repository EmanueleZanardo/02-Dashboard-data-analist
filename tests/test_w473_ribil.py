"""Test tab473 '🔁 Ribilanciare: i nuovi pesi post-shock': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh473_num", "mh473_ribilancia", "mh473_verdetto",
           "mh472_num", "mh472_drift", "mh472_verdetto",
           "mh471_num", "mh471_risk_budget",
           "mh470_num", "mh470_shortfall",
           "mh468_num", "mh468_phi_inv")

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

# Segnali demo deterministici: (nome, lam, mu, sigma) con i pesi
# convergenti tab471; shock vol B +40%, C -20%, D fermo; tol 30%:
# B va ridotto (vol salita, +107.2% sopra budget) e C va aumentato
# (vol scesa, -79.6% sotto budget), D tiene quasi fermo
SEGNALI = (("B", 12.0, 2000.0, 8000.0),
           ("C", 8.0, 3000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0))
PESI = (1.08667581, 0.83448255, 1.07884163)
SHOCK = (1.4, 0.8, 1.0)
TOL = 0.30

W1B = 0.7291412555657247
W1C = 1.1533144276265044
W1D = 1.117544316807771
DB = -0.3575345544342753
DC = 0.31883187762650433
DD = 0.03870268680777089
ROT = 0.7150691188685505
ES_ATT = 79048.22063083155
ES_DRIFT = 94903.74461955775
ES_RIBIL = 82980.43542825337
FUORI = 67836.57681259612
NFLAG = 2
COSTO = 1000.0
MAXROT = 'B'
ITER = 23
DEVFIN = 6.675920006508962e-10
VERD = 'RIBILANCIA — B: 1.09x -> 0.73x (-0.36x); C: 0.83x -> 1.15x (+0.32x); tiene: D: 1.08x -> 1.12x (+0.04x). Rotazione totale 0.72x. Costo stimato 1,000 EUR contro 67,837 EUR fuori budget: conviene ribilanciare.'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh473_ribilancia"](SEGNALI, PESI, shock_vol=SHOCK,
                                       tol=TOL)
    return _DEMO


class TestRegistry473:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 529
        assert "tab473" in dvars
        assert "tab473" in withs

    def test_titoli_allineati_461_462_463_464_465_466_467_468_469_470_471_472_473(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {461: TITLE461, 462: TITLE462, 463: TITLE463,
                  464: TITLE464, 465: TITLE465, 466: TITLE466,
                  467: TITLE467, 468: TITLE468, 469: TITLE469,
                  470: TITLE470, 471: TITLE471, 472: TITLE472,
                  473: TITLE473}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestRibilancia473:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        assert m["nomi"] == ["B", "C", "D"]
        assert m["pesi_attuali"] == pytest.approx(list(PESI))
        assert m["pesi_nuovi"] == pytest.approx([W1B, W1C, W1D])
        assert m["shock_vol"] == pytest.approx(list(SHOCK))
        assert m["budget"] == pytest.approx([1.0 / 3.0] * 3)
        assert len(m["segnali_shock"]) == 3
        rB, rC, rD = m["righe"]
        for r, w1, d in ((rB, W1B, DB), (rC, W1C, DC), (rD, W1D, DD)):
            assert r["peso_nuovo"] == w1
            assert r["delta"] == d
            assert r["peso_nuovo"] - r["peso_attuale"] == \
                pytest.approx(d)
        assert m["rotazione_tot"] == ROT
        assert m["max_rotazione"] == MAXROT == "B"
        assert m["delta_max_rotazione"] == DB
        assert m["es_atteso"] == ES_ATT
        assert m["es_drift"] == ES_DRIFT
        assert m["es_ribilanciato"] == ES_RIBIL
        assert m["fuori_budget_eur"] == FUORI
        assert m["n_ribilanciare"] == NFLAG == 2
        assert m["costo_ribil_tot"] == COSTO
        assert m["iterazioni"] == ITER == 23
        assert m["deviazione_finale"] == DEVFIN
        assert m["tol"] == pytest.approx(TOL)

    def test_pesi_riallineano(self):
        # coi nuovi pesi, sul regime driftato, il drift e' zero:
        # nessuna deviazione oltre la tolleranza
        m = _demo()
        dr2 = _F["mh472_drift"](m["segnali_shock"], m["pesi_nuovi"],
                                shock_vol=(1.0, 1.0, 1.0), tol=TOL)
        assert dr2["n_ribilanciare"] == 0
        assert max(abs(r["deviazione"])
                   for r in dr2["righe"]) < 1e-6

    def test_direzione(self):
        # la vol salita chiede pesi piu' bassi e viceversa
        m = _demo()
        rB, rC, rD = m["righe"]
        assert rB["delta"] < 0.0   # B: vol +40% -> peso giu'
        assert rC["delta"] > 0.0   # C: vol -20% -> peso su'
        # D non flaggato: si muove meno dei due flaggati
        assert abs(rD["delta"]) < abs(rB["delta"])
        assert abs(rD["delta"]) < abs(rC["delta"])

    def test_identita_modello(self):
        # i segnali shockati rappresentano ESATTAMENTE il regime
        # driftato: var' = s^2 * var, media invariata (verifica via
        # mh470, indipendente dalla costruzione in mh473)
        m = _demo()
        sf0 = _F["mh470_shortfall"](SEGNALI)
        sf1 = _F["mh470_shortfall"](m["segnali_shock"])
        for r0, r1, s in zip(sf0["righe"], sf1["righe"], SHOCK):
            assert r1["var"] == pytest.approx(s ** 2 * r0["var"])
            assert r1["media"] == pytest.approx(r0["media"])

    def test_componenti_indipendenti(self):
        # comp_i(pesi_nuovi) ricalcolate a mano sui segnali shockati
        # con k via statistics.NormalDist: ognuna ~= budget * ES
        m = _demo()
        nd = statistics.NormalDist()
        z = nd.inv_cdf(0.01)
        k = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi) / 0.01
        w = m["pesi_nuovi"]
        med = []
        var = []
        for (nm, lam, mu, sg) in m["segnali_shock"]:
            med.append(lam * mu)
            var.append(lam * (sg ** 2 + mu ** 2))
        V = sum(w[i] ** 2 * var[i] for i in range(3))
        std = math.sqrt(V)
        es = k * std - sum(w[i] * med[i] for i in range(3))
        assert abs(es - m["es_ribilanciato"]) < 1e-6
        for i in range(3):
            comp = k * w[i] ** 2 * var[i] / std - w[i] * med[i]
            assert abs(comp - es / 3.0) < 1e-6 * es

    def test_rotazione(self):
        m = _demo()
        assert abs(m["rotazione_tot"] - sum(
            abs(r["delta"]) for r in m["righe"])) < 1e-12
        assert m["rotazione_tot"] == pytest.approx(
            abs(DB) + abs(DC) + abs(DD))

    def test_costo(self):
        m = _demo()
        assert m["costo_ribil_tot"] == pytest.approx(
            m["n_ribilanciare"] * 500.0)
        m2 = _F["mh473_ribilancia"](SEGNALI, PESI, shock_vol=SHOCK,
                                    tol=TOL, costo_ribil=250.0)
        assert m2["costo_ribil_tot"] == pytest.approx(2 * 250.0)

    def test_fuori_budget(self):
        m = _demo()
        dr = _F["mh472_drift"](SEGNALI, PESI, shock_vol=SHOCK, tol=TOL)
        assert m["fuori_budget_eur"] == dr["fuori_budget_eur"]
        assert m["es_atteso"] == dr["es_atteso"]
        assert m["es_drift"] == dr["es_corrente"]

    def test_shock_nullo_nessuna_azione(self):
        # senza shock i nuovi pesi coincidono con gli attuali: niente
        # da fare (coerenza col punto fisso tab471)
        m = _F["mh473_ribilancia"](SEGNALI, PESI)
        assert m["n_ribilanciare"] == 0
        assert max(abs(r["delta"]) for r in m["righe"]) < 1e-6
        v = _F["mh473_verdetto"](m)
        assert v.startswith("NESSUNA AZIONE")

    def test_shock_incompatibile(self):
        # drift OK (ES > 0) ma lo shock schiaccia la vol sotto il
        # quadrato della media: costruzione impossibile -> ValueError
        with pytest.raises(ValueError):
            _F["mh473_ribilancia"]([("S", 4.0, 1000.0, 100.0)], [1.0],
                                   shock_vol=(0.9,))

    def test_non_convergenza(self):
        # max_iter=1: il punto fisso non converge -> ValueError onesto,
        # non pesi finti
        with pytest.raises(ValueError):
            _F["mh473_ribilancia"](SEGNALI, PESI, shock_vol=SHOCK,
                                   tol=TOL, max_iter=1)

    def test_verdetto(self):
        v = _F["mh473_verdetto"](_demo())
        assert v == VERD
        assert v.startswith("RIBILANCIA")
        assert "B" in v and "C" in v

    def test_verdetto_degeneri(self):
        V = _F["mh473_verdetto"]
        sv = V({"righe": [{"nome": "B", "peso_attuale": 1.0,
                           "peso_nuovo": 1.0, "delta": 0.0,
                           "flag_drift": False}],
                "n_ribilanciare": 0, "rotazione_tot": 0.0})
        assert sv.startswith("NESSUNA AZIONE")
        for bad in (lambda: V({}),
                    lambda: V({"righe": []}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": -1}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": True}),
                    lambda: V({"righe": [{"nome": "X"}],
                               "n_ribilanciare": 0,
                               "rotazione_tot": -1.0}),
                    lambda: V({"righe": [{"nome": "X", "peso_attuale": 1.0,
                                          "peso_nuovo": 1.0, "delta": 0.0,
                                          "flag_drift": True}],
                               "n_ribilanciare": 1, "rotazione_tot": 0.1,
                               "costo_ribil_tot": 500.0,
                               "fuori_budget_eur": -5.0})):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        D = _F["mh473_ribilancia"]
        V = _F["mh473_verdetto"]
        N = _F["mh473_num"]
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
                   lambda: D(SEGNALI, PESI, max_iter=0),
                   # ES <= 0: drift senza senso
                   lambda: D([("S", 10.0, 100000.0, 100.0)], [1.0]),
                   # shock incompatibile col modello
                   lambda: D([("S", 4.0, 1000.0, 100.0)], [1.0],
                             shock_vol=(0.9,)),
                   # punto fisso non convergente
                   lambda: D(SEGNALI, PESI, shock_vol=SHOCK, max_iter=1),
                   lambda: V({}),
                   lambda: V({"righe": []}),
                   lambda: N(True, "x"),
                   lambda: N(float("inf"), "x"),
                   lambda: N(float("nan"), "x")):
            with pytest.raises(ValueError):
                fn()

    def test_determinismo(self):
        a = _F["mh473_ribilancia"](SEGNALI, PESI, shock_vol=SHOCK,
                                   tol=TOL)
        b = _F["mh473_ribilancia"](SEGNALI, PESI, shock_vol=SHOCK,
                                   tol=TOL)
        assert a["pesi_nuovi"] == b["pesi_nuovi"]
        assert a["rotazione_tot"] == b["rotazione_tot"]
