"""Test tab357 'Kelly con lotti interi: sizing discreto e drag di arrotondamento': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh357_num", "mh357_parse_seq", "mh357_kelly_f",
           "mh357_lotti", "mh357_verdetto", "mh357_walk",
           "mh357_confronto")

TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
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
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
P = 0.5
EQUITY0 = 10000.0
LOTTO = 1000.0
FKELLY = 0.16666666666666666
LOTTI_INIT = 1
FEFF_INIT = 0.1
EQFIN = 14500.0
EQFIN_CONT = 15041.37952717448
DRAG = 541.3795271744802
DRAG_PCT = 0.03599267781232419
MAXDD = 0.42000000000000004
N = 20
NWINS = 10
VERDETTO = "LOTTO ECCESSIVO: il lotto da 1,000 mangia piu' di un quarto del Kelly (f_eff 10.00% vs f_kelly 16.67%): il drag di arrotondamento e' eccessivo, riduci il taglio."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry357:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert "tab357" in dvars
        assert "tab357" in withs

    def test_titoli_allineati_353_354_355_356_357(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab353")] == TITLE353
        assert titoli[dvars.index("tab354")] == TITLE354
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356
        assert titoli[dvars.index("tab357")] == TITLE357

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab374"
        assert titoli[-1] == TITLE374
        assert withs[-1] == "tab374"


class TestNum:
    def test_num_ok(self):
        assert _F["mh357_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh357_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh357_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_parse_seq"](123)


class TestKellyF:
    def test_demo(self):
        assert _F["mh357_kelly_f"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh357_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_kelly_f"](1.5, 1.5)


class TestLotti:
    def test_demo(self):
        assert _F["mh357_lotti"](1.0 / 6.0, 10000.0, 1000.0) == (1, 0.1)

    def test_zero_lotti(self):
        assert _F["mh357_lotti"](1.0 / 6.0, 500.0, 1000.0) == (0, 0.0)

    def test_floor_conservativo(self):
        n, f_eff = _F["mh357_lotti"](0.2, 1000.0, 150.0)
        assert n == 1
        assert f_eff == 0.15

    def test_f_eff_mai_sopra_kelly(self):
        for fk, eq, lo in ((0.2, 1000.0, 160.0),
                           (1.0 / 6.0, 10000.0, 700.0),
                           (0.4, 5000.0, 999.0),
                           (0.05, 2000.0, 10.0)):
            n, f_eff = _F["mh357_lotti"](fk, eq, lo)
            assert f_eff <= fk + 1e-12
            assert n * lo / eq == f_eff

    def test_fk_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_lotti"](-0.1, 10000.0, 1000.0)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_lotti"](0.2, 0.0, 1000.0)

    def test_lotto_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_lotti"](0.2, 1000.0, -5.0)


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh357_verdetto"](0.0, 10000.0, 1000.0)
        assert v.startswith("NESSUN EDGE")

    def test_nessun_edge_fk_negativo(self):
        v = _F["mh357_verdetto"](-0.1, 10000.0, 1000.0)
        assert v.startswith("NESSUN EDGE")

    def test_capitale_insufficiente(self):
        v = _F["mh357_verdetto"](1.0 / 6.0, 500.0, 1000.0)
        assert v.startswith("CAPITALE INSUFFICIENTE")

    def test_lotto_eccessivo(self):
        v = _F["mh357_verdetto"](1.0 / 6.0, 10000.0, 1000.0)
        assert v.startswith("LOTTO ECCESSIVO")

    def test_drag_moderato(self):
        v = _F["mh357_verdetto"](0.2, 1000.0, 160.0)
        assert v.startswith("DRAG MODERATO")

    def test_ok(self):
        v = _F["mh357_verdetto"](1.0 / 6.0, 10000.0, 500.0)
        assert v.startswith("ARROTONDAMENTO OK")

    def test_soglia_075_sotto_eccessivo(self):
        v = _F["mh357_verdetto"](0.2, 1000.0, 140.0)
        assert v.startswith("LOTTO ECCESSIVO")

    def test_soglia_075_sopra_moderato(self):
        v = _F["mh357_verdetto"](0.2, 1000.0, 160.0)
        assert v.startswith("DRAG MODERATO")

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_verdetto"](0.2, 0.0, 100.0)


class TestWalk:
    def _demo(self):
        return _F["mh357_confronto"](SEQ, B, P, EQUITY0, LOTTO)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["f_kelly"] == FKELLY == 1.0 / 6.0
        assert m["lotti_iniz"] == LOTTI_INIT == 1
        assert m["f_eff_iniz"] == FEFF_INIT == 0.10
        assert m["eq_fin"] == EQFIN == 14500.0
        assert abs(m["eqc_fin"] - EQFIN_CONT) < 1e-9
        assert abs(m["drag"] - DRAG) < 1e-9
        assert abs(m["drag_pct"] - DRAG_PCT) < 1e-12
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("LOTTO ECCESSIVO")
        assert m["equity0"] == EQUITY0 == 10000.0
        assert m["lotto"] == LOTTO == 1000.0

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eq_path"] == m2["eq_path"]
        assert m1["eqc_path"] == m2["eqc_path"]

    def test_equity_iniziale(self):
        m = self._demo()
        assert m["eq_path"][0] == EQUITY0
        assert m["eqc_path"][0] == EQUITY0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eq_path"]) == N + 1
        assert len(m["eqc_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_righe_progressive(self):
        m = self._demo()
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        for i, r in enumerate(m["righe"]):
            assert r["equity"] == m["eq_path"][i + 1]
            assert r["equity_cont"] == m["eqc_path"][i + 1]
            assert r["f_eff"] <= m["f_kelly"] + 1e-12
            assert r["lotti"] >= 0

    def test_drag_coerente(self):
        m = self._demo()
        assert m["drag"] == m["eqc_fin"] - m["eq_fin"]
        assert m["drag_pct"] == m["drag"] / m["eqc_fin"]

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"]("", B, P, EQUITY0, LOTTO)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"](SEQ, B, 1.5, EQUITY0, LOTTO)

    def test_equity_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"](SEQ, B, P, 0.0, LOTTO)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh357_confronto"](SEQ, B, P, EQUITY0, LOTTO)
        assert m["b"] == B
        assert m["p"] == P
        assert m["equity0"] == EQUITY0
        assert m["lotto"] == LOTTO

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"]("XYZ", B, P, EQUITY0, LOTTO)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"](SEQ, -1.0, P, EQUITY0, LOTTO)

    def test_lotto_ko(self):
        with pytest.raises(ValueError):
            _F["mh357_confronto"](SEQ, B, P, EQUITY0, 0.0)

