"""Test tab354 'Kelly con controllo drawdown: sizing frazionato al drawdown': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh354_num", "mh354_parse_seq", "mh354_kelly_f", "mh354_fattore",
           "mh354_walk", "mh354_verdetto", "mh354_confronto")

TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
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
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE350 = "Kelly robusto: sizing con edge incerta"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
FKELLY = 0.15
DDMAX = 0.25
N = 20
NWINS = 10
EQFIN = 1.3932856206831181
DDFIN = 0.24206512827376742
MAXDD = 0.24206512827376742
FFIN = 0.008796925329063043
FATTORE = 0.031739486904930336
VERDETTO = "RIDUZIONE SEVERA: drawdown 24.2% oltre i 2/3 della soglia 25%. La size effettiva e' f=0.88% contro f_kelly=15.00% (fattore 5.9%). Riduci drasticamente l'esposizione."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry354:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 367
        assert "tab354" in dvars
        assert "tab354" in withs

    def test_titoli_allineati_350_351_352_353_354(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab350")] == TITLE350
        assert titoli[dvars.index("tab351")] == TITLE351
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353
        assert titoli[dvars.index("tab354")] == TITLE354

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab367"
        assert titoli[-1] == TITLE367
        assert withs[-1] == "tab367"


class TestNum:
    def test_num_ok(self):
        assert _F["mh354_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh354_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh354_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_parse_seq"](123)


class TestKellyF:
    def test_demo(self):
        assert abs(_F["mh354_kelly_f"](0.5, 1.5) - 1.0 / 6.0) < 1e-12

    def test_no_edge_zero(self):
        assert _F["mh354_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_kelly_f"](1.5, 1.5)


class TestFattore:
    def test_dd_zero_uno(self):
        assert _F["mh354_fattore"](0.0, 0.25) == 1.0

    def test_meta(self):
        assert abs(_F["mh354_fattore"](0.125, 0.25) - 0.5) < 1e-15

    def test_soglia_zero(self):
        assert _F["mh354_fattore"](0.25, 0.25) == 0.0

    def test_oltre_soglia_zero(self):
        assert _F["mh354_fattore"](0.40, 0.25) == 0.0

    def test_dd_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_fattore"](-0.01, 0.25)

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_fattore"](0.10, 0.0)
        with pytest.raises(ValueError):
            _F["mh354_fattore"](0.10, 1.0)


class TestWalk:
    def _demo(self):
        return _F["mh354_confronto"](SEQ, B, FKELLY, DDMAX)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert abs(m["eq_fin"] - EQFIN) < 1e-9
        assert abs(m["dd_fin"] - DDFIN) < 1e-12
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["f_fin"] - FFIN) < 1e-12
        assert abs(m["fattore_fin"] - FATTORE) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("RIDUZIONE SEVERA")

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eq_path"] == m2["eq_path"]
        assert m1["dd_path"] == m2["dd_path"]
        assert m1["f_path"] == m2["f_path"]

    def test_equity_iniziale_uno(self):
        m = self._demo()
        assert m["eq_path"][0] == 1.0
        assert m["dd_path"][0] == 0.0

    def test_fattore_limitato(self):
        m = self._demo()
        for dd, f in zip(m["dd_path"], m["f_path"]):
            assert 0.0 <= f <= FKELLY + 1e-15
            assert abs(f - FKELLY * _F["mh354_fattore"](dd, DDMAX)) < 1e-15

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eq_path"]) == N + 1
        assert len(m["dd_path"]) == N + 1
        assert len(m["f_path"]) == N
        assert len(m["righe"]) == N

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh354_confronto"]("WLW", B, FKELLY, DDMAX)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_vincite_tutte_size_piena(self):
        m = _F["mh354_confronto"]("W" * 15, B, FKELLY, DDMAX)
        assert m["verdetto"].startswith("SIZE PIENA")
        assert m["dd_fin"] == 0.0

    def test_fkelly_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_confronto"](SEQ, B, -0.1, DDMAX)

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_confronto"](SEQ, B, FKELLY, 0.0)


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh354_verdetto"](0.10, 0.25, 0.10, 0.15, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_stop(self):
        v = _F["mh354_verdetto"](0.25, 0.25, 0.0, 0.15, 20)
        assert v.startswith("STOP")

    def test_riduzione_severa(self):
        v = _F["mh354_verdetto"](0.242, 0.25, 0.009, 0.15, 20)
        assert v.startswith("RIDUZIONE SEVERA")

    def test_riduzione(self):
        v = _F["mh354_verdetto"](0.10, 0.25, 0.09, 0.15, 20)
        assert v.startswith("RIDUZIONE")

    def test_size_piena(self):
        v = _F["mh354_verdetto"](0.05, 0.25, 0.12, 0.15, 20)
        assert v.startswith("SIZE PIENA")

    def test_dd_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_verdetto"](-0.1, 0.25, 0.1, 0.15, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_verdetto"](0.1, 0.25, 0.1, 0.15, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh354_confronto"](SEQ, B, FKELLY, DDMAX)
        assert m["b"] == B
        assert m["f_kelly"] == FKELLY
        assert m["dd_max"] == DDMAX
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_confronto"]("XYZ", B, FKELLY, DDMAX)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh354_confronto"](SEQ, -1.0, FKELLY, DDMAX)

    def test_righe(self):
        m = _F["mh354_confronto"](SEQ, B, FKELLY, DDMAX)
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ

