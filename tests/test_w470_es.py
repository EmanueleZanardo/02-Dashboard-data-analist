"""Test tab470 '📈 Expected Shortfall: quanto perdi quando perdi?': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh470_num", "mh470_shortfall", "mh470_verdetto",
           "mh468_num", "mh468_phi_inv")

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
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"

# Segnali demo deterministici: (nome, lam, mu, sigma)
# B/C/D/E: E e' il "goloso" dell'ES, B e C diversificano
SEGNALI = (("B", 12.0, 2000.0, 8000.0),
           ("C", 8.0, 3000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0),
           ("E", 10.0, -500.0, 20000.0))

COMP_B = 2884.9312994839747
QUOTA_B = 0.01721336141194049
ESWO_B = 177708.47632095256
RISP_B = -10110.107214337011
MEDIA_B = 24000.0
STD_B = 28565.7137141714
COMP_C = 16327.396949225964
QUOTA_C = 0.0974197841915723
ESWO_C = 170391.70699611702
RISP_C = -2793.3378895014757
MEDIA_C = 24000.0
STD_C = 34985.7113690718
COMP_D = 11514.793889542088
QUOTA_D = 0.0687046893768823
ESWO_D = 164176.48064564483
RISP_D = 3421.8884609707166
MEDIA_D = 5000.0
STD_D = 22388.613177238112
COMP_E = 136871.2469683635
QUOTA_E = 0.8166621650196048
ESWO_E = 81355.61388716713
RISP_E = 86242.75521944842
MEDIA_E = -5000.0
STD_E = 63265.314351546534
ES_TOT = 167598.36910661554
VP_TOT = 140186.30179482204
DELTA = 27412.067311793508
CAP_TOT = 167598.36910661554
TOP = 'E'
QUOTA_TOP = 0.8166621650196048
BEN_DIV = 182065.85842667165
VERD = "QUANTO PERDI QUANDO PERDI — ES 167,598 EUR vs VaR 140,186 EUR (Δ +27,412 EUR): quando la coda colpisce perdi in media il 19.6% in più della soglia; il più goloso è E (82% dell'ES): tagliandolo il capitale scende a 81,356 EUR (Δ +86,243 EUR)"

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh470_shortfall"](SEGNALI)
    return _DEMO


class TestRegistry470:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 825
        assert "tab470" in dvars
        assert "tab470" in withs

    def test_titoli_allineati_458_459_460_461_462_463_464_465_466_467_468_469_470(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {458: TITLE458, 459: TITLE459,
                  460: TITLE460, 461: TITLE461, 462: TITLE462,
                  463: TITLE463, 464: TITLE464, 465: TITLE465,
                  466: TITLE466, 467: TITLE467, 468: TITLE468,
                  469: TITLE469, 470: TITLE470}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestShortfall470:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 4
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D", "E"]
        rB, rC, rD, rE = m["righe"]
        for r, comp, quota, eswo, risp, media, std in (
                (rB, COMP_B, QUOTA_B, ESWO_B, RISP_B, MEDIA_B, STD_B),
                (rC, COMP_C, QUOTA_C, ESWO_C, RISP_C, MEDIA_C, STD_C),
                (rD, COMP_D, QUOTA_D, ESWO_D, RISP_D, MEDIA_D, STD_D),
                (rE, COMP_E, QUOTA_E, ESWO_E, RISP_E, MEDIA_E, STD_E)):
            assert r["componente"] == pytest.approx(comp, rel=1e-9)
            assert r["quota"] == pytest.approx(quota, rel=1e-9)
            assert r["es_perdita_wo"] == pytest.approx(eswo, rel=1e-9)
            assert r["risparmio"] == pytest.approx(risp, rel=1e-9)
            assert r["media"] == pytest.approx(media)
            assert r["std"] == pytest.approx(std, rel=1e-9)
        assert m["es_perdita"] == pytest.approx(ES_TOT, rel=1e-9)
        assert m["var_perdita"] == pytest.approx(VP_TOT, rel=1e-9)
        assert m["delta_var"] == pytest.approx(DELTA, rel=1e-9)
        assert m["capitale"] == pytest.approx(CAP_TOT)
        assert m["top"] == TOP
        assert m["quota_top"] == pytest.approx(QUOTA_TOP, rel=1e-9)
        assert m["beneficio_diversificazione"] == pytest.approx(BEN_DIV,
                                                                rel=1e-9)
        assert _F["mh470_verdetto"](m) == VERD
        # disegno: ES ~167'598 > VaR 140'186 (Delta +27'412, +19.6%);
        # E e' il piu' goloso (81.7% dell'ES); B e C diversificano
        assert TOP == "E"
        assert rE["quota"] > 0.81
        assert rB["risparmio"] < 0.0
        assert rC["risparmio"] < 0.0
        assert VERD.startswith("QUANTO PERDI QUANDO PERDI")

    def test_somma_componenti_uguale_es(self):
        # allocazione Euleriana: la somma delle componenti E' l'ES
        m = _demo()
        assert sum(r["componente"] for r in m["righe"]) == pytest.approx(
            m["es_perdita"], rel=1e-9)

    def test_quote_sommano_uno(self):
        m = _demo()
        assert m["es_perdita"] > 0.0
        assert sum(r["quota"] for r in m["righe"]) == pytest.approx(1.0)

    def test_es_maggiore_uguale_var(self):
        # chiave teorica: k = phi(z)/alpha > |z| => ES >= VaR SEMPRE
        m = _demo()
        assert m["es_perdita"] >= m["var_perdita"]
        assert m["delta_var"] == pytest.approx(
            m["es_perdita"] - m["var_perdita"])
        assert m["delta_var"] > 0.0

    def test_formula_a_mano(self):
        # S=(lam 10, mu -500, sigma 100), alpha=0.01:
        # M=-5000, V=2600000, std=1612.45, k=2.66521 ->
        # es = k*std - M = 9297.53; vp = 8751.12
        S = _F["mh470_shortfall"]
        m = S([("S", 10.0, -500.0, 100.0)])
        assert m["es_perdita"] == pytest.approx(9297.53, abs=0.01)
        assert m["righe"][0]["componente"] == pytest.approx(
            m["es_perdita"], rel=1e-12)
        assert m["var_perdita"] == pytest.approx(8751.12, abs=0.01)
        assert m["es_perdita"] > m["var_perdita"]

    def test_euler_differenze_finite(self):
        # comp_i deve coincidere con d(es)/d(w_i) numerica
        # (implementazione indipendente via statistics.NormalDist)
        S = _F["mh470_shortfall"]
        m = S(SEGNALI)
        medie = [r["media"] for r in m["righe"]]
        varianze = [r["var"] for r in m["righe"]]
        _nd = statistics.NormalDist()
        _k = _nd.pdf(_nd.inv_cdf(0.01)) / 0.01

        def es_w(w):
            mw = sum(w[i] * medie[i] for i in range(len(w)))
            vw = sum(w[i] ** 2 * varianze[i] for i in range(len(w)))
            return _k * math.sqrt(vw) - mw

        eps = 1e-5
        for i, r in enumerate(m["righe"]):
            wp = [1.0] * len(medie)
            wm = [1.0] * len(medie)
            wp[i] += eps
            wm[i] -= eps
            fd = (es_w(wp) - es_w(wm)) / (2 * eps)
            assert r["componente"] == pytest.approx(fd, rel=1e-6)

    def test_whatif_taglio(self):
        # tagliare l'unico segnale azzera il capitale;
        # risparmio = capitale - max(0, es_wo)*mult per costruzione
        S = _F["mh470_shortfall"]
        m1 = S([("Z", 10.0, -500.0, 100.0)])
        assert m1["n_segnali"] == 1
        assert m1["righe"][0]["componente"] == pytest.approx(
            m1["es_perdita"], rel=1e-12)
        assert m1["righe"][0]["es_perdita_wo"] == pytest.approx(0.0)
        assert m1["righe"][0]["capitale_wo"] == 0.0
        assert m1["righe"][0]["risparmio"] == pytest.approx(
            m1["capitale"])
        m = _demo()
        for r in m["righe"]:
            assert r["risparmio"] == pytest.approx(
                m["capitale"] - max(0.0, r["es_perdita_wo"]))

    def test_mult(self):
        S = _F["mh470_shortfall"]
        m = S(SEGNALI, mult=1.25)
        assert m["capitale"] == pytest.approx(m["es_perdita"] * 1.25)
        for r in m["righe"]:
            assert r["capitale_wo"] == pytest.approx(
                max(0.0, r["es_perdita_wo"]) * 1.25)

    def test_beneficio_diversificazione_nonnegativo(self):
        # somma ES singoli >= ES portafoglio (indipendenti, approx)
        S = _F["mh470_shortfall"]
        for cfgs in ((("A", 12.0, 2000.0, 8000.0),
                      ("B", 8.0, 3000.0, 12000.0)),
                     (("A", 5.0, -100.0, 5000.0),
                      ("B", 5.0, 50.0, 5000.0),
                      ("C", 5.0, 200.0, 1000.0))):
            m = S(list(cfgs))
            assert m["beneficio_diversificazione"] >= -1e-9, cfgs

    def test_verdetto_nessun_capitale(self):
        # coda in utile -> nessun segnale da tagliare
        # (lam=10, mu=100000, sigma=100: es < 0)
        S = _F["mh470_shortfall"]
        V = _F["mh470_verdetto"]
        m = S([("S", 10.0, 100000.0, 100.0)])
        assert m["capitale"] == 0.0
        assert V(m).startswith("NESSUN CAPITALE RICHIESTO")

    def test_degeneri(self):
        S, V, N = (_F["mh470_shortfall"], _F["mh470_verdetto"],
                   _F["mh470_num"])
        for bad in (lambda: S([], 0.01),
                    lambda: S("B", 0.01),
                    lambda: S([("B", 1, 2)], 0.01),
                    lambda: S([(123, 1, 2, 3)]),
                    lambda: S([("", 1, 2, 3)]),
                    lambda: S([("B", 0, 2, 3)]),
                    lambda: S([("B", -1, 2, 3)]),
                    lambda: S([("B", 1, 2, -3)]),
                    lambda: S([("B", 1, 2, 3)], alpha=0.0),
                    lambda: S([("B", 1, 2, 3)], alpha=0.5),
                    lambda: S([("B", 1, 2, 3)], alpha=0.7),
                    lambda: S([("B", 1, 2, 3)], mult=0.9),
                    lambda: S([("B", "x", 2, 3)]),
                    lambda: S([("B", 1, 2, float("nan"))]),
                    lambda: V({}),
                    lambda: V({"righe": []}),
                    lambda: N(True, "x"),
                    lambda: N(float("inf"), "x")):
            with pytest.raises(ValueError):
                bad()

    def test_determinismo(self):
        m1 = _F["mh470_shortfall"](SEGNALI)
        m2 = _F["mh470_shortfall"](SEGNALI)
        assert m1["es_perdita"] == m2["es_perdita"]
        assert [r["componente"] for r in m1["righe"]] == [
            r["componente"] for r in m2["righe"]]
