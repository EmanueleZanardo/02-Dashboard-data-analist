"""Test tab475 '💰 Costo di esecuzione: quanto costa davvero ruotare': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh475_num", "mh475_esecuzione", "mh475_frazione_ottima",
           "mh475_verdetto")

TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
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

# Segnali demo deterministici: deltas tab473 (B -0.3575x, C +0.3188x,
# D +0.0387x), nozionale 2M EUR/segnale, ADV 50/40/60M, spread 5/8/3
# bps, sigma_g 2%/3%/1.5%; c_impact 1.0, fisso 50 EUR; fuori budget
# 67'836.58 EUR da tab473 -> ESEGUI, f* = 100%
SEGNALI = (("B", -0.3575345544342753, 2000000.0, 50000000.0, 5.0, 0.02),
           ("C", 0.31883187762650433, 2000000.0, 40000000.0, 8.0, 0.03),
           ("D", 0.03870268680777089, 2000000.0, 60000000.0, 3.0, 0.015))
C_IMPACT = 1.0
FISSO = 50.0
FUORI = 67836.57681259612

TRB = 715069.1088685506
TRC = 637663.7552530087
TRD = 77405.37361554179
SPB = 178.76727721713766
SPC = 255.06550210120346
SPD = 11.610806042331268
IMB = 1710.2792188152227
IMC = 2415.34324799556
IMD = 41.703480377612024
CTOT = 4762.769532549068
CSPT = 445.4435853606724
CIMT = 4167.325947188395
CFST = 150.0
FSTAR = 1.0
CMIN = 4762.769532549068
CEXF = 4762.769532549068
VERD = 'ESEGUI — costo modellato 4,763 EUR <= 67,837 EUR fuori budget: conviene ruotare tutto'
FSTAR2 = 0.42
CMIN2 = 4081.395378369429
VERD2 = 'RUOTA PARZIALE 42% — costo pieno 4,763 EUR > 4,500 EUR fuori budget, ma ruotando il 42% il totale (esecuzione + residuo) scende a 4,081 EUR'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh475_esecuzione"](SEGNALI, c_impact=C_IMPACT,
                                       costo_fisso=FISSO)
    return _DEMO


class TestRegistry475:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 706
        assert "tab475" in dvars
        assert "tab475" in withs

    def test_titoli_allineati_463_464_465_466_467_468_469_470_471_472_473_474_475(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {463: TITLE463, 464: TITLE464, 465: TITLE465,
                  466: TITLE466, 467: TITLE467, 468: TITLE468,
                  469: TITLE469, 470: TITLE470, 471: TITLE471,
                  472: TITLE472, 473: TITLE473, 474: TITLE474,
                  475: TITLE475}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestEsecuzione475:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        assert [r["nome"] for r in m["righe"]] == ["B", "C", "D"]
        assert m["c_impact"] == C_IMPACT
        assert m["costo_fisso"] == FISSO
        rB, rC, rD = m["righe"]
        assert rB["trade_eur"] == TRB
        assert rC["trade_eur"] == TRC
        assert rD["trade_eur"] == TRD
        assert rB["costo_spread"] == SPB
        assert rC["costo_spread"] == SPC
        assert rD["costo_spread"] == SPD
        assert rB["costo_impact"] == IMB
        assert rC["costo_impact"] == IMC
        assert rD["costo_impact"] == IMD
        assert rB["costo_fisso"] == rC["costo_fisso"] == \
            rD["costo_fisso"] == FISSO
        assert m["costo_spread_tot"] == CSPT
        assert m["costo_impact_tot"] == CIMT
        assert m["costo_fisso_tot"] == CFST
        assert m["costo_tot"] == CTOT
        assert m["rotazione_nozionale_tot"] == pytest.approx(
            TRB + TRC + TRD)

    def test_spread_a_mano(self):
        # costo_spread = trade * spread_bps / 2 / 10000 (niente helper)
        m = _demo()
        for r, (nm, dl, nz, av, sp, sg) in zip(m["righe"], SEGNALI):
            trade = abs(dl) * nz
            assert r["costo_spread"] == pytest.approx(
                trade * sp / 2.0 / 10000.0)

    def test_impact_a_mano(self):
        # legge sqrt: c * sigma_g * trade * sqrt(trade/adv)
        m = _demo()
        for r, (nm, dl, nz, av, sp, sg) in zip(m["righe"], SEGNALI):
            trade = abs(dl) * nz
            assert r["costo_impact"] == pytest.approx(
                C_IMPACT * sg * trade * math.sqrt(trade / av))

    def test_legge_sqrt_scaling(self):
        # trade raddoppiato -> impact x 2^1.5 (non x2: e' la firma
        # della legge sqrt, non di un costo lineare)
        m1 = _F["mh475_esecuzione"](
            [("B", -0.3575345544342753, 2000000.0, 50000000.0, 5.0,
              0.02)], c_impact=1.0, costo_fisso=0.0)
        m2 = _F["mh475_esecuzione"](
            [("B", -0.7150691088685506, 2000000.0, 50000000.0, 5.0,
              0.02)], c_impact=1.0, costo_fisso=0.0)
        i1 = m1["righe"][0]["costo_impact"]
        i2 = m2["righe"][0]["costo_impact"]
        assert i2 == pytest.approx(i1 * 2.0 * math.sqrt(2.0))
        # lo spread invece scala lineare
        s1 = m1["righe"][0]["costo_spread"]
        s2 = m2["righe"][0]["costo_spread"]
        assert s2 == pytest.approx(2.0 * s1)

    def test_delta_zero_nessun_costo(self):
        # delta 0 -> trade 0 -> nessun costo, e il fisso NON scatta
        m = _F["mh475_esecuzione"](
            [("X", 0.0, 1000000.0, 10000000.0, 5.0, 0.02)],
            c_impact=1.0, costo_fisso=50.0)
        r = m["righe"][0]
        assert r["trade_eur"] == 0.0
        assert r["costo_tot"] == 0.0
        assert m["costo_tot"] == 0.0

    def test_frazione_ottima_demo(self):
        m = _demo()
        fo = _F["mh475_frazione_ottima"](m, FUORI)
        assert fo["f_star"] == FSTAR == 1.0
        assert fo["costo_exec_fstar"] == CEXF == CTOT
        assert fo["costo_tot_min"] == CMIN == CTOT
        assert fo["n_grid"] == 101
        f0, c0, t0 = fo["dettaglio"][0]
        assert f0 == 0.0 and c0 == 0.0
        assert t0 == pytest.approx(FUORI)  # f=0: solo drift residuo
        f1, c1, t1 = fo["dettaglio"][-1]
        assert f1 == 1.0 and c1 == CTOT and t1 == CTOT
        assert len(fo["dettaglio"]) == 101

    def test_verdetto_esegui(self):
        m = _demo()
        fo = _F["mh475_frazione_ottima"](m, FUORI)
        v = _F["mh475_verdetto"](m, FUORI, fo)
        assert v == VERD
        assert v.startswith("ESEGUI")

    def test_ruota_parziale(self):
        # F=4500 < costo pieno 4763 ma il parziale batte il drift
        m = _demo()
        fo = _F["mh475_frazione_ottima"](m, 4500.0)
        assert fo["f_star"] == FSTAR2 == 0.42
        assert fo["costo_tot_min"] == CMIN2
        assert fo["costo_tot_min"] < 4500.0
        v = _F["mh475_verdetto"](m, 4500.0, fo)
        assert v == VERD2
        assert v.startswith("RUOTA PARZIALE")

    def test_rimanda(self):
        # F=3000: nemmeno il parziale batte il drift (f*=0)
        m = _demo()
        fo = _F["mh475_frazione_ottima"](m, 3000.0)
        assert fo["f_star"] == 0.0
        v = _F["mh475_verdetto"](m, 3000.0, fo)
        assert v.startswith("RIMANDA")

    def test_nessuna_azione(self):
        m = _demo()
        v = _F["mh475_verdetto"](m, 0.0, None)
        assert v.startswith("NESSUNA AZIONE")

    def test_degeneri(self):
        ex = _F["mh475_esecuzione"]
        fo = _F["mh475_frazione_ottima"]
        vd = _F["mh475_verdetto"]
        m = _demo()
        for bad in (lambda: ex([], 1.0, 0.0),
                    lambda: ex("no", 1.0, 0.0),
                    lambda: ex([("X", 0.1, 1e6, 1e6, 5.0, 0.02)], -1.0,
                               0.0),
                    lambda: ex([("X", 0.1, 1e6, 1e6, 5.0, 0.02)], 1.0,
                               -5.0),
                    lambda: ex([("X", 0.1, 0.0, 1e6, 5.0, 0.02)], 1.0,
                               0.0),
                    lambda: ex([("X", 0.1, 1e6, 0.0, 5.0, 0.02)], 1.0,
                               0.0),
                    lambda: ex([("X", 0.1, 1e6, 1e6, -1.0, 0.02)], 1.0,
                               0.0),
                    lambda: ex([("X", 0.1, 1e6, 1e6, 5.0, -0.01)], 1.0,
                               0.0),
                    lambda: ex([("", 0.1, 1e6, 1e6, 5.0, 0.02)], 1.0,
                               0.0),
                    lambda: ex([("X", 0.1, 1e6, 1e6, 5.0)], 1.0, 0.0),
                    lambda: ex([("X", float("nan"), 1e6, 1e6, 5.0,
                                 0.02)], 1.0, 0.0),
                    lambda: fo(m, -1.0),
                    lambda: fo({"righe": []}, 100.0),
                    lambda: fo(m, 100.0, n_grid=1),
                    lambda: vd({"righe": []}, 100.0, None),
                    lambda: vd(m, -1.0, None),
                    lambda: vd({"righe": [{"nome": "X"}],
                                "costo_tot": -5.0}, 100.0, None),
                    lambda: vd(m, 100.0, "no")):
            try:
                bad()
                raise SystemExit("caso degenere non solleva!")
            except ValueError:
                pass

    def test_verdetti_degeneri_a_mano(self):
        vd = _F["mh475_verdetto"]
        v = vd({"righe": [{"nome": "B", "costo_tot": 100.0}],
                "costo_tot": 100.0}, 0.0, None)
        assert v.startswith("NESSUNA AZIONE")
        v = vd({"righe": [{"nome": "B", "costo_tot": 100.0}],
                "costo_tot": 100.0}, 100.0, None)
        assert v.startswith("ESEGUI")  # costo == F: conviene

    def test_determinismo(self):
        a = _F["mh475_esecuzione"](SEGNALI, c_impact=C_IMPACT,
                                   costo_fisso=FISSO)
        b = _F["mh475_esecuzione"](SEGNALI, c_impact=C_IMPACT,
                                   costo_fisso=FISSO)
        assert a["costo_tot"] == b["costo_tot"]
        fa = _F["mh475_frazione_ottima"](a, FUORI)
        fb = _F["mh475_frazione_ottima"](b, FUORI)
        assert fa["f_star"] == fb["f_star"]
        assert fa["costo_tot_min"] == fb["costo_tot_min"]

    def test_num_degenere(self):
        num = _F["mh475_num"]
        assert num(3.5, "x") == 3.5
        assert num(3, "x") == 3.0
        # stringhe rifiutate: come mh473_num, solo numeri reali
        for bad in ("3.5", "no", None, float("nan"), float("inf"),
                    float("-inf"), True, [1]):
            try:
                num(bad, "x")
                raise SystemExit("num non solleva!")
            except ValueError:
                pass
