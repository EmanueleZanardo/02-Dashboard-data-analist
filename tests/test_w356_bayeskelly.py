"""Test tab356 'Kelly bayesiano: sizing con win-rate posterior': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh356_num", "mh356_parse_seq", "mh356_kelly_f",
           "mh356_posterior", "mh356_beta_reg", "mh356_p_quantile",
           "mh356_edge_prob", "mh356_verdetto", "mh356_walk",
           "mh356_confronto")

TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
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
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
ALPHA = 2.0
BETA = 2.0
APOST = 12.0
BPOST = 12.0
PMEAN = 0.5
PQUANT05 = 0.3351476474715449
EDGEPROB = 0.8363565593601016
PEST = 0.5
F = 0.16666666666666666
EQFIN = 0.5832514684465875
MAXDD = 0.8133595300970919
N = 20
NWINS = 10
VERDETTO = "EDGE MARGINALE: la posterior da' 83.6% di probabilita' che il vero win-rate batta il break-even. Considera la modalita' prudente (quantile 5%)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry356:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 375
        assert "tab356" in dvars
        assert "tab356" in withs

    def test_titoli_allineati_352_353_354_355_356(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353
        assert titoli[dvars.index("tab354")] == TITLE354
        assert titoli[dvars.index("tab355")] == TITLE355
        assert titoli[dvars.index("tab356")] == TITLE356

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab375"
        assert titoli[-1] == TITLE375
        assert withs[-1] == "tab375"


class TestNum:
    def test_num_ok(self):
        assert _F["mh356_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh356_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh356_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_parse_seq"](123)


class TestBetaReg:
    def test_uniforme(self):
        assert abs(_F["mh356_beta_reg"](1, 1, 0.3) - 0.3) < 1e-9

    def test_quadrato(self):
        assert abs(_F["mh356_beta_reg"](2, 1, 0.5) - 0.25) < 1e-9

    def test_complemento(self):
        assert abs(_F["mh356_beta_reg"](1, 2, 0.5) - 0.75) < 1e-9

    def test_simmetria(self):
        assert abs(_F["mh356_beta_reg"](12, 12, 0.5) - 0.5) < 1e-9

    def test_bordi(self):
        assert _F["mh356_beta_reg"](3, 4, 0.0) == 0.0
        assert _F["mh356_beta_reg"](3, 4, 1.0) == 1.0

    def test_a_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_beta_reg"](0, 1, 0.5)

    def test_x_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_beta_reg"](1, 1, 1.5)


class TestQuantile:
    def test_radice(self):
        assert abs(_F["mh356_p_quantile"](2, 1, 0.25) - 0.5) < 1e-9

    def test_complemento(self):
        assert abs(_F["mh356_p_quantile"](1, 2, 0.75) - 0.5) < 1e-9

    def test_uniforme(self):
        assert abs(_F["mh356_p_quantile"](1, 1, 0.05) - 0.05) < 1e-9

    def test_mediana_simmetrica(self):
        assert abs(_F["mh356_p_quantile"](12, 12, 0.5) - 0.5) < 1e-7

    def test_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_p_quantile"](2, 2, 1.5)

    def test_a_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_p_quantile"](0, 2, 0.5)


class TestKellyF:
    def test_demo(self):
        assert _F["mh356_kelly_f"](0.5, 1.5) == 1.0 / 6.0

    def test_no_edge_zero(self):
        assert _F["mh356_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_kelly_f"](1.5, 1.5)


class TestPosterior:
    def test_demo(self):
        assert _F["mh356_posterior"](2.0, 2.0, (1, 1, 0)) == (4.0, 3.0)

    def test_vuota(self):
        assert _F["mh356_posterior"](2.0, 2.0, ()) == (2.0, 2.0)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_posterior"](0.0, 2.0, (1,))


class TestEdgeProb:
    def test_demo(self):
        assert abs(_F["mh356_edge_prob"](12.0, 12.0, 1.5)
                   - EDGEPROB) < 1e-9

    def test_simmetria(self):
        assert abs(_F["mh356_edge_prob"](12.0, 12.0, 1.0) - 0.5) < 1e-9

    def test_monotonia_b(self):
        assert (_F["mh356_edge_prob"](12.0, 12.0, 2.0)
                > _F["mh356_edge_prob"](12.0, 12.0, 1.5))

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_edge_prob"](12.0, 12.0, 0.0)


class TestWalk:
    def _demo(self):
        return _F["mh356_confronto"](SEQ, B, ALPHA, BETA)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert m["a_post"] == APOST == 12.0
        assert m["b_post"] == BPOST == 12.0
        assert m["p_mean"] == PMEAN == 0.5
        assert abs(m["p_quant05"] - PQUANT05) < 1e-9
        assert abs(m["edge_prob"] - EDGEPROB) < 1e-9
        assert m["p_est"] == PEST == 0.5
        assert abs(m["f"] - F) < 1e-12
        assert abs(m["eq_fin"] - EQFIN) < 1e-9
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("EDGE MARGINALE")
        assert m["p_be"] == 0.4

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eq_path"] == m2["eq_path"]
        assert m1["p_est"] == m2["p_est"]

    def test_equity_iniziale_uno(self):
        m = self._demo()
        assert m["eq_path"][0] == 1.0

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eq_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_prudente_taglia_size(self):
        m = _F["mh356_confronto"](SEQ, B, ALPHA, BETA, "prudente")
        assert m["p_est"] == m["p_quant05"]
        assert m["f"] == 0.0
        assert m["verdetto"] == VERDETTO

    def test_righe_progressive(self):
        m = self._demo()
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        assert m["righe"][-1]["a"] == APOST
        assert m["righe"][-1]["b"] == BPOST
        for i, r in enumerate(m["righe"]):
            assert r["equity"] == m["eq_path"][i + 1]

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh356_confronto"]("WLW", B, ALPHA, BETA)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_modo_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, B, ALPHA, BETA, "strano")

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"]("XYZ", B, ALPHA, BETA)


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh356_verdetto"](0.99, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_marginale(self):
        v = _F["mh356_verdetto"](0.84, 20)
        assert v.startswith("EDGE MARGINALE")

    def test_attendibile(self):
        v = _F["mh356_verdetto"](0.95, 20)
        assert v.startswith("EDGE ATTENDIBILE")

    def test_non_attendibile(self):
        v = _F["mh356_verdetto"](0.49, 20)
        assert v.startswith("EDGE NON ATTENDIBILE")

    def test_soglia_090_attendibile(self):
        v = _F["mh356_verdetto"](0.91, 20)
        assert v.startswith("EDGE ATTENDIBILE")

    def test_soglia_050_marginale(self):
        v = _F["mh356_verdetto"](0.51, 20)
        assert v.startswith("EDGE MARGINALE")

    def test_ep_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_verdetto"](1.5, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_verdetto"](0.9, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh356_confronto"](SEQ, B, ALPHA, BETA)
        assert m["b"] == B
        assert m["alpha"] == ALPHA
        assert m["beta"] == BETA
        assert m["modo"] == "media"
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"]("XYZ", B, ALPHA, BETA)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, -1.0, ALPHA, BETA)

    def test_prior_ko(self):
        with pytest.raises(ValueError):
            _F["mh356_confronto"](SEQ, B, 0.0, BETA)

