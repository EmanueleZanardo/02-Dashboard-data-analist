"""Test tab487 '📉 VaR ed Expected Shortfall del portafoglio forward: il rischio giornaliero': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh487_num", "mh487_segno", "mh487_mese", "mh487_z",
           "mh487_phi", "mh487_Phi", "mh487_dv01_linea",
           "mh487_sigma_mtm_linea", "mh487_var_linea", "mh487_es_linea",
           "mh487_riga", "mh487_portafoglio", "mh487_verdetto")

TITLE487 = "📉 VaR ed Expected Shortfall del portafoglio forward: il rischio giornaliero"
TITLE486 = "🧾🔍 P&L spiegato dalle greche: theta, delta e rho contro il ΔMtM realizzato"

Z99 = 2.3263478740408408
Z975 = 1.959963984540054

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, f_now 88.00,
# vol giornaliera 2.5%.
DV01_A = 100000.0
MTM_A = -700000.0
SIGMA_A = 220000.0
VAR_A = 511796.532288985
ES_A = 586347.1284760772

# Demo B: portafoglio 3 linee (TTF long 2027-01 sigma 2.5%,
# TTF short 2026-12 sigma 2.5%, Power DE long 2027-03 sigma 1.8%).
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00,
     "f_now": 88.00, "sigma_pct": 2.5},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00,
     "f_now": 90.00, "sigma_pct": 2.5},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00,
     "f_now": 116.00, "sigma_pct": 1.8},
]
N_B = 3
MTM_B = 550000.0
SIGMA_CONS_B = 750100.0
SIGMA_IND_B = 485227.7918668715
VAR_CONS_B = 1744993.5403180346
ES_CONS_B = 1999177.1866813889
VAR_IND_B = 1128808.6420350282
ES_IND_B = 1293236.0109905808
DIV_B = 0.35311586206256296
VERD_B = "RISCHIO ELEVATO"
RATIO_B = 3.172715527850972


def _righe_b():
    return [_F["mh487_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


class TestRegistry487:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_counts(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 668
        assert TITLE487 in titoli
        assert "tab488" in dvars

    def test_ui_indentata(self):
        src = self._src()
        assert "    with tab487:" in src

    def test_titolo_occorrenze(self):
        src = self._src()
        # header W487 + lista titoli + H1 nella UI
        assert src.count(TITLE487) == 3

    def test_dvar_line(self):
        src = self._src()
        assert "tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668 = st.tabs([" in src


class TestNum487:
    def test_ok(self):
        assert _F["mh487_num"](3, "x") == 3.0
        assert _F["mh487_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh487_num"](v, "x")


class TestSegno487:
    def test_ok(self):
        assert _F["mh487_segno"](1.0, "s") == 1.0
        assert _F["mh487_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh487_segno"](v, "s")


class TestMese487:
    def test_ok(self):
        assert _F["mh487_mese"]("2026-11", "m") == "2026-11"

    def test_ko(self):
        for v in ("2026-13", "26-11", "2026/11", 202611):
            with pytest.raises(ValueError):
                _F["mh487_mese"](v, "m")


class TestZ487:
    def test_99(self):
        assert _F["mh487_z"](0.99, "c") == Z99

    def test_975(self):
        assert _F["mh487_z"](0.975, "c") == Z975

    def test_ko(self):
        for v in (0.95, 1.0, 0.0, "0.99"):
            with pytest.raises(ValueError):
                _F["mh487_z"](v, "c")

    def test_phi_zero(self):
        assert _F["mh487_phi"](0.0) == pytest.approx(1.0 / math.sqrt(2.0 * math.pi))

    def test_phi_positivo(self):
        assert _F["mh487_phi"](Z99) < _F["mh487_phi"](0.0)
        assert _F["mh487_phi"](Z99) > 0.0

    def test_Phi_zero(self):
        assert _F["mh487_Phi"](0.0) == pytest.approx(0.5)

    def test_Phi_z99(self):
        assert _F["mh487_Phi"](Z99) == pytest.approx(0.99, rel=1e-6)

    def test_Phi_z975(self):
        assert _F["mh487_Phi"](Z975) == pytest.approx(0.975, rel=1e-6)


class TestDv01487:
    def test_long(self):
        assert _F["mh487_dv01_linea"](1.0, 100000.0) == 100000.0

    def test_short(self):
        assert _F["mh487_dv01_linea"](-1.0, 50000.0) == -50000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh487_dv01_linea"](1.0, -10.0)
        with pytest.raises(ValueError):
            _F["mh487_dv01_linea"](0.0, 100.0)


class TestSigma487:
    def test_demo_a(self):
        assert _F["mh487_sigma_mtm_linea"](DV01_A, 2.5, 88.00) == SIGMA_A

    def test_lineare_in_dv01(self):
        s = _F["mh487_sigma_mtm_linea"]
        assert s(200000.0, 2.5, 88.0) == pytest.approx(2.0 * s(100000.0, 2.5, 88.0))

    def test_ko(self):
        for v in (0.0, -1.0, 100.1, "2.5"):
            with pytest.raises(ValueError):
                _F["mh487_sigma_mtm_linea"](100000.0, v, 88.0)
        with pytest.raises(ValueError):
            _F["mh487_sigma_mtm_linea"](100000.0, 2.5, -1.0)


class TestVarEs487:
    def test_var_demo_a(self):
        assert _F["mh487_var_linea"](SIGMA_A, Z99) == VAR_A

    def test_es_demo_a(self):
        assert _F["mh487_es_linea"](SIGMA_A, Z99) == ES_A

    def test_es_maggiore_var(self):
        for sig in (1000.0, 220000.0, 417600.0):
            for z in (Z99, Z975):
                assert _F["mh487_es_linea"](sig, z) > _F["mh487_var_linea"](sig, z)

    def test_scaling_lineare(self):
        assert _F["mh487_var_linea"](2.0 * SIGMA_A, Z99) == pytest.approx(2.0 * VAR_A)
        assert _F["mh487_es_linea"](2.0 * SIGMA_A, Z99) == pytest.approx(2.0 * ES_A)

    def test_es_factor_teorico(self):
        z = Z99
        atteso = SIGMA_A * _F["mh487_phi"](z) / (1.0 - _F["mh487_Phi"](z))
        assert _F["mh487_es_linea"](SIGMA_A, z) == pytest.approx(atteso)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh487_var_linea"](-1.0, Z99)
        with pytest.raises(ValueError):
            _F["mh487_var_linea"](SIGMA_A, 0.0)
        with pytest.raises(ValueError):
            _F["mh487_es_linea"](SIGMA_A, -1.0)


class TestRiga487:
    def test_demo_a(self):
        r = _F["mh487_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                             95.00, 88.00, 2.5)
        assert r["dv01"] == DV01_A
        assert r["mtm"] == MTM_A
        assert r["sigma_mtm"] == SIGMA_A
        assert r["volume_mwh"] == 100000.0
        assert r["segno"] == 1.0
        assert r["scadenza"] == "2027-01"

    def test_short_mtm_positivo(self):
        r = _F["mh487_riga"]("TTF gas", "2026-12", 50000.0, -1.0,
                             91.00, 90.00, 2.5)
        assert r["mtm"] == pytest.approx(50000.0)
        assert r["dv01"] == -50000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh487_riga"]("TTF gas", "2027-13", 100000.0, 1.0,
                             95.00, 88.00, 2.5)


class TestPortafoglio487:
    def test_demo_b(self):
        agg = _F["mh487_portafoglio"](_righe_b(), Z99)
        assert agg["n_posizioni"] == N_B
        assert agg["mtm_tot"] == pytest.approx(MTM_B)
        assert agg["sigma_cons"] == pytest.approx(SIGMA_CONS_B)
        assert agg["sigma_ind"] == pytest.approx(SIGMA_IND_B)
        assert agg["var_cons"] == pytest.approx(VAR_CONS_B)
        assert agg["es_cons"] == pytest.approx(ES_CONS_B)
        assert agg["var_ind"] == pytest.approx(VAR_IND_B)
        assert agg["es_ind"] == pytest.approx(ES_IND_B)
        assert agg["div_benefit"] == pytest.approx(DIV_B)

    def test_conservativo_ge_indipendenza(self):
        agg = _F["mh487_portafoglio"](_righe_b(), Z99)
        assert agg["var_cons"] > agg["var_ind"]
        assert agg["es_cons"] > agg["es_ind"]
        assert 0.0 < agg["div_benefit"] < 1.0

    def test_linea_singola_div_zero(self):
        r = _F["mh487_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                             95.00, 88.00, 2.5)
        agg = _F["mh487_portafoglio"]([r], Z99)
        assert agg["div_benefit"] == pytest.approx(0.0)
        assert agg["var_cons"] == pytest.approx(agg["var_ind"])

    def test_ko_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh487_portafoglio"]([], Z99)


class TestVerdetto487:
    def test_demo_b_elevato(self):
        v = _F["mh487_verdetto"](_righe_b(), Z99)
        assert v["verdetto"] == VERD_B
        assert v["ratio"] == pytest.approx(RATIO_B)
        assert v["var_cons"] == pytest.approx(VAR_CONS_B)
        assert v["mtm_tot"] == pytest.approx(MTM_B)

    def test_contenuto(self):
        r = _F["mh487_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                             100.00, 200.00, 0.1)
        v = _F["mh487_verdetto"]([r], Z99)
        assert v["verdetto"] == "RISCHIO CONTENUTO"
        assert v["ratio"] <= 0.02

    def test_moderato(self):
        r = _F["mh487_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                             100.00, 200.00, 0.5)
        v = _F["mh487_verdetto"]([r], Z99)
        assert v["verdetto"] == "RISCHIO MODERATO"
        assert 0.02 < v["ratio"] < 0.10

    def test_neutrale_mtm_nullo(self):
        righe = [_F["mh487_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                                  95.00, 95.00, 2.5)]
        v = _F["mh487_verdetto"](righe, Z99)
        assert v["verdetto"] == "NEUTRALE"
        assert v["ratio"] is None

    def test_soglie_ko(self):
        with pytest.raises(ValueError):
            _F["mh487_verdetto"](_righe_b(), Z99, soglia_elevata=0.01,
                                 soglia_contenuta=0.02)
