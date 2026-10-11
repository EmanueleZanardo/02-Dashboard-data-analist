"""Test tab358 'Kelly con stop-loss: sizing con perdita troncata': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh358_num", "mh358_parse_seq", "mh358_kelly_stop",
           "mh358_kelly_base", "mh358_verdetto", "mh358_walk",
           "mh358_confronto")

TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
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
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
S = 0.5
EQUITY0 = 10000.0
FSTOP = 0.6666666666666666
FBASE = 0.16666666666666666
BOOST = 4.0
EQSFIN = 177577.26633812618
EQBFIN = 15041.37952717448
GAP = 162535.8868109517
GAP_PCT = 10.805916207174118
MAXDD = 0.736625514403292
N = 20
NWINS = 10
VERDETTO = 'BOOST FORTE: lo stop al 50% porta il Kelly a 66.67%. (4.0x il Kelly base 16.67%). Verifica che lo stop sia eseguibile: slippage e gap possono allargare la perdita reale oltre il livello dichiarato.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry358:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 375
        assert "tab358" in dvars
        assert "tab358" in withs

    def test_titoli_allineati_354_355_356_357_358(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab354")] == TITLE354
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab375"
        assert titoli[-1] == TITLE375
        assert withs[-1] == "tab375"


class TestNum:
    def test_num_ok(self):
        assert _F["mh358_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh358_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh358_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_parse_seq"](123)


class TestKellyStop:
    def test_demo(self):
        assert _F["mh358_kelly_stop"](0.5, 1.5, 0.5) == 2.0 / 3.0

    def test_no_edge_zero(self):
        assert _F["mh358_kelly_stop"](0.2, 1.5, 0.5) == 0.0

    def test_stop_crea_edge(self):
        # senza stop f* sarebbe 0, con stop s=0.3 c'e' edge
        assert _F["mh358_kelly_stop"](0.3, 1.5, 0.3) == pytest.approx(
            0.24 / 0.45)

    def test_mai_negativo(self):
        assert _F["mh358_kelly_stop"](0.1, 1.5, 0.5) == 0.0

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_kelly_stop"](0.5, 1.5, 0.0)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_kelly_stop"](0.5, 0.0, 0.5)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_kelly_stop"](1.5, 1.5, 0.5)


class TestKellyBase:
    def test_demo(self):
        assert _F["mh358_kelly_base"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh358_kelly_base"](0.2, 1.5) == 0.0

    def test_sempre_sotto_stop(self):
        for p, b, s in ((0.5, 1.5, 0.5), (0.6, 2.0, 0.3),
                        (0.4, 1.2, 0.8), (0.7, 1.5, 0.2)):
            fs = _F["mh358_kelly_stop"](p, b, s)
            fb = _F["mh358_kelly_base"](p, b)
            if (p * b - (1.0 - p) * s) > 0:
                assert fs >= fb


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh358_verdetto"](0.2, 1.5, 0.5)
        assert v.startswith("NESSUN EDGE")

    def test_stop_inutile(self):
        v = _F["mh358_verdetto"](0.5, 1.5, 1.2)
        assert v.startswith("STOP INUTILE")

    def test_sizing_estremo(self):
        v = _F["mh358_verdetto"](0.7, 1.5, 0.2)
        assert v.startswith("SIZING ESTREMO")

    def test_boost_forte(self):
        v = _F["mh358_verdetto"](0.5, 1.5, 0.5)
        assert v.startswith("BOOST FORTE")

    def test_boost_forte_stop_crea_edge(self):
        v = _F["mh358_verdetto"](0.3, 1.5, 0.3)
        assert v.startswith("BOOST FORTE")
        assert "CREA" in v

    def test_boost_moderato(self):
        v = _F["mh358_verdetto"](0.5, 1.5, 0.8)
        assert v.startswith("BOOST MODERATO")

    def test_soglia_boost_25(self):
        # m = 4.0 -> FORTE; m = 1.75 -> MODERATO
        assert _F["mh358_verdetto"](0.5, 1.5, 0.5).startswith("BOOST FORTE")
        assert _F["mh358_verdetto"](0.5, 1.5, 0.8).startswith(
            "BOOST MODERATO")

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_verdetto"](0.5, 1.5, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_verdetto"](2.0, 1.5, 0.5)


class TestWalk:
    def _demo(self):
        return _F["mh358_confronto"](SEQ, B, P, S, EQUITY0)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_stop"] == FSTOP == 2.0 / 3.0
        assert m["f_base"] == FBASE == 1.0 / 6.0
        assert m["boost"] == BOOST == 4.0
        assert abs(m["eqs_fin"] - EQSFIN) < 1e-9
        assert abs(m["eqb_fin"] - EQBFIN) < 1e-9
        assert abs(m["gap"] - GAP) < 1e-9
        assert abs(m["gap_pct"] - GAP_PCT) < 1e-12
        assert abs(m["max_dd_stop"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("BOOST FORTE")
        assert m["s"] == S == 0.5
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
            assert r["eq_stop"] == m["eqs_path"][i + 1]
            assert r["eq_base"] == m["eqb_path"][i + 1]

    def test_gap_coerente(self):
        m = self._demo()
        assert m["gap"] == m["eqs_fin"] - m["eqb_fin"]
        assert m["gap_pct"] == m["gap"] / m["eqb_fin"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"]("", B, P, S, EQUITY0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"](SEQ, B, 1.5, S, EQUITY0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"](SEQ, B, P, S, 0.0)

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"](SEQ, B, P, -0.5, EQUITY0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh358_confronto"](SEQ, B, P, S, EQUITY0)
        assert m["b"] == B
        assert m["p"] == P
        assert m["s"] == S
        assert m["equity0"] == EQUITY0

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"]("XYZ", B, P, S, EQUITY0)

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh358_confronto"](SEQ, B, P, 0.0, EQUITY0)

