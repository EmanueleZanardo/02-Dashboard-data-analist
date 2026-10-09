
"""Test tab338 '⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dell'M² di Modigliani: validatori,
parse delle due serie di rendimenti %, misure (exp_ann, bm_ann, rf_ann, sd_s,
sd_b, scala, m2, delta, vol_s_ann, vol_b_ann; risk-free parametrizzabile) e
verdetto a 4 stati (ECCELLENTE / BUONO / MODERATO / DEBOLE + NON MISURABILE),
con note su leva implicita (de-levata/levata/rischio simile).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh338_num", "mh338_parse_serie", "mh338_misure", "mh338_verdetto")

TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
SERIE_ST_DEMO = '1.43\n0.02\n2.44\n2.61\n-1.28\n-0.76\n0.81\n0.2\n0.73\n-0.03\n2.45\n2.47\n1.51\n2.61\n1.46\n-0.45\n1.07\n-0.45\n2.17\n1.28\n1.26\n0.56\n2.72\n0.67\n0.1\n0.15\n1.45\n1.52\n1.86\n2.03\n4.13\n0.65\n0.22\n-0.4\n1.38\n2.2'
SERIE_BM_DEMO = '0.94\n-0.54\n1.43\n1.63\n-1.55\n-0.83\n0.74\n0.25\n0.58\n-0.34\n1.57\n1.46\n0.67\n1.84\n1.11\n-0.35\n1.01\n-0.45\n1.57\n0.55\n0.4\n-0.15\n1.94\n0.43\n0.13\n0.21\n1.19\n1.0\n1.05\n1.07\n2.96\n0.15\n0.04\n-0.3\n1.28\n1.84'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ANN = 13.596666666666668
BM_ANN = 8.176666666666666
RF_ANN = 0.0
SD_S = 1.1888837969035
SD_B = 0.9234536194642302
SCALA = 0.7767400160296621
M2 = 10.56107508461664
DELTA = 2.384408417949974
VOL_S_ANN = 4.118414281064521
VOL_B_ANN = 3.1989371746908453
STATO = "M² Modigliani BUONO"
VERDETTO = "M² Modigliani BUONO (Δ +2.38 pp/anno): a parita' di rischio col benchmark la strategia rende di piu' (M² 10.56 pp/anno vs benchmark 8.18). C'e' valore aggiunto oltre il rischio corso. La strategia e' piu' rischiosa del benchmark (scala 0.78 < 1): nel M² viene de-levata, il rendimento grezzo va letto con cautela."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh338_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh338_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry338:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 339
        assert "tab338" in dvars
        assert "tab338" in withs

    def test_titoli_allineati_335_336_337_338(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab335")] == TITLE335
        assert titoli[dvars.index("tab336")] == TITLE336
        assert titoli[dvars.index("tab337")] == TITLE337
        assert titoli[dvars.index("tab338")] == TITLE338

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab339"
        assert titoli[-1] == TITLE339
        assert withs[-1] == "tab339"


class TestNum:
    def test_num_ok(self):
        assert _F["mh338_num"](1.5, "x") == 1.5
        assert _F["mh338_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh338_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh338_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.43)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh338_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestMisure:
    def test_demo(self):
        rs, rb = _demo()
        m = _F["mh338_misure"](rs, rb)
        assert m["n"] == N_PER == 36
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["bm_ann"] == pytest.approx(BM_ANN, rel=1e-9)
        assert m["rf_ann"] == pytest.approx(RF_ANN, rel=1e-9)
        assert m["sd_s"] == pytest.approx(SD_S, rel=1e-9)
        assert m["sd_b"] == pytest.approx(SD_B, rel=1e-9)
        assert m["scala"] == pytest.approx(SCALA, rel=1e-9)
        assert m["m2"] == pytest.approx(M2, rel=1e-9)
        assert m["delta"] == pytest.approx(DELTA, rel=1e-9)
        assert m["vol_s_ann"] == pytest.approx(VOL_S_ANN, rel=1e-9)
        assert m["vol_b_ann"] == pytest.approx(VOL_B_ANN, rel=1e-9)
        assert m["vol_s_ann"] > m["vol_b_ann"] > 0

    def test_relazioni(self):
        rs, rb = _demo()
        m = _F["mh338_misure"](rs, rb)
        assert m["scala"] == pytest.approx(m["sd_b"] / m["sd_s"], rel=1e-9)
        assert m["m2"] == pytest.approx(
            m["rf_ann"] + m["scala"] * (m["exp_ann"] - m["rf_ann"]), rel=1e-9)
        assert m["delta"] == pytest.approx(m["m2"] - m["bm_ann"], rel=1e-9)
        assert m["vol_s_ann"] == pytest.approx(m["sd_s"] * (12 ** 0.5),
                                               rel=1e-9)

    def test_riskfree_sposta_base(self):
        rs, rb = _demo()
        m0 = _F["mh338_misure"](rs, rb, 12, 0.0)
        m1 = _F["mh338_misure"](rs, rb, 12, 1.0)
        assert m1["rf_ann"] == pytest.approx(12.0, rel=1e-9)
        assert m1["m2"] == pytest.approx(
            12.0 + m0["scala"] * (m0["exp_ann"] - 12.0), rel=1e-9)
        assert m1["delta"] == pytest.approx(m1["m2"] - m0["bm_ann"], rel=1e-9)

    def test_ko_benchmark_piatto(self):
        rs = np.arange(36, dtype=float)
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, np.ones(36))

    def test_ko_strategia_piatta(self):
        with pytest.raises(ValueError):
            _F["mh338_misure"](np.ones(36), np.arange(36, dtype=float))

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh338_misure"](np.ones(11), np.ones(11))

    def test_ko_periodi_annuo(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb, 0)
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb, -4)


class TestVerdetto:
    def test_verdetto_buono_demo(self):
        v = _F["mh338_verdetto"](2.38, 0.777, 10.56, 8.18)
        assert v.startswith("M² Modigliani BUONO")
        assert "de-levata" in v

    def test_verdetto_soglia_3(self):
        v = _F["mh338_verdetto"](3.0, 1.0, 12.0, 9.0)
        assert v.startswith("M² Modigliani ECCELLENTE")

    def test_verdetto_soglia_1(self):
        v = _F["mh338_verdetto"](1.0, 1.0, 10.0, 9.0)
        assert v.startswith("M² Modigliani BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh338_verdetto"](0.5, 1.0, 9.5, 9.0)
        assert v.startswith("M² Modigliani MODERATO")

    def test_verdetto_soglia_0(self):
        v = _F["mh338_verdetto"](0.0, 1.0, 9.0, 9.0)
        assert v.startswith("M² Modigliani MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh338_verdetto"](-0.5, 1.0, 8.5, 9.0)
        assert v.startswith("M² Modigliani DEBOLE")

    def test_verdetto_scala_levata(self):
        v = _F["mh338_verdetto"](2.0, 1.5, 11.0, 9.0)
        assert "levata" in v
        assert "meno rischiosa" in v

    def test_verdetto_scala_simile(self):
        v = _F["mh338_verdetto"](2.0, 1.0, 11.0, 9.0)
        assert "simile" in v

    def test_verdetto_none(self):
        v = _F["mh338_verdetto"](None, 0.8, 10.0, 8.0)
        assert v.startswith("M² Modigliani NON MISURABILE")
        v2 = _F["mh338_verdetto"](2.0, None, 10.0, 8.0)
        assert v2.startswith("M² Modigliani NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh338_verdetto"](DELTA, SCALA, M2, BM_ANN)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh338_verdetto"]("x", 1.0, 10.0, 9.0)
