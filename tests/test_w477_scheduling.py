"""Test tab477 '⏳ Scheduling di esecuzione': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh477_num", "mh477_parametri", "mh477_traiettoria",
           "mh477_frontiera", "mh477_vwap", "mh477_verdetto")

TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE477 = "⏳ Scheduling di esecuzione"
TITLE476 = "🎯 Calibrazione: previsto vs realizzato"

# Demo deterministica: gamba B di tab475/476 — nozionale 715'069.11 EUR,
# ADV 50M, spread 5 bps, sigma_g 2%, c_impact 1.197 (k calibrato tab476),
# orizzonte 6.5 ore in 13 bucket da 30'.
X = 715069.1088685506
SG = 0.02
ADV = 50_000_000.0
SP = 5.0
CI = 1.197
ORE = 6.5
NB = 13

ETA = 4.788e-10
TAU = 0.020833333333333332
E_VWAP = 1205.135802314905
STD_VWAP = 4544.184880706017
SPREAD = 178.76727721713766
TEMP_VWAP = 903.957600086107
PERM = 122.41092501166031
E_L6 = 1205.2098091592502
STD_L6 = 4527.822009823313
Q_L6 = 0.5037831377032891
E_L4 = 1512.3295180895655
STD_L4 = 3580.5188940257794
Q_L4 = 0.7312503022714811
VERD0 = ("SCHEDULING NEUTRO — lambda = 0: l'ottimo coincide con la VWAP "
         "(costo atteso 1,205 EUR, std 4,544 EUR).")
VERD4 = ("SCHEDULING AGGRESSIVO — costo atteso 1,512 EUR (+307 vs VWAP), "
         "std 3,581 EUR (-964 vs VWAP): paghi 307 EUR di costo atteso per "
         "tagliare 964 EUR di rischio di timing.")


def _par():
    return _F["mh477_parametri"](X, SG, ADV, SP, CI, ORE, NB)


class TestRegistry481:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 663

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE482 in titoli
        assert TITLE477 in titoli  # membership (non [-2]: la posizione scorre a ogni ciclo)
        assert "tab482" in dvars
        assert f"with tab482:" in src

    def test_chiavi_univoche(self):
        import re
        from collections import Counter
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        keys = re.findall(r'key="(st477_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 9


class TestNum477:
    def test_ok(self):
        assert _F["mh477_num"](3, "x") == 3.0
        assert _F["mh477_num"](2.5, "x") == 2.5

    @pytest.mark.parametrize("bad", [True, float("nan"), float("inf"),
                                     float("-inf"), "3", None])
    def test_degeneri(self, bad):
        with pytest.raises(ValueError):
            _F["mh477_num"](bad, "x")


class TestParametri477:
    def test_demo(self):
        p = _par()
        assert p["notionale"] == X
        assert p["n_bucket"] == NB
        assert abs(p["eta"] - ETA) / ETA < 1e-12
        assert abs(p["tau_giorni"] - TAU) < 1e-15
        assert abs(p["T_giorni"] - ORE / 24.0) < 1e-15

    def test_n_bucket_float_intero(self):
        p = _F["mh477_parametri"](X, SG, ADV, SP, CI, ORE, 13.0)
        assert p["n_bucket"] == 13

    @pytest.mark.parametrize("kw", [
        {"notionale": 0.0}, {"notionale": -5.0},
        {"sigma_g": 0.0}, {"sigma_g": 1.0}, {"sigma_g": 1.5},
        {"adv": 0.0}, {"adv": -1.0},
        {"spread_bps": -0.5},
        {"c_impact": 0.0},
        {"ore": 0.0}, {"ore": -2.0},
        {"n_bucket": 1}, {"n_bucket": 2.5},
    ])
    def test_degeneri(self, kw):
        args = {"notionale": X, "sigma_g": SG, "adv": ADV,
                "spread_bps": SP, "c_impact": CI, "ore": ORE,
                "n_bucket": NB}
        args.update(kw)
        with pytest.raises(ValueError):
            _F["mh477_parametri"](**args)


class TestTraiettoria477:
    def test_vwap_uniforme(self):
        v = _F["mh477_vwap"](_par())
        assert len(v["bucket"]) == NB
        for b in v["bucket"]:
            assert abs(b["trade"] - X / NB) < 1e-6
        assert abs(sum(b["trade"] for b in v["bucket"]) - X) < 1e-6
        assert abs(v["quota_prima_meta"] - 0.5) < 1e-12
        assert v["kappa"] == 0.0

    def test_vwap_valori(self):
        v = _F["mh477_vwap"](_par())
        assert abs(v["costo_spread"] - SPREAD) < 1e-9
        assert abs(v["costo_temp"] - TEMP_VWAP) < 1e-6
        assert abs(v["costo_perm"] - PERM) < 1e-6
        assert abs(v["costo_atteso"] - E_VWAP) < 1e-6
        assert abs(v["std_costo"] - STD_VWAP) < 1e-6

    def test_spread_coincide_tab476(self):
        # lo spread del modello = previsto_spread B di tab476
        v = _F["mh477_vwap"](_par())
        assert abs(v["costo_spread"] - 178.76727721713766) < 1e-9

    def test_lambda_zero_e_vwap(self):
        r = _F["mh477_traiettoria"](_par(), 0.0)
        v = _F["mh477_vwap"](_par())
        assert abs(r["costo_atteso"] - v["costo_atteso"]) < 1e-9
        assert abs(r["std_costo"] - v["std_costo"]) < 1e-9

    def test_lambda_1e_6(self):
        r = _F["mh477_traiettoria"](_par(), 1e-6)
        assert abs(r["costo_atteso"] - E_L6) < 1e-6
        assert abs(r["std_costo"] - STD_L6) < 1e-6
        assert abs(r["quota_prima_meta"] - Q_L6) < 1e-9
        # trade-off onesto: E sale (o pareggia), std scende vs VWAP
        assert r["costo_atteso"] >= E_VWAP - 1e-6
        assert r["std_costo"] <= STD_VWAP + 1e-6
        assert r["quota_prima_meta"] > 0.5
        assert abs(sum(b["trade"] for b in r["bucket"]) - X) < 1e-6

    def test_lambda_1e_4_aggressivo(self):
        r = _F["mh477_traiettoria"](_par(), 1e-4)
        assert abs(r["costo_atteso"] - E_L4) < 1e-6
        assert abs(r["std_costo"] - STD_L4) < 1e-6
        assert abs(r["quota_prima_meta"] - Q_L4) < 1e-9
        assert r["quota_prima_meta"] > 0.70
        assert r["costo_atteso"] > E_VWAP
        assert r["std_costo"] < STD_VWAP

    def test_lambda_negativa(self):
        with pytest.raises(ValueError):
            _F["mh477_traiettoria"](_par(), -1e-6)

    def test_par_incompleto(self):
        with pytest.raises(ValueError):
            _F["mh477_traiettoria"]({"notionale": X}, 0.0)


class TestFrontiera477:
    def test_monotonia(self):
        fr = _F["mh477_frontiera"](_par(), [0.0, 1e-7, 1e-6, 1e-5, 1e-4])
        assert len(fr) == 5
        assert [p["lambda"] for p in fr] == [0.0, 1e-7, 1e-6, 1e-5, 1e-4]
        es = [p["costo_atteso"] for p in fr]
        ss = [p["std_costo"] for p in fr]
        assert all(es[i] <= es[i + 1] + 1e-6 for i in range(4))
        assert all(ss[i] >= ss[i + 1] - 1e-6 for i in range(4))
        assert abs(es[0] - E_VWAP) < 1e-9

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh477_frontiera"](_par(), [])


class TestVerdetto477:
    def test_neutro(self):
        v = _F["mh477_vwap"](_par())
        assert _F["mh477_verdetto"](v, v) == VERD0

    def test_aggressivo(self):
        r = _F["mh477_traiettoria"](_par(), 1e-4)
        v = _F["mh477_vwap"](_par())
        assert _F["mh477_verdetto"](r, v) == VERD4

    def test_chiavi_mancanti(self):
        v = _F["mh477_vwap"](_par())
        with pytest.raises(ValueError):
            _F["mh477_verdetto"]({"costo_atteso": 1.0}, v)
        with pytest.raises(ValueError):
            _F["mh477_verdetto"](v, [1, 2, 3])


class TestRegressione476:
    def test_mh476_ancora_ok(self):
        G = _load("mh476_num", "mh476_riga", "mh476_verdetto",
                 "mh476_statistiche")
        r = G["mh476_riga"]("B", 178.76727721713766, 1710.2792188152227,
                            185.2, 2050.0, 715069.1088685506)
        assert abs(r["err_tot"] - 346.1535039676394) < 1e-9
