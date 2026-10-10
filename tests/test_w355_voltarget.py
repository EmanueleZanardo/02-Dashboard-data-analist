"""Test tab355 'Kelly con target di volatilità: sizing riscalato sulla vol': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh355_num", "mh355_parse_seq", "mh355_kelly_f", "mh355_fattore",
           "mh355_walk", "mh355_verdetto", "mh355_confronto")

TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
SEQ = 'WWWLWLWWLLLWWWLLWLLL'
B = 1.5
FKELLY = 0.15
SIGMA = 0.3
SIGTGT = 0.2
N = 20
NWINS = 10
EQFIN = 1.410598760621121
EQBASEFIN = 1.4981322191561401
MAXDD = 0.32093650000000007
FATTORE = 0.6666666666666667
FEFF = 0.1
VERDETTO = "VOL ELEVATA - RIDUZIONE: sigma 30.0% sopra il target 20.0%. Il fattore di scala e' 66.7%: la size effettiva scende a f=10.00% contro f_kelly=15.00%. Ridotto il rischio in regime di volatilita' alta."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry355:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 355
        assert "tab355" in dvars
        assert "tab355" in withs

    def test_titoli_allineati_351_352_353_354_355(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab351")] == TITLE351
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353
        assert titoli[dvars.index("tab354")] == TITLE354
        assert titoli[dvars.index("tab355")] == TITLE355

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab355"
        assert titoli[-1] == TITLE355
        assert withs[-1] == "tab355"


class TestNum:
    def test_num_ok(self):
        assert _F["mh355_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh355_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh355_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_parse_seq"](123)


class TestKellyF:
    def test_demo(self):
        assert abs(_F["mh355_kelly_f"](0.5, 1.5) - 1.0 / 6.0) < 1e-12

    def test_no_edge_zero(self):
        assert _F["mh355_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_kelly_f"](1.5, 1.5)


class TestFattore:
    def test_pari_uno(self):
        assert _F["mh355_fattore"](0.20, 0.20) == 1.0

    def test_riduzione(self):
        assert abs(_F["mh355_fattore"](0.30, 0.20) - 2.0 / 3.0) < 1e-15

    def test_aumento(self):
        assert abs(_F["mh355_fattore"](0.10, 0.20) - 2.0) < 1e-15

    def test_clamp_min(self):
        assert _F["mh355_fattore"](2.0, 0.20) == 0.25

    def test_clamp_max(self):
        assert _F["mh355_fattore"](0.05, 0.20) == 2.0

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_fattore"](0.0, 0.20)

    def test_target_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_fattore"](0.30, -0.01)

    def test_limiti_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_fattore"](0.30, 0.20, f_min=1.5, f_max=1.0)


class TestWalk:
    def _demo(self):
        return _F["mh355_confronto"](SEQ, B, FKELLY, SIGMA, SIGTGT)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 10
        assert abs(m["eq_fin"] - EQFIN) < 1e-9
        assert abs(m["eq_base_fin"] - EQBASEFIN) < 1e-9
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["fattore"] - FATTORE) < 1e-15
        assert abs(m["f_eff"] - FEFF) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("VOL ELEVATA - RIDUZIONE")

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["eq_path"] == m2["eq_path"]
        assert m1["base_path"] == m2["base_path"]

    def test_equity_iniziale_uno(self):
        m = self._demo()
        assert m["eq_path"][0] == 1.0
        assert m["base_path"][0] == 1.0

    def test_vol_alta_riduce_rischio(self):
        m = self._demo()
        assert m["f_eff"] < m["f_kelly"]
        assert m["max_dd"] >= 0.0

    def test_fattore_coerente(self):
        m = self._demo()
        assert abs(m["f_eff"] - FKELLY * FATTORE) < 1e-15
        assert abs(m["fattore"] - SIGTGT / SIGMA) < 1e-15

    def test_lunghezze(self):
        m = self._demo()
        assert len(m["eq_path"]) == N + 1
        assert len(m["base_path"]) == N + 1
        assert len(m["righe"]) == N

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh355_confronto"]("WLW", B, FKELLY, SIGMA, SIGTGT)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ

    def test_vol_bassa_aumento(self):
        m = _F["mh355_confronto"]("W" * 15, B, FKELLY, 0.10, 0.20)
        assert m["verdetto"].startswith("VOL BASSA - AUMENTO")
        assert m["f_eff"] == FKELLY * 2.0

    def test_neutra(self):
        m = _F["mh355_confronto"]("W" * 15, B, FKELLY, 0.20, 0.20)
        assert m["verdetto"].startswith("NEUTRA")
        assert m["f_eff"] == FKELLY

    def test_fkelly_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_confronto"](SEQ, B, -0.1, SIGMA, SIGTGT)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_confronto"](SEQ, B, FKELLY, 0.0, SIGTGT)


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh355_verdetto"](0.30, 0.20, 0.10, 0.15, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_vol_elevata(self):
        v = _F["mh355_verdetto"](0.30, 0.20, 0.10, 0.15, 20)
        assert v.startswith("VOL ELEVATA - RIDUZIONE")

    def test_vol_bassa(self):
        v = _F["mh355_verdetto"](0.10, 0.20, 0.30, 0.15, 20)
        assert v.startswith("VOL BASSA - AUMENTO")

    def test_neutra(self):
        v = _F["mh355_verdetto"](0.20, 0.20, 0.15, 0.15, 20)
        assert v.startswith("NEUTRA")

    def test_soglia_090_vol_elevata(self):
        v = _F["mh355_verdetto"](0.30, 0.20, 0.134, 0.15, 20)
        assert v.startswith("VOL ELEVATA - RIDUZIONE")

    def test_soglia_110_vol_bassa(self):
        v = _F["mh355_verdetto"](0.10, 0.20, 0.165, 0.15, 20)
        assert v.startswith("VOL BASSA - AUMENTO")

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_verdetto"](0.0, 0.20, 0.10, 0.15, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_verdetto"](0.30, 0.20, 0.10, 0.15, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh355_confronto"](SEQ, B, FKELLY, SIGMA, SIGTGT)
        assert m["b"] == B
        assert m["f_kelly"] == FKELLY
        assert m["sigma"] == SIGMA
        assert m["sigma_target"] == SIGTGT
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_confronto"]("XYZ", B, FKELLY, SIGMA, SIGTGT)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh355_confronto"](SEQ, -1.0, FKELLY, SIGMA, SIGTGT)

    def test_righe(self):
        m = _F["mh355_confronto"](SEQ, B, FKELLY, SIGMA, SIGTGT)
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        for i, r in enumerate(m["righe"]):
            assert r["equity"] == m["eq_path"][i + 1]
            assert r["equity_base"] == m["base_path"][i + 1]
            assert r["f_effettiva"] == m["f_eff"]

