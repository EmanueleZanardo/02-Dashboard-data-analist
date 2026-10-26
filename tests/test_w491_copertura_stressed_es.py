"""Test tab491 '🛡️🌪️ Copertura dello Stressed ES: quanto hedgiare per rientrare nel limite?': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh491_num", "mh491_segno", "mh491_mese", "mh491_z",
           "mh491_phi", "mh491_Phi", "mh491_lambda",
           "mh491_mult", "mh491_limite",
           "mh491_dv01_linea", "mh491_sigma_mtm_linea",
           "mh491_es_stress_linea", "mh491_riga", "mh491_componenti",
           "mh491_idx", "mh491_spread_bps", "mh491_copertura")

TITLE491 = "🛡️🌪️ Copertura dello Stressed ES: quanto hedgiare per rientrare nel limite?"
TITLE490 = "🪓🌊 Component Stressed ES: chi alimenta la coda sotto stress?"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, f_now 88.00,
# vol giornaliera 2.5%, z 99%, stress x2.
SIGMA_MTM_A = 220000.0
ES_STRESS_A = 1172694.2569521545

# Demo B: portafoglio 3 linee (TTF long 2027-01 sigma 2.5%,
# TTF short 2026-12 sigma 2.5%, Power DE long 2027-03 sigma 1.8%),
# z 99%, stress x2, limite ES 3'000'000 EUR; hedge sulla peggiore
# (Power DE 2027-03) con F_hedge = F_now = 116.00, sigma_hedge = 1.8%,
# spread 10 bps.
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
ES_STRESS_CONS_B = 3998354.3733627778
ES_STRESS_IND_B = 2586472.0219811616
WORST_B = 2
LABEL_WORST_B = "Power baseload DE 2027-03"
LIMITE_ES_B = 3000000.0
HEDGE_B_MWH = 89699.9318201976  # = taglio tab490 (stessi parametri hedge)
COSTO_B_EUR = 10405.19209114292  # h * 116.00 * 10/10000
ES_MIN_B = 1772367.456529961  # es_cons - es_worst (copertura intera gamba)


def _righe_b():
    return [_F["mh491_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


class TestRegistry491:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_counts(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 725
        assert TITLE491 in titoli
        assert TITLE490 in titoli
        assert "tab491" in dvars

    def test_ui_indentata(self):
        src = self._src()
        assert "    with tab491:" in src

    def test_titolo_occorrenze(self):
        src = self._src()
        # header W491 + lista titoli + H1 nella UI
        assert src.count(TITLE491) == 3

    def test_dvar_line(self):
        src = self._src()
        assert "tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725 = st.tabs([" in src

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st491_" in ln]
        basi = [re.search(r"st491_[a-z]+", ln).group(0) for ln in righe]
        # ogni base compare una sola volta nel sorgente
        # (il loop for genera le 3 istanze a runtime)
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10


class TestNum491:
    def test_ok(self):
        assert _F["mh491_num"](3, "x") == 3.0
        assert _F["mh491_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh491_num"](v, "x")


class TestSegno491:
    def test_ok(self):
        assert _F["mh491_segno"](1.0, "s") == 1.0
        assert _F["mh491_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh491_segno"](v, "s")


class TestMese491:
    def test_ok(self):
        assert _F["mh491_mese"]("2027-01", "m") == "2027-01"
        assert _F["mh491_mese"](" 2027-03 ", "m") == "2027-03"

    def test_ko(self):
        for v in ("2027", "2027-13", "2027-00", 202701, "gen-2027"):
            with pytest.raises(ValueError):
                _F["mh491_mese"](v, "m")


class TestZLambda491:
    def test_z(self):
        assert _F["mh491_z"](0.99, "c") == Z99
        assert _F["mh491_z"](0.975, "c") == 1.959963984540054
        with pytest.raises(ValueError):
            _F["mh491_z"](0.95, "c")

    def test_lambda(self):
        assert _F["mh491_lambda"](Z99) == pytest.approx(LAMBDA99)
        # lambda(z) >= z sempre
        assert _F["mh491_lambda"](Z99) >= Z99

    def test_mult_limite(self):
        assert _F["mh491_mult"](1.0, "m") == 1.0
        assert _F["mh491_mult"](10.0, "m") == 10.0
        with pytest.raises(ValueError):
            _F["mh491_mult"](0.99, "m")
        with pytest.raises(ValueError):
            _F["mh491_mult"](10.01, "m")
        assert _F["mh491_limite"](1.0, "l") == 1.0
        with pytest.raises(ValueError):
            _F["mh491_limite"](0.0, "l")
        with pytest.raises(ValueError):
            _F["mh491_limite"](-5.0, "l")


class TestIdxSpread491:
    def test_idx_ok(self):
        assert _F["mh491_idx"](0, 3, "i") == 0
        assert _F["mh491_idx"](2, 3, "i") == 2
        assert _F["mh491_idx"](2.0, 3, "i") == 2

    def test_idx_ko(self):
        for v in (-1, 3, 1.5, True, "1"):
            with pytest.raises(ValueError):
                _F["mh491_idx"](v, 3, "i")

    def test_spread_ok(self):
        assert _F["mh491_spread_bps"](0.0, "s") == 0.0
        assert _F["mh491_spread_bps"](10.0, "s") == 10.0
        assert _F["mh491_spread_bps"](1000.0, "s") == 1000.0

    def test_spread_ko(self):
        for v in (-0.1, 1000.1, "10"):
            with pytest.raises(ValueError):
                _F["mh491_spread_bps"](v, "s")


class TestEsStress491:
    def test_demo_a(self):
        assert _F["mh491_es_stress_linea"](
            SIGMA_MTM_A, Z99, 2.0) == pytest.approx(ES_STRESS_A)

    def test_demo_b_componenti(self):
        comp = _F["mh491_componenti"](_righe_b(), Z99, 2.0)
        assert comp["es_stress_cons"] == pytest.approx(ES_STRESS_CONS_B)
        assert comp["es_stress_ind"] == pytest.approx(ES_STRESS_IND_B)
        assert comp["div_benefit"] == pytest.approx(
            (ES_STRESS_CONS_B - ES_STRESS_IND_B) / ES_STRESS_CONS_B)
        assert sum(comp["share_cons"]) == pytest.approx(1.0)
        assert sum(comp["comp_ind"]) == pytest.approx(comp["es_stress_ind"])

    def test_riga_ko(self):
        with pytest.raises(ValueError):
            _F["mh491_riga"]("TTF gas", "2027-13", 100.0, 1.0,
                             95.0, 88.0, 2.5)
        with pytest.raises(ValueError):
            _F["mh491_riga"]("TTF gas", "2027-01", -1.0, 1.0,
                             95.0, 88.0, 2.5)


class TestCopertura491:
    def _cov_b(self, limite=LIMITE_ES_B, idx=WORST_B, f_h=116.00,
               s_h=1.8, spread=10.0):
        return _F["mh491_copertura"](_righe_b(), Z99, 2.0, limite, idx,
                                     f_h, s_h, spread)

    def test_demo_b_hedge(self):
        cov = self._cov_b()
        assert cov["es_stress_cons"] == pytest.approx(ES_STRESS_CONS_B)
        assert cov["limite"] == LIMITE_ES_B
        assert cov["linea"] == LABEL_WORST_B
        assert cov["direzione"] == "short"  # linea long -> hedge short
        assert cov["copertura_mwh"] == pytest.approx(HEDGE_B_MWH)
        # con gli stessi parametri dell'hedge = taglio tab490
        assert cov["copertura_mwh"] == pytest.approx(89699.9318201976)
        assert cov["costo_eur"] == pytest.approx(COSTO_B_EUR)
        assert cov["es_dopo_copertura"] == pytest.approx(LIMITE_ES_B)
        assert cov["verdetto"].startswith("COPRIRE")

    def test_costo_formula(self):
        cov = self._cov_b()
        assert cov["costo_eur"] == pytest.approx(
            cov["copertura_mwh"] * 116.00 * 10.0 / 10000.0)

    def test_hedge_params_custom(self):
        # F_hedge piu' basso -> es_per_mwh minore -> serve piu' volume
        cov = self._cov_b(f_h=100.00)
        assert cov["copertura_mwh"] == pytest.approx(104051.92091142922)
        assert cov["copertura_mwh"] > HEDGE_B_MWH

    def test_nessuna_copertura(self):
        cov = self._cov_b(limite=5000000.0)
        assert cov["copertura_mwh"] is None
        assert cov["costo_eur"] is None
        assert cov["es_dopo_copertura"] == pytest.approx(ES_STRESS_CONS_B)
        assert cov["verdetto"].startswith("NESSUNA COPERTURA NECESSARIA")

    def test_copertura_insufficiente(self):
        # limite sotto es_cons - es_worst: neanche coprendo tutta la gamba basta
        cov = self._cov_b(limite=1000000.0)
        assert cov["copertura_mwh"] is None
        assert cov["costo_eur"] is None
        assert cov["es_dopo_copertura"] == pytest.approx(ES_MIN_B)
        assert cov["verdetto"].startswith("COPERTURA INSUFFICIENTE")

    def test_direzione_long(self):
        # linea short (idx 1) -> hedge long
        cov = self._cov_b(idx=1)
        assert cov["linea"] == "TTF gas 2026-12"
        assert cov["direzione"] == "long"

    def test_errori(self):
        righe = _righe_b()
        with pytest.raises(ValueError):  # indice fuori range
            _F["mh491_copertura"](righe, Z99, 2.0, LIMITE_ES_B, 5,
                                  116.0, 1.8, 10.0)
        with pytest.raises(ValueError):  # sigma hedge nulla
            _F["mh491_copertura"](righe, Z99, 2.0, LIMITE_ES_B, WORST_B,
                                  116.0, 0.0, 10.0)
        with pytest.raises(ValueError):  # f_hedge zero -> hedge senza coda
            _F["mh491_copertura"](righe, Z99, 2.0, LIMITE_ES_B, WORST_B,
                                  0.0, 1.8, 10.0)
        with pytest.raises(ValueError):  # limite non positivo
            _F["mh491_copertura"](righe, Z99, 2.0, -5.0, WORST_B,
                                  116.0, 1.8, 10.0)
        with pytest.raises(ValueError):  # spread fuori range
            _F["mh491_copertura"](righe, Z99, 2.0, LIMITE_ES_B, WORST_B,
                                  116.0, 1.8, 1001.0)
        with pytest.raises(ValueError):  # mult fuori range
            _F["mh491_copertura"](righe, Z99, 0.5, LIMITE_ES_B, WORST_B,
                                  116.0, 1.8, 10.0)
