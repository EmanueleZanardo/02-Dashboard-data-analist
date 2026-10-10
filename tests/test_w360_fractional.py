"""Test tab360 'Kelly frazionario (fractional Kelly): λ·f*': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh360_num", "mh360_parse_seq", "mh360_kelly",
           "mh360_verdetto", "mh360_walk", "mh360_confronto")

TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
LAM = 0.5
EQUITY0 = 10000.0
FEFF = 0.08333333333333333
FFULL = 0.16666666666666666
EQFFIN = 13603.154027780993
EQBFIN = 15041.37952717448
GAP = -1438.2254993934876
GAP_PCT = -0.09561792499119647
GF = 0.015504800579495104
GB = 0.0206207261596576
MDDF = 0.2718686704282409
MDDB = 0.4976530349794238
N = 20
NWINS = 10
VERDETTO = "HALF-KELLY: λ = 0.50 e' il compromesso classico: circa il 75% della crescita attesa del Kelly pieno con circa meta' del drawdown e della volatilita'. La scelta standard quando le stime di win-rate e payoff sono incerte."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry360:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 362
        assert "tab360" in dvars
        assert "tab360" in withs

    def test_titoli_allineati_356_357_358_359_360(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab362"
        assert titoli[-1] == TITLE362
        assert withs[-1] == "tab362"


class TestNum:
    def test_num_ok(self):
        assert _F["mh360_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh360_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh360_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_parse_seq"](123)


class TestKelly:
    def test_demo(self):
        assert _F["mh360_kelly"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh360_kelly"](0.2, 1.5) == 0.0

    def test_mai_negativo(self):
        assert _F["mh360_kelly"](0.1, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_kelly"](0.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_kelly"](1.5, 1.5)


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh360_verdetto"](0.2, 1.5, 0.5)
        assert v.startswith("NESSUN EDGE")

    def test_leva(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 1.5)
        assert v.startswith("LEVA")

    def test_full_kelly(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 1.0)
        assert v.startswith("FULL-KELLY")

    def test_half_kelly(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 0.5)
        assert v.startswith("HALF-KELLY")

    def test_frazione_prudente(self):
        v = _F["mh360_verdetto"](0.5, 1.5, 0.3)
        assert v.startswith("FRAZIONE PRUDENTE")

    def test_soglie(self):
        # 0.95 -> FULL-KELLY; 0.45 -> HALF-KELLY; 0.44 -> PRUDENTE; 1.01 -> LEVA
        assert _F["mh360_verdetto"](0.5, 1.5, 0.95).startswith("FULL-KELLY")
        assert _F["mh360_verdetto"](0.5, 1.5, 0.45).startswith("HALF-KELLY")
        assert _F["mh360_verdetto"](0.5, 1.5, 0.44).startswith(
            "FRAZIONE PRUDENTE")
        assert _F["mh360_verdetto"](0.5, 1.5, 1.01).startswith("LEVA")

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_verdetto"](0.5, 1.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_verdetto"](2.0, 1.5, 0.5)


class TestWalk:
    def _demo(self):
        return _F["mh360_confronto"](SEQ, B, P, LAM, EQUITY0)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_eff"] == FEFF == 1.0 / 12.0
        assert m["f_full"] == FFULL == 1.0 / 6.0
        assert m["lam"] == LAM == 0.5
        assert abs(m["eqf_fin"] - EQFFIN) < 1e-9
        assert abs(m["eqb_fin"] - EQBFIN) < 1e-9
        assert abs(m["gap"] - GAP) < 1e-9
        assert abs(m["gap_pct"] - GAP_PCT) < 1e-12
        assert abs(m["growth_frac"] - GF) < 1e-12
        assert abs(m["growth_full"] - GB) < 1e-12
        assert abs(m["max_dd_frac"] - MDDF) < 1e-12
        assert abs(m["max_dd_full"] - MDDB) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("HALF-KELLY")
        assert m["equity0"] == EQUITY0 == 10000.0

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eqf_path"] == m2["eqf_path"]
        assert m1["eqb_path"] == m2["eqb_path"]

    def test_equity_iniziale(self):
        m = self._demo()
        assert m["eqf_path"][0] == EQUITY0
        assert m["eqb_path"][0] == EQUITY0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eqf_path"]) == N + 1
        assert len(m["eqb_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_righe_coerenti(self):
        m = self._demo()
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        for i, r in enumerate(m["righe"]):
            assert r["eq_frac"] == m["eqf_path"][i + 1]
            assert r["eq_full"] == m["eqb_path"][i + 1]

    def test_gap_coerente(self):
        m = self._demo()
        assert m["gap"] == m["eqf_fin"] - m["eqb_fin"]
        assert m["gap_pct"] == m["gap"] / m["eqb_fin"]

    def test_frazionario_cresce_meno(self):
        m = self._demo()
        assert m["growth_frac"] < m["growth_full"]

    def test_frazionario_drawdown_minore(self):
        m = self._demo()
        assert m["max_dd_frac"] < m["max_dd_full"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"]("", B, P, LAM, EQUITY0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, 1.5, LAM, EQUITY0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, LAM, 0.0)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, -0.5, EQUITY0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh360_confronto"](SEQ, B, P, LAM, EQUITY0)
        assert m["b"] == B
        assert m["p"] == P
        assert m["lam"] == LAM
        assert m["equity0"] == EQUITY0

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"]("XYZ", B, P, LAM, EQUITY0)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh360_confronto"](SEQ, B, P, 0.0, EQUITY0)

