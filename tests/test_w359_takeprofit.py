"""Test tab359 'Kelly con take-profit: sizing con vincita troncata': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh359_num", "mh359_parse_seq", "mh359_kelly_tp",
           "mh359_kelly_base", "mh359_verdetto", "mh359_walk",
           "mh359_confronto")

TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
T = 1.1
EQUITY0 = 10000.0
FTP = 0.04545454545454549
FBASE = 0.16666666666666666
RATIO = 0.272727272727273
EQSFIN = 10229.611250772074
EQBFIN = 15041.37952717448
GAP = -4811.768276402407
GAP_PCT = -0.31990205869808913
MAXDD = 0.16790604179731916
N = 20
NWINS = 10
VERDETTO = "TAGLIO FORTE: il take-profit a 1.10x dimezza il Kelly (da 16.67% a 4.55%, rapporto 0.27x): il TP mangia buona parte dell'edge. O accetti un sizing molto prudente, o allenti il take-profit per lasciare correre di piu' i profitti."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry359:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 375
        assert "tab359" in dvars
        assert "tab359" in withs

    def test_titoli_allineati_355_356_357_358_359(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab375"
        assert titoli[-1] == TITLE375
        assert withs[-1] == "tab375"


class TestNum:
    def test_num_ok(self):
        assert _F["mh359_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh359_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh359_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_parse_seq"](123)


class TestKellyTp:
    def test_demo(self):
        assert _F["mh359_kelly_tp"](0.5, 1.1) == pytest.approx(0.05 / 1.1)

    def test_no_edge_zero(self):
        assert _F["mh359_kelly_tp"](0.2, 1.1) == 0.0

    def test_mai_negativo(self):
        assert _F["mh359_kelly_tp"](0.1, 1.1) == 0.0

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_kelly_tp"](0.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_kelly_tp"](1.5, 1.1)


class TestKellyBase:
    def test_demo(self):
        assert _F["mh359_kelly_base"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh359_kelly_base"](0.2, 1.5) == 0.0

    def test_sempre_sopra_tp(self):
        for p, b, t in ((0.5, 1.5, 1.1), (0.6, 2.0, 1.3),
                        (0.7, 1.5, 1.2), (0.55, 1.8, 1.4)):
            ft = _F["mh359_kelly_tp"](p, t)
            fb = _F["mh359_kelly_base"](p, b)
            if (p * t - (1.0 - p)) > 0:
                assert fb >= ft


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh359_verdetto"](0.2, 1.5, 1.1)
        assert v.startswith("NESSUN EDGE")

    def test_tp_inutile(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.5)
        assert v.startswith("TP INUTILE")

    def test_taglio_forte(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.1)
        assert v.startswith("TAGLIO FORTE")

    def test_taglio_moderato(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.3)
        assert v.startswith("TAGLIO MODERATO")

    def test_taglio_leggero(self):
        v = _F["mh359_verdetto"](0.5, 1.5, 1.45)
        assert v.startswith("TAGLIO LEGGERO")

    def test_soglie_05_09(self):
        # r = 0.2727 -> FORTE; r = 0.6923 -> MODERATO; r = 0.9310 -> LEGGERO
        assert _F["mh359_verdetto"](0.5, 1.5, 1.1).startswith("TAGLIO FORTE")
        assert _F["mh359_verdetto"](0.5, 1.5, 1.3).startswith(
            "TAGLIO MODERATO")
        assert _F["mh359_verdetto"](0.5, 1.5, 1.45).startswith(
            "TAGLIO LEGGERO")

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_verdetto"](0.5, 1.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_verdetto"](2.0, 1.5, 1.1)


class TestWalk:
    def _demo(self):
        return _F["mh359_confronto"](SEQ, B, P, T, EQUITY0)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_tp"] == FTP == pytest.approx(0.05 / 1.1)
        assert m["f_base"] == FBASE == 1.0 / 6.0
        assert m["ratio"] == RATIO == pytest.approx(
            (0.05 / 1.1) / (1.0 / 6.0))
        assert abs(m["eqs_fin"] - EQSFIN) < 1e-9
        assert abs(m["eqb_fin"] - EQBFIN) < 1e-9
        assert abs(m["gap"] - GAP) < 1e-9
        assert abs(m["gap_pct"] - GAP_PCT) < 1e-12
        assert abs(m["max_dd_tp"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("TAGLIO FORTE")
        assert m["t"] == T == 1.1
        assert m["equity0"] == EQUITY0 == 10000.0

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eqs_path"] == m2["eqs_path"]
        assert m1["eqb_path"] == m2["eqb_path"]

    def test_equity_iniziale(self):
        m = self._demo()
        assert m["eqs_path"][0] == EQUITY0
        assert m["eqb_path"][0] == EQUITY0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eqs_path"]) == N + 1
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
            assert r["eq_tp"] == m["eqs_path"][i + 1]
            assert r["eq_base"] == m["eqb_path"][i + 1]

    def test_gap_coerente(self):
        m = self._demo()
        assert m["gap"] == m["eqs_fin"] - m["eqb_fin"]
        assert m["gap_pct"] == m["gap"] / m["eqb_fin"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"]("", B, P, T, EQUITY0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, 1.5, T, EQUITY0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, T, 0.0)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, -0.5, EQUITY0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh359_confronto"](SEQ, B, P, T, EQUITY0)
        assert m["b"] == B
        assert m["p"] == P
        assert m["t"] == T
        assert m["equity0"] == EQUITY0

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"]("XYZ", B, P, T, EQUITY0)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh359_confronto"](SEQ, B, P, 0.0, EQUITY0)

