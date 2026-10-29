"""Test tab469 '📊 VaR per segnale: chi mangia il capitale?': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh469_num", "mh469_componenti", "mh469_verdetto",
           "mh468_num", "mh468_phi", "mh468_phi_inv",
           "mh468_rischio", "mh468_verdetto", "mh468_mappa")

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
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"

# Segnali demo deterministici: (nome, lam, mu, sigma)
# B/C/D/E: E e' il "goloso" (mu negativo, sigma alta), B diversifica
SEGNALI = (("B", 12.0, 2000.0, 8000.0),
           ("C", 8.0, 3000.0, 12000.0),
           ("D", 20.0, 250.0, 5000.0),
           ("E", 10.0, -500.0, 20000.0))

COMP_B = -533.3299309150316
QUOTA_B = -0.0038044368393112915
VPWO_B = 152062.4273587965
RISP_B = -11876.125563974463
MEDIA_B = 24000.0
STD_B = 28565.7137141714
COMP_C = 11200.005103627453
QUOTA_C = 0.07989371971606672
VPWO_C = 145675.94231240128
RISP_C = -5489.640517579246
MEDIA_C = 24000.0
STD_C = 34985.7113690718
COMP_D = 9415.034769765738
QUOTA_D = 0.06716087555791057
VPWO_D = 137835.20702464398
RISP_D = 2351.0947701780533
MEDIA_D = 5000.0
STD_D = 22388.613177238112
COMP_E = 120104.59185234386
QUOTA_E = 0.8567498415653338
VPWO_E = 64273.086097863226
RISP_E = 75913.21569695881
MEDIA_E = -5000.0
STD_E = 63265.314351546534
VP_TOT = 140186.30179482204
CAP_TOT = 140186.30179482204
TOP = 'E'
QUOTA_TOP = 0.8567498415653338
BEN_DIV = 158917.25304968294
VERD = 'CHI MANGIA IL CAPITALE — E assorbe 86% del capitale (120,105 EUR); tagliandolo il capitale scende a 64,273 EUR (Δ +75,913 EUR)'

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh469_componenti"](SEGNALI)
    return _DEMO


class TestRegistry469:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 806
        assert "tab469" in dvars
        assert "tab469" in withs

    def test_titoli_allineati_457_458_459_460_461_462_463_464_465_466_467_468_469(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {457: TITLE457, 458: TITLE458,
                  459: TITLE459, 460: TITLE460, 461: TITLE461,
                  462: TITLE462, 463: TITLE463, 464: TITLE464,
                  465: TITLE465, 466: TITLE466, 467: TITLE467,
                  468: TITLE468, 469: TITLE469}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestComponenti469:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["n_segnali"] == 4
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["B", "C", "D", "E"]
        rB, rC, rD, rE = m["righe"]
        for r, comp, quota, vpwo, risp, media, std in (
                (rB, COMP_B, QUOTA_B, VPWO_B, RISP_B, MEDIA_B, STD_B),
                (rC, COMP_C, QUOTA_C, VPWO_C, RISP_C, MEDIA_C, STD_C),
                (rD, COMP_D, QUOTA_D, VPWO_D, RISP_D, MEDIA_D, STD_D),
                (rE, COMP_E, QUOTA_E, VPWO_E, RISP_E, MEDIA_E, STD_E)):
            assert r["componente"] == pytest.approx(comp, rel=1e-9)
            assert r["quota"] == pytest.approx(quota, rel=1e-9)
            assert r["var_perdita_wo"] == pytest.approx(vpwo, rel=1e-9)
            assert r["risparmio"] == pytest.approx(risp, rel=1e-9)
            assert r["media"] == pytest.approx(media)
            assert r["std"] == pytest.approx(std, rel=1e-9)
        assert m["var_perdita"] == pytest.approx(VP_TOT, rel=1e-9)
        assert m["capitale"] == pytest.approx(CAP_TOT)
        assert m["top"] == TOP
        assert m["quota_top"] == pytest.approx(QUOTA_TOP, rel=1e-9)
        assert m["beneficio_diversificazione"] == pytest.approx(BEN_DIV,
                                                               rel=1e-9)
        assert _F["mh469_verdetto"](m) == VERD
        # disegno: E e' il piu' goloso (85.7% del capitale); B
        # diversifica (componente negativa: tagliarlo COSTA capitale)
        assert TOP == "E"
        assert rE["quota"] > 0.85
        assert rB["componente"] < 0.0
        assert rB["risparmio"] < 0.0
        assert VERD.startswith("CHI MANGIA IL CAPITALE")

    def test_somma_componenti_uguale_var(self):
        # allocazione Euleriana: la somma delle componenti E' il VaR
        m = _demo()
        assert sum(r["componente"] for r in m["righe"]) == pytest.approx(
            m["var_perdita"], rel=1e-9)

    def test_quote_sommano_uno(self):
        m = _demo()
        assert m["var_perdita"] > 0.0
        assert sum(r["quota"] for r in m["righe"]) == pytest.approx(1.0)

    def test_formula_a_mano(self):
        # S1=(lam 2, mu 100, sigma 10), S2=(3, 50, 20), alpha=0.01:
        # media_1=200, var_1=20200; media_2=150, var_2=8700;
        # M=350, V=28900, std=170, z=-2.326347874040841 ->
        # vp = -(350+z*170) = 45.48;
        # comp_1 = -(200+z*20200/170) = 76.42;
        # comp_2 = -(150+z*8700/170) = -30.95; somma = 45.48
        C = _F["mh469_componenti"]
        m = C([("S1", 2.0, 100.0, 10.0), ("S2", 3.0, 50.0, 20.0)])
        assert m["var_perdita"] == pytest.approx(45.48, abs=0.01)
        assert m["righe"][0]["componente"] == pytest.approx(76.42,
                                                            abs=0.01)
        assert m["righe"][1]["componente"] == pytest.approx(-30.95,
                                                           abs=0.01)
        assert m["righe"][0]["componente"] + m["righe"][1][
            "componente"] == pytest.approx(m["var_perdita"], rel=1e-9)

    def test_euler_differenze_finite(self):
        # comp_i deve coincidere con d(vp)/d(w_i) numerica
        # (w_i scala il P&L del segnale i)
        C = _F["mh469_componenti"]
        m = C(SEGNALI)
        medie = [r["media"] for r in m["righe"]]
        varianze = [r["var"] for r in m["righe"]]
        z = statistics.NormalDist().inv_cdf(0.01)

        def vp_w(w):
            mw = sum(w[i] * medie[i] for i in range(len(w)))
            vw = sum(w[i] ** 2 * varianze[i] for i in range(len(w)))
            return -(mw + z * math.sqrt(vw))

        eps = 1e-5
        for i, r in enumerate(m["righe"]):
            wp = [1.0] * len(medie)
            wm = [1.0] * len(medie)
            wp[i] += eps
            wm[i] -= eps
            fd = (vp_w(wp) - vp_w(wm)) / (2 * eps)
            assert r["componente"] == pytest.approx(fd, rel=1e-6)

    def test_whatif_taglio(self):
        # tagliare l'unico segnale azzera il capitale;
        # risparmio = capitale - max(0, vp_wo)*mult per costruzione
        C = _F["mh469_componenti"]
        m1 = C([("Z", 5.0, -20.0, 100.0)])
        assert m1["n_segnali"] == 1
        assert m1["righe"][0]["componente"] == pytest.approx(
            m1["var_perdita"], rel=1e-12)
        assert m1["righe"][0]["var_perdita_wo"] == pytest.approx(0.0)
        assert m1["righe"][0]["capitale_wo"] == 0.0
        assert m1["righe"][0]["risparmio"] == pytest.approx(
            m1["capitale"])
        m = _demo()
        for r in m["righe"]:
            assert r["risparmio"] == pytest.approx(
                m["capitale"] - max(0.0, r["var_perdita_wo"]))

    def test_mult(self):
        C = _F["mh469_componenti"]
        m = C(SEGNALI, mult=1.25)
        assert m["capitale"] == pytest.approx(m["var_perdita"] * 1.25)
        for r in m["righe"]:
            assert r["capitale_wo"] == pytest.approx(
                max(0.0, r["var_perdita_wo"]) * 1.25)

    def test_beneficio_diversificazione_nonnegativo(self):
        # somma VaR singoli >= VaR portafoglio (indipendenti, approx)
        C = _F["mh469_componenti"]
        for cfgs in ((("A", 12.0, 2000.0, 8000.0),
                      ("B", 8.0, 3000.0, 12000.0)),
                     (("A", 5.0, -100.0, 5000.0),
                      ("B", 5.0, 50.0, 5000.0),
                      ("C", 5.0, 200.0, 1000.0))):
            m = C(list(cfgs))
            assert m["beneficio_diversificazione"] >= -1e-9, cfgs

    def test_verdetto_nessun_capitale(self):
        # coda in utile -> nessun segnale da tagliare
        # (lam=10, mu=100000, sigma=100: vp < 0; con lam=1 il VaR
        # e' sempre > 0, serve lam > z^2 per la coda in utile)
        C = _F["mh469_componenti"]
        V = _F["mh469_verdetto"]
        m = C([("S", 10.0, 100000.0, 100.0)])
        assert m["capitale"] == 0.0
        assert V(m).startswith("NESSUN CAPITALE RICHIESTO")

    def test_degeneri(self):
        C, V, N = (_F["mh469_componenti"], _F["mh469_verdetto"],
                   _F["mh469_num"])
        for bad in (lambda: C([], 0.01),
                    lambda: C("B", 0.01),
                    lambda: C([("B", 1, 2)], 0.01),
                    lambda: C([(123, 1, 2, 3)]),
                    lambda: C([("", 1, 2, 3)]),
                    lambda: C([("B", 0, 2, 3)]),
                    lambda: C([("B", -1, 2, 3)]),
                    lambda: C([("B", 1, 2, -3)]),
                    lambda: C([("B", 1, 2, 3)], alpha=0.0),
                    lambda: C([("B", 1, 2, 3)], alpha=0.5),
                    lambda: C([("B", 1, 2, 3)], alpha=0.7),
                    lambda: C([("B", 1, 2, 3)], mult=0.9),
                    lambda: C([("B", "x", 2, 3)]),
                    lambda: C([("B", 1, 2, float("nan"))]),
                    lambda: V({}),
                    lambda: V({"righe": []}),
                    lambda: N(True, "x"),
                    lambda: N(float("inf"), "x")):
            with pytest.raises(ValueError):
                bad()

    def test_determinismo(self):
        m1 = _F["mh469_componenti"](SEGNALI)
        m2 = _F["mh469_componenti"](SEGNALI)
        assert m1["var_perdita"] == m2["var_perdita"]
        assert [r["componente"] for r in m1["righe"]] == [
            r["componente"] for r in m2["righe"]]
