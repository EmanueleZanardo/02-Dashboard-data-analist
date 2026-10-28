"""Test tab490 '🪓🌊 Component Stressed ES: chi alimenta la coda sotto stress?': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh490_num", "mh490_segno", "mh490_mese", "mh490_z",
           "mh490_phi", "mh490_Phi", "mh490_lambda",
           "mh490_mult", "mh490_limite",
           "mh490_dv01_linea", "mh490_sigma_mtm_linea",
           "mh490_es_stress_linea", "mh490_riga", "mh490_componenti",
           "mh490_taglio")

TITLE490 = "🪓🌊 Component Stressed ES: chi alimenta la coda sotto stress?"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, f_now 88.00,
# vol giornaliera 2.5%, z 99%, stress x2.
SIGMA_MTM_A = 220000.0
ES_STRESS_A = 1172694.2569521545

# Demo B: portafoglio 3 linee (TTF long 2027-01 sigma 2.5%,
# TTF short 2026-12 sigma 2.5%, Power DE long 2027-03 sigma 1.8%),
# z 99%, stress x2, limite ES 3'000'000 EUR.
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
ES_STRESS_B = [1172694.2569521545, 599673.1995778063, 2225986.916832817]
ES_STRESS_CONS_B = 3998354.3733627778
ES_STRESS_IND_B = 2586472.0219811616
DIV_BENEFIT_B = 0.353115862062563
PEG_B = 'Power baseload DE 2027-03'
LIMITE_ES_B = 3000000.0
TAGLIO_B_MWH = 89699.9318201976


def _righe_b():
    return [_F["mh490_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


class TestRegistry490:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_counts(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 765
        assert TITLE490 in titoli
        assert "tab491" in dvars

    def test_ui_indentata(self):
        src = self._src()
        assert "    with tab490:" in src

    def test_titolo_occorrenze(self):
        src = self._src()
        # header W490 + lista titoli + H1 nella UI
        assert src.count(TITLE490) == 3

    def test_dvar_line(self):
        src = self._src()
        assert "tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765 = st.tabs([" in src

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st490_" in ln]
        basi = [re.search(r"st490_[a-z]+", ln).group(0) for ln in righe]
        # ogni base compare una sola volta nel sorgente
        # (il loop for genera le 3 istanze a runtime)
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10


class TestNum490:
    def test_ok(self):
        assert _F["mh490_num"](3, "x") == 3.0
        assert _F["mh490_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh490_num"](v, "x")


class TestSegno490:
    def test_ok(self):
        assert _F["mh490_segno"](1.0, "s") == 1.0
        assert _F["mh490_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh490_segno"](v, "s")


class TestMese490:
    def test_ok(self):
        assert _F["mh490_mese"]("2027-01", "m") == "2027-01"
        assert _F["mh490_mese"](" 2027-03 ", "m") == "2027-03"

    def test_ko(self):
        for v in ("2027", "2027-13", "2027-00", 202701, "gen-2027"):
            with pytest.raises(ValueError):
                _F["mh490_mese"](v, "m")


class TestZ490:
    def test_ok(self):
        assert _F["mh490_z"](0.99, "c") == Z99
        assert _F["mh490_z"](0.975, "c") == pytest.approx(1.959963984540054)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_z"](0.95, "c")


class TestPhi490:
    def test_phi_zero(self):
        import math
        assert _F["mh490_phi"](0.0) == pytest.approx(
            1.0 / math.sqrt(2.0 * math.pi))

    def test_Phi_zero(self):
        assert _F["mh490_Phi"](0.0) == pytest.approx(0.5)

    def test_lambda99(self):
        assert _F["mh490_lambda"](Z99) == pytest.approx(LAMBDA99, rel=1e-9)
        # l'ES e' sempre >= VaR: lambda(z) >= z
        assert _F["mh490_lambda"](Z99) >= Z99
        assert _F["mh490_lambda"](1.959963984540054) >= 1.959963984540054


class TestMult490:
    def test_ok(self):
        assert _F["mh490_mult"](2.0) == 2.0
        assert _F["mh490_mult"](10.0) == 10.0

    def test_ko(self):
        for v in (0.0, -1.0, 10.5):
            with pytest.raises(ValueError):
                _F["mh490_mult"](v)


class TestLimite490:
    def test_ok(self):
        assert _F["mh490_limite"](3000000.0) == 3000000.0

    def test_ko(self):
        for v in (0.0, -5.0):
            with pytest.raises(ValueError):
                _F["mh490_limite"](v)


class TestDv01490:
    def test_ok(self):
        assert _F["mh490_dv01_linea"](1.0, 100000.0) == 100000.0
        assert _F["mh490_dv01_linea"](-1.0, 50000.0) == -50000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_dv01_linea"](1.0, -1.0)


class TestSigmaMtm490:
    def test_demo_a(self):
        assert _F["mh490_sigma_mtm_linea"](100000.0, 2.5, 88.00) == SIGMA_MTM_A

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_sigma_mtm_linea"](100000.0, 0.0, 88.00)
        with pytest.raises(ValueError):
            _F["mh490_sigma_mtm_linea"](100000.0, 101.0, 88.00)
        with pytest.raises(ValueError):
            _F["mh490_sigma_mtm_linea"](100000.0, 2.5, -1.0)


class TestEsStressLinea490:
    def test_demo_a(self):
        assert _F["mh490_es_stress_linea"](
            SIGMA_MTM_A, Z99, 2.0) == pytest.approx(ES_STRESS_A, rel=1e-9)

    def test_es_maggiore_var(self):
        # a parita' di z e stress, ES >= VaR (lambda >= z)
        es = _F["mh490_es_stress_linea"](SIGMA_MTM_A, Z99, 2.0)
        var = Z99 * 2.0 * SIGMA_MTM_A
        assert es >= var

    def test_scala_con_mult(self):
        v1 = _F["mh490_es_stress_linea"](SIGMA_MTM_A, Z99, 1.0)
        v3 = _F["mh490_es_stress_linea"](SIGMA_MTM_A, Z99, 3.0)
        assert v3 == pytest.approx(3.0 * v1)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_es_stress_linea"](-1.0, Z99, 2.0)
        with pytest.raises(ValueError):
            _F["mh490_es_stress_linea"](SIGMA_MTM_A, 0.0, 2.0)
        with pytest.raises(ValueError):
            _F["mh490_es_stress_linea"](SIGMA_MTM_A, Z99, 0.0)


class TestRiga490:
    def test_demo_a(self):
        r = _F["mh490_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00,
                             88.00, 2.5)
        assert r["scadenza"] == "2027-01"
        assert r["dv01"] == 100000.0
        assert r["sigma_mtm"] == SIGMA_MTM_A

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_riga"]("TTF gas", "2027-13", 100000.0, 1.0, 95.00,
                             88.00, 2.5)
        with pytest.raises(ValueError):
            _F["mh490_riga"]("TTF gas", "2027-01", 100000.0, 1.0, -95.00,
                             88.00, 2.5)


class TestComponenti490:
    def test_demo_b(self):
        c = _F["mh490_componenti"](_righe_b(), Z99, 2.0)
        for got, exp in zip(c["es_stress"], ES_STRESS_B):
            assert got == pytest.approx(exp, rel=1e-9)
        assert c["es_stress_cons"] == pytest.approx(ES_STRESS_CONS_B,
                                                   rel=1e-9)
        # conservativo = somma (attribuzione lineare, corr=1)
        assert sum(c["es_stress"]) == pytest.approx(c["es_stress_cons"])
        # indipendenza: RSS
        import math
        assert c["es_stress_ind"] == pytest.approx(
            math.sqrt(sum(v * v for v in ES_STRESS_B)))
        assert c["es_stress_ind"] == pytest.approx(ES_STRESS_IND_B, rel=1e-9)
        assert c["es_stress_ind"] <= c["es_stress_cons"]
        # Eulero: i componenti d'indipendenza sommano all'ES indipendente
        assert sum(c["comp_ind"]) == pytest.approx(c["es_stress_ind"])
        # share conservative: sommano a 1
        assert sum(c["share_cons"]) == pytest.approx(1.0)
        # la linea C e' la peggiore
        assert c["share_cons"][2] == max(c["share_cons"])
        assert c["div_benefit"] == pytest.approx(DIV_BENEFIT_B, rel=1e-9)
        assert 0.0 <= c["div_benefit"] <= 1.0

    def test_riga_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_componenti"]([], Z99, 2.0)

    def test_volumi_nulli(self):
        r = _F["mh490_riga"]("TTF gas", "2027-01", 0.0, 1.0, 95.00, 88.00,
                             2.5)
        c = _F["mh490_componenti"]([r], Z99, 2.0)
        assert c["es_stress_cons"] == 0.0
        assert c["share_cons"] == [0.0]


class TestTaglio490:
    def test_demo_b_sfondato(self):
        t = _F["mh490_taglio"](_righe_b(), Z99, 2.0, LIMITE_ES_B)
        assert t["peggiore"] == PEG_B
        assert t["verdetto"].startswith(f"TAGLIARE {PEG_B}:")
        assert t["verdetto"].endswith("LIMITE ES SFONDATO SOTTO STRESS")
        _per_mwh = ES_STRESS_B[2] / 200000.0
        assert t["taglio_mwh"] == pytest.approx(
            (ES_STRESS_CONS_B - LIMITE_ES_B) / _per_mwh, rel=1e-9)
        assert t["taglio_mwh"] == pytest.approx(TAGLIO_B_MWH, rel=1e-9)
        assert 0.0 < t["taglio_mwh"] < 200000.0
        # dopo il taglio l'ES stressato torna (circa) al limite
        assert t["es_dopo_taglio"] == pytest.approx(LIMITE_ES_B, rel=1e-9)

    def test_entro_limite(self):
        t = _F["mh490_taglio"](_righe_b(), Z99, 2.0, 10_000_000.0)
        assert t["peggiore"] is None
        assert t["taglio_mwh"] is None
        assert t["verdetto"] == ("NESSUN TAGLIO NECESSARIO — "
                                 "ENTRO IL LIMITE ES SOTTO STRESS")
        assert t["es_dopo_taglio"] == pytest.approx(ES_STRESS_CONS_B,
                                                   rel=1e-9)

    def test_limite_uguale_es(self):
        t = _F["mh490_taglio"](_righe_b(), Z99, 2.0, ES_STRESS_CONS_B)
        assert t["peggiore"] is None

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh490_taglio"](_righe_b(), Z99, 2.0, 0.0)

    def test_soglia_zero(self):
        # volume nullo -> ES nullo -> nessun taglio, nessun errore
        r = _F["mh490_riga"]("TTF gas", "2027-01", 0.0, 1.0, 95.00, 88.00,
                             2.5)
        t = _F["mh490_taglio"]([r], Z99, 2.0, 1.0)
        assert t["peggiore"] is None
        assert t["taglio_mwh"] is None
