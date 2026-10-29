"""Test tab468 '📉 VaR annuale: quanto capitale di rischio?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh468_num", "mh468_phi", "mh468_phi_inv", "mh468_rischio",
           "mh468_verdetto", "mh468_mappa")

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
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"

# Segnali demo deterministici: (nome, lam, mu, sigma); budget desk 100k
SEGNALI = (("B", 12.0, 17000.0, 8000.0),
           ("C", 8.0, 27000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0))
CAP_DISP = 100000.0

MEDIA_B = 204000.0
STD_B = 65084.56038109192
VAR_B = -52590.671324564086
CAP_B = 0.0
ES_B = -30535.704147358425
VERD_B = 'NON RICHIESTO — VaR ≤ 0: la coda resta in utile, nessun capitale di rischio necessario'
MEDIA_C = 216000.0
STD_C = 83570.32966310471
VAR_C = -21586.34125534413
CAP_C = 0.0
ES_C = 6732.831017093762
VERD_C = 'NON RICHIESTO — VaR ≤ 0: la coda resta in utile, nessun capitale di rischio necessario'
MEDIA_D = 5000.0
STD_D = 22388.613177238112
VAR_D = 47083.70266759064
CAP_D = 47083.70266759064
ES_D = 54670.45021379656
VERD_D = 'COPERTO — copertura 212%'
MEDIA_TOT = 425000.0
STD_TOT = 108264.72186266402
VAR_TOT = -173138.59446116863
CAP_TOT = 0.0
ES_TOT = -136451.32372984412
VERD_PTF = 'NON RICHIESTO — VaR ≤ 0: la coda resta in utile, nessun capitale di rischio necessario'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh468_mappa"](SEGNALI, CAP_DISP)
    return _DEMO


class TestRegistry468:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 783
        assert "tab468" in dvars
        assert "tab468" in withs

    def test_titoli_allineati_456_457_458_459_460_461_462_463_464_465_466_467_468(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {456: TITLE456, 457: TITLE457, 458: TITLE458,
                  459: TITLE459, 460: TITLE460, 461: TITLE461,
                  462: TITLE462, 463: TITLE463, 464: TITLE464,
                  465: TITLE465, 466: TITLE466, 467: TITLE467,
                  468: TITLE468}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestRischio468:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 3
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D"]
        rB, rC, rD = m["righe"]
        assert rB["rischio"]["media_annua"] == pytest.approx(MEDIA_B)
        assert rB["rischio"]["std_annua"] == pytest.approx(STD_B, rel=1e-9)
        assert rB["rischio"]["var_perdita"] == pytest.approx(VAR_B,
                                                           rel=1e-9)
        assert rB["rischio"]["capitale"] == pytest.approx(CAP_B)
        assert rB["rischio"]["es"] == pytest.approx(ES_B, rel=1e-9)
        assert rC["rischio"]["media_annua"] == pytest.approx(MEDIA_C)
        assert rC["rischio"]["std_annua"] == pytest.approx(STD_C, rel=1e-9)
        assert rC["rischio"]["var_perdita"] == pytest.approx(VAR_C,
                                                           rel=1e-9)
        assert rC["rischio"]["capitale"] == pytest.approx(CAP_C)
        assert rC["rischio"]["es"] == pytest.approx(ES_C, rel=1e-9)
        assert rD["rischio"]["media_annua"] == pytest.approx(MEDIA_D)
        assert rD["rischio"]["std_annua"] == pytest.approx(STD_D, rel=1e-9)
        assert rD["rischio"]["var_perdita"] == pytest.approx(VAR_D,
                                                           rel=1e-9)
        assert rD["rischio"]["capitale"] == pytest.approx(CAP_D, rel=1e-9)
        assert rD["rischio"]["es"] == pytest.approx(ES_D, rel=1e-9)
        assert rB["verdetto"] == VERD_B
        assert rC["verdetto"] == VERD_C
        assert rD["verdetto"] == VERD_D
        assert m["media_tot"] == pytest.approx(MEDIA_TOT)
        assert m["std_tot"] == pytest.approx(STD_TOT, rel=1e-9)
        assert m["var_perdita_tot"] == pytest.approx(VAR_TOT, rel=1e-9)
        assert m["capitale_tot"] == pytest.approx(CAP_TOT)
        assert m["es_tot"] == pytest.approx(ES_TOT, rel=1e-9)
        assert m["verdetto"] == VERD_PTF
        # disegno: B e C non richiedono capitale, D coperto,
        # portafoglio non richiede capitale
        assert rB["verdetto"].startswith("NON RICHIESTO")
        assert rC["verdetto"].startswith("NON RICHIESTO")
        assert rD["verdetto"].startswith("COPERTO")
        assert m["verdetto"].startswith("NON RICHIESTO")

    def test_formula_a_mano(self):
        # lam=10, mu=100, sigma=50, alpha=0.01: media=1000,
        # var=125000, std=353.5534, z=-2.326347874040841,
        # var_perdita=-(1000+z*std)=-177.5118,
        # es=-1000+std*phi(z)/0.01=-57.7045, capitale=0
        r = _F["mh468_rischio"](10.0, 100.0, 50.0)
        assert r["media_annua"] == pytest.approx(1000.0)
        assert r["var_annua"] == pytest.approx(125000.0)
        assert r["std_annua"] == pytest.approx(353.5533905932738,
                                              rel=1e-9)
        assert r["z_alpha"] == pytest.approx(-2.326347874040841,
                                            rel=1e-12)
        assert r["var_perdita"] == pytest.approx(-177.51182143340657,
                                                 rel=1e-9)
        assert r["es"] == pytest.approx(-57.70447573933086, rel=1e-9)
        assert r["capitale"] == 0.0

    def test_es_domina_var(self):
        # proprieta' di Mills: ES >= VaR per ogni configurazione
        R = _F["mh468_rischio"]
        for cfg in ((12.0, 17000.0, 8000.0), (20.0, 250.0, 5000.0),
                    (5.0, -20.0, 100.0), (3.0, 0.0, 1000.0)):
            r = R(*cfg)
            assert r["es"] >= r["var_perdita"] - 1e-9, cfg

    def test_verdetti_copertura(self):
        V = _F["mh468_verdetto"]
        assert V(47083.70, 100000.0).startswith("COPERTO")
        assert V(47083.70, 47083.70).startswith("COPERTO")
        assert V(47083.70, 30000.0).startswith("MARGINALE")
        assert V(47083.70, 23541.85).startswith("MARGINALE")
        assert V(47083.70, 20000.0).startswith("SOTTO-CAPITALIZZATO")
        assert V(47083.70, 0.0).startswith("SOTTO-CAPITALIZZATO")
        assert V(0.0, 50000.0).startswith("NON RICHIESTO")
        assert V(0.0, 0.0).startswith("NON RICHIESTO")

    def test_phi_inv(self):
        P = _F["mh468_phi_inv"]
        assert P(0.01) == pytest.approx(-2.326347874040841, rel=1e-12)
        assert P(0.5) == 0.0
        assert P(0.99) == pytest.approx(2.326347874040841, rel=1e-12)
        assert _F["mh468_phi"](P(0.37)) == pytest.approx(0.37, rel=1e-12)

    def test_mappa_totali(self):
        m = _demo()
        assert m["media_tot"] == pytest.approx(
            sum(r["rischio"]["media_annua"] for r in m["righe"]))
        assert m["var_tot"] == pytest.approx(
            sum(r["rischio"]["var_annua"] for r in m["righe"]))
        assert m["std_tot"] == pytest.approx(
            math.sqrt(sum(r["rischio"]["var_annua"] for r in m["righe"])))
        assert m["var_perdita_tot"] == pytest.approx(
            -(m["media_tot"] + m["z_alpha"] * m["std_tot"]))
        # singolo segnale con media negativa: capitale > 0
        # (lam=5, mu=-20, sigma=100: media=-100, var_perdita=630.49)
        m0 = _F["mh468_mappa"]([("Z", 5.0, -20.0, 100.0)], 1000.0)
        assert m0["righe"][0]["rischio"]["capitale"] == pytest.approx(
            630.4889352425982, rel=1e-9)
        assert m0["righe"][0]["verdetto"].startswith("COPERTO")
        assert m0["verdetto"].startswith("COPERTO")

    def test_degeneri(self):
        R, V, M, P = (_F["mh468_rischio"], _F["mh468_verdetto"],
                      _F["mh468_mappa"], _F["mh468_phi_inv"])
        for bad in (lambda: R(0, 100, 10),
                    lambda: R(-2, 100, 10),
                    lambda: R(5, 100, -1),
                    lambda: R(5, 100, 10, alpha=0.0),
                    lambda: R(5, 100, 10, alpha=0.5),
                    lambda: R(5, 100, 10, alpha=0.7),
                    lambda: R(5, 100, 10, mult=0.9),
                    lambda: R("x", 100, 10),
                    lambda: R(True, 100, 10),
                    lambda: R(5, 100, float("nan")),
                    lambda: P(0.0),
                    lambda: P(1.0),
                    lambda: P(-0.1),
                    lambda: V(-1, 100),
                    lambda: V(100, -1),
                    lambda: M([], 1000),
                    lambda: M("B", 1000),
                    lambda: M([("B", 1, 2)], 1000),
                    lambda: M([(123, 1, 2, 3)], 1000),
                    lambda: M([("", 1, 2, 3)], 1000),
                    lambda: M([("B", 1, 2, 3)], -5)):
            with pytest.raises(ValueError):
                bad()

    def test_determinismo(self):
        m1 = _F["mh468_mappa"](SEGNALI, CAP_DISP)
        m2 = _F["mh468_mappa"](SEGNALI, CAP_DISP)
        assert m1 == m2
