"""Test tab362 'Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh362_num", "mh362_parse_seq", "mh362_g", "mh362_gbin",
           "mh362_gprime0", "mh362_fstar", "mh362_fstar_bin",
           "mh362_verdetto", "mh362_walk", "mh362_curva", "mh362_analisi")

TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
PW = 0.45
PM = 0.25
B = 1.5
M = 0.5
SEQ = "WWMLWMLWLMWMWLWLMWLW"
F3 = 0.2046663608817132
G3 = 0.02479318738161633
FBIN = 0.08333333333333333
GBIN = 0.005146108701076159
FIN3 = 1.6419158276581305
FINB = 1.3842811600324245
VERDETTO = 'BINARIO CONSERVATIVO: il modello a 2 esiti sottostima f* (8.33% vs 20.47% con tre esiti, 2.46x). Stai puntando troppo poco.'
PL = 1.0 - PW - PM


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry362:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 365
        assert "tab362" in dvars
        assert "tab362" in withs

    def test_titoli_allineati_358_359_360_361_362(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab365"
        assert titoli[-1] == TITLE365
        assert withs[-1] == "tab365"


class TestNum:
    def test_num_ok(self):
        assert _F["mh362_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_num"](float("nan"), "x")


class TestParseSeq:
    def test_ok(self):
        assert _F["mh362_parse_seq"]("wMl") == ("W", "M", "L")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_parse_seq"]("   ")

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_parse_seq"]("WX")


class TestG:
    def test_g_zero(self):
        assert _F["mh362_g"](0.0, PW, PM, PL, B, M) == 0.0
        assert _F["mh362_gbin"](0.0, PW, PM + PL, B) == 0.0

    def test_g_demo(self):
        assert abs(_F["mh362_g"](F3, PW, PM, PL, B, M) - G3) < 1e-12

    def test_g_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_g"](1.0, PW, PM, PL, B, M)


class TestFstar:
    def test_demo(self):
        f3, g3 = _F["mh362_fstar"](PW, PM, PL, B, M)
        assert abs(f3 - F3) < 1e-9
        assert abs(g3 - G3) < 1e-12

    def test_massimo_locale(self):
        f3, g3 = _F["mh362_fstar"](PW, PM, PL, B, M)
        assert g3 >= _F["mh362_g"](f3 - 0.01, PW, PM, PL, B, M)
        assert g3 >= _F["mh362_g"](f3 + 0.01, PW, PM, PL, B, M)

    def test_no_edge(self):
        f3, g3 = _F["mh362_fstar"](0.30, 0.10, 0.60, 1.0, 0.5)
        assert f3 == 0.0 and g3 == 0.0

    def test_bin_chiusa(self):
        assert abs(_F["mh362_fstar_bin"](PW, PM + PL, B) - FBIN) < 1e-12
        assert _F["mh362_fstar_bin"](0.30, 0.70, 1.0) == 0.0


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh362_verdetto"](0.0, 0.05).startswith("NESSUN EDGE")

    def test_binario_aggressivo(self):
        assert _F["mh362_verdetto"](0.05, 0.10).startswith(
            "BINARIO AGGRESSIVO")

    def test_differenza_moderata(self):
        assert _F["mh362_verdetto"](0.11, 0.10).startswith(
            "DIFFERENZA MODERATA")

    def test_binario_adeguato(self):
        assert _F["mh362_verdetto"](0.098, 0.10).startswith(
            "BINARIO ADEGUATO")

    def test_binario_conservativo(self):
        assert _F["mh362_verdetto"](0.20, 0.10).startswith(
            "BINARIO CONSERVATIVO")

    def test_binario_inutilizzabile(self):
        assert _F["mh362_verdetto"](0.05, 0.0).startswith(
            "BINARIO INUTILIZZABILE")


class TestWalk:
    def test_demo(self):
        sq = _F["mh362_parse_seq"](SEQ)
        w3 = _F["mh362_walk"](sq, F3, B, M)
        wb = _F["mh362_walk"](sq, FBIN, B, M)
        assert w3["n"] == wb["n"] == 20
        assert abs(w3["finale"] - FIN3) < 1e-9
        assert abs(wb["finale"] - FINB) < 1e-9
        assert len(w3["equity"]) == 21
        assert 0.0 <= w3["max_dd"] < 1.0

    def test_f_zero_fermo(self):
        sq = _F["mh362_parse_seq"]("WML")
        w = _F["mh362_walk"](sq, 0.0, B, M)
        assert all(e == 1.0 for e in w["equity"])

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_walk"](("W",), 1.0, B, M)


class TestCurva:
    def test_demo(self):
        c = _F["mh362_curva"](PW, PM, PL, B, M, 0.50, 25)
        assert len(c) == 25
        assert c[0]["f"] == 0.0
        assert abs(c[0]["g_3esiti"]) < 1e-15
        imax = max(range(25), key=lambda i: c[i]["g_3esiti"])
        assert abs(c[imax]["f"] - F3) < 0.03

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_curva"](PW, PM, PL, B, M, 0.50, 1)


class TestAnalisi:
    def _demo(self):
        return _F["mh362_analisi"](PW, PM, B, M, SEQ)

    def test_demo(self):
        a = self._demo()
        assert abs(a["f3"] - F3) < 1e-9
        assert abs(a["g3"] - G3) < 1e-12
        assert abs(a["fbin"] - FBIN) < 1e-12
        assert abs(a["gbin"] - GBIN) < 1e-12
        assert abs(a["finale3"] - FIN3) < 1e-9
        assert abs(a["finaleb"] - FINB) < 1e-9
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("BINARIO CONSERVATIVO")
        assert a["n"] == 20
        assert abs(a["p_l"] - PL) < 1e-15

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["finale3"] == a2["finale3"]
        assert a1["verdetto"] == a2["verdetto"]

    def test_prob_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_analisi"](0.70, 0.40, B, M, SEQ)

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh362_analisi"](PW, PM, B, M, "WX")
