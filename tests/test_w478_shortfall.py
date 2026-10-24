"""Test tab478 '📉 Implementation shortfall: scomponi il costo realizzato': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh478_num", "mh478_componenti", "mh478_attribuzione",
           "mh478_verdetto")

TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE478 = "📉 Implementation shortfall: scomponi il costo realizzato"
TITLE477 = "⏳ Scheduling di esecuzione"

# Demo deterministica: gamba B di tab475/476/477 — nozionale 715'069.11 EUR,
# prezzo di arrivo 100 EUR/unita' (X = 7150.69109 unita'), 13 bucket VWAP,
# gamma = 4.788e-6 EUR/unita'^2 (eta*p^2 da tab477), spread 5 bps,
# drift rialzista +0.025 EUR/unita' per bucket, impatto temporaneo
# 0.005*(1+0.2*sin(i*1.3)) EUR/unita'.
PA = 100.0
XU = 715069.11 / 100.0
NB = 13
GAMMA = 4.788e-6
SP = 5.0
IS_DEMO = 1401.1665862221123
IS_BPS_DEMO = 19.59484148633008
SPREAD_DEMO = 179.06367709134207
TEMP_DEMO = 36.504543762420695
PERM_DEMO = 131.82715042973578
TIMING_DEMO = 1053.7712149386136
RESIDUO_DEMO = 2.2737367544323206e-13
SP_MEDIO_DEMO = 5.0
QUOTA_TIMING_DEMO = 0.7520670456321962
VERD_DEMO = 'TIMING DOMINANTE — 75% dello shortfall (1,054 EUR a tuo sfavore, IS totale 1,401 EUR = 19.59 bps).'


def _demo():
    q = XU / NB
    qty = [q] * NB
    mid, px, sps = [], [], []
    cum = 0.0
    for i in range(NB):
        cum += q
        m = PA + GAMMA * (XU - cum) + 0.025 * i
        t = 0.005 * (1.0 + 0.2 * math.sin(i * 1.3))
        mid.append(m)
        px.append(m * (1.0 + SP / 20000.0) + t)
        sps.append(SP)
    return _F["mh478_componenti"](PA, mid, px, qty, sps, GAMMA)


class TestRegistry481:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 683

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE482 in titoli
        assert TITLE478 in titoli  # membership (non [-2]: la posizione scorre a ogni ciclo)
        assert "tab482" in dvars
        assert f"with tab482:" in src

    def test_chiavi_univoche(self):
        import re
        from collections import Counter
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        keys = re.findall(r'key="(st478_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 7


class TestNum478:
    def test_ok(self):
        assert _F["mh478_num"](3, "x") == 3.0
        assert _F["mh478_num"](2.5, "x") == 2.5

    @pytest.mark.parametrize("bad", [True, float("nan"), float("inf"),
                                     float("-inf"), "3", None])
    def test_degeneri(self, bad):
        with pytest.raises(ValueError):
            _F["mh478_num"](bad, "x")


class TestComponenti478:
    def test_demo(self):
        c = _demo()
        assert c["n"] == NB
        assert abs(c["X"] - XU) / XU < 1e-12
        assert abs(c["notionale"] - 715069.11) < 1e-6
        assert abs(c["is"] - IS_DEMO) < 1e-6
        assert abs(c["is_bps"] - IS_BPS_DEMO) < 1e-9
        assert abs(c["spread"] - SPREAD_DEMO) < 1e-6
        assert abs(c["temporaneo"] - TEMP_DEMO) < 1e-6
        assert abs(c["permanente"] - PERM_DEMO) < 1e-6
        assert abs(c["timing"] - TIMING_DEMO) < 1e-6
        assert abs(c["residuo"] - RESIDUO_DEMO) < 1e-9
        assert abs(c["spread_medio_bps"] - SP_MEDIO_DEMO) < 1e-12

    def test_chiusura(self):
        c = _demo()
        assert abs(c["residuo"]) < 1e-6
        assert abs(c["is"] - (c["spread"] + c["temporaneo"]
                              + c["permanente"] + c["timing"])) < 1e-6

    def test_spread_a_mano(self):
        # spread = Σ qty*mid*5/20000, ricalcolato indipendentemente
        q = XU / NB
        cum = 0.0
        att = 0.0
        for i in range(NB):
            cum += q
            m = PA + GAMMA * (XU - cum) + 0.025 * i
            att += q * m * SP / 20000.0
        assert abs(_demo()["spread"] - att) < 1e-9

    def test_permanente_a_mano(self):
        # permanente = gamma * Σ qty_i*(X - x_i), x_i = rimanente dopo i
        q = XU / NB
        att = 0.0
        for i in range(NB):
            x_dopo = XU - (i + 1) * q
            att += GAMMA * q * (XU - x_dopo)
        assert abs(_demo()["permanente"] - att) < 1e-9

    def test_is_bps_formula(self):
        c = _demo()
        assert abs(c["is_bps"] - c["is"] / c["notionale"] * 10000.0) < 1e-12

    def test_determinismo(self):
        a = _demo()
        b = _demo()
        assert a == b

    @pytest.mark.parametrize("kw", [
        {"p_arrivo": 0.0}, {"p_arrivo": -1.0}, {"gamma": -1e-9},
        {"mid": [100.0]},  # n < 2
        {"qty": [1.0] * 12},  # lunghezze diverse
        {"qty": [1.0] * 12 + [-1.0]},  # qty <= 0
        {"px": [100.0] * 12 + [0.0]},  # px <= 0
        {"mid": [100.0] * 12 + [-5.0]},  # mid <= 0
        {"spread_bps": [5.0] * 12 + [-1.0]},  # spread < 0
        {"p_arrivo": float("nan")}, {"gamma": "x"},
    ])
    def test_degeneri(self, kw):
        q = XU / NB
        args = {"p_arrivo": PA,
                "mid": [PA] * NB, "px": [PA * 1.001] * NB,
                "qty": [q] * NB, "spread_bps": [SP] * NB,
                "gamma": GAMMA}
        args.update(kw)
        with pytest.raises(ValueError):
            _F["mh478_componenti"](**args)


class TestAttribuzione478:
    def test_demo(self):
        att = _F["mh478_attribuzione"](_demo())
        assert att["dominante"] == "timing"
        assert att["segno_dominante"] == 1
        assert abs(att["quote"]["timing"] - QUOTA_TIMING_DEMO) < 1e-12
        assert abs(sum(att["quote"].values()) - 1.0) < 1e-12

    def test_spread_dominante_a_mano(self):
        comp = {"n": 3, "is": 500.0, "is_bps": 10.0, "spread": 400.0,
                "temporaneo": 50.0, "permanente": 30.0, "timing": 20.0,
                "spread_medio_bps": 5.0}
        att = _F["mh478_attribuzione"](comp)
        assert att["dominante"] == "spread"
        assert abs(att["quote"]["spread"] - 0.8) < 1e-12

    def test_timing_negativo(self):
        comp = {"n": 3, "is": -200.0, "is_bps": -4.0, "spread": 100.0,
                "temporaneo": 50.0, "permanente": 30.0, "timing": -800.0,
                "spread_medio_bps": 5.0}
        att = _F["mh478_attribuzione"](comp)
        assert att["dominante"] == "timing"
        assert att["segno_dominante"] == -1

    @pytest.mark.parametrize("bad", [
        {}, {"n": 3}, "no",
        {"n": 3, "is": 0.0, "is_bps": 0.0, "spread": 0.0,
         "temporaneo": 0.0, "permanente": 0.0, "timing": 0.0},
    ])
    def test_degeneri(self, bad):
        with pytest.raises(ValueError):
            _F["mh478_attribuzione"](bad)


class TestVerdetto478:
    def test_demo_timing_dominante(self):
        v = _F["mh478_verdetto"](_demo())
        assert v == VERD_DEMO
        assert v.startswith("TIMING DOMINANTE")

    def test_efficiente_a_mano(self):
        comp = {"n": 3, "is": 100.0, "is_bps": 2.0,
                "spread_medio_bps": 5.0}
        v = _F["mh478_verdetto"](comp)
        assert v.startswith("ESECUZIONE EFFICIENTE")

    def test_spread_dominante_a_mano(self):
        comp = {"n": 3, "is": 500.0, "is_bps": 10.0, "spread": 400.0,
                "temporaneo": 50.0, "permanente": 30.0, "timing": 20.0,
                "spread_medio_bps": 5.0}
        v = _F["mh478_verdetto"](comp)
        assert v == ("SPREAD DOMINANTE — 80% dello shortfall (400 EUR "
                     "a tuo sfavore, IS totale 500 EUR = 10.00 bps).")

    def test_timing_a_favore(self):
        comp = {"n": 3, "is": 600.0, "is_bps": 12.0, "spread": 1500.0,
                "temporaneo": 500.0, "permanente": 600.0,
                "timing": -2000.0, "spread_medio_bps": 5.0}
        v = _F["mh478_verdetto"](comp)
        assert v == ("TIMING DOMINANTE — 43% dello shortfall (-2,000 EUR "
                     "a tuo favore, IS totale 600 EUR = 12.00 bps).")

    def test_dati_insufficienti(self):
        comp = {"n": 1, "is": 0.0, "is_bps": 0.0}
        assert _F["mh478_verdetto"](comp).startswith("DATI INSUFFICIENTI")

    @pytest.mark.parametrize("bad", [
        "no", {}, {"n": 3, "is": 1.0},
        {"n": 3, "is": 500.0, "is_bps": 10.0, "spread": 400.0,
         "temporaneo": 50.0, "permanente": 30.0, "timing": 20.0,
         "spread_medio_bps": -1.0},
    ])
    def test_degeneri(self, bad):
        with pytest.raises(ValueError):
            _F["mh478_verdetto"](bad)
