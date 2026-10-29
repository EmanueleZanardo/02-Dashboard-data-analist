"""Test tab488 '🌪️📉 Stressed VaR: il VaR sotto volatilità stressata': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh488_num", "mh488_segno", "mh488_mese", "mh488_z",
           "mh488_phi", "mh488_Phi", "mh488_mult", "mh488_limite",
           "mh488_dv01_linea", "mh488_mtm_linea", "mh488_sigma_mtm_linea",
           "mh488_var_es_linea", "mh488_riga", "mh488_portafoglio",
           "mh488_moltiplicatore_critico", "mh488_verdetto")

TITLE488 = "🌪️📉 Stressed VaR: il VaR sotto volatilità stressata"
TITLE487 = "📉 VaR ed Expected Shortfall del portafoglio forward: il rischio giornaliero"

Z99 = 2.3263478740408408
Z975 = 1.959963984540054

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, f_now 88.00,
# vol giornaliera 2.5%, stress x2.
VAR_A = 511796.532288985
ES_A = 586347.1284760772
VAR_STRESS_A = 1023593.06457797
ES_STRESS_A = 1172694.2569521545

# Demo B: portafoglio 3 linee (TTF long 2027-01 sigma 2.5%,
# TTF short 2026-12 sigma 2.5%, Power DE long 2027-03 sigma 1.8%),
# stress x2, limite 2'500'000 EUR.
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
MTM_B = 550000.0
VAR_CONS_B = 1744993.5403180346
ES_CONS_B = 1999177.1866813889
VAR_IND_B = 1128808.6420350282
ES_IND_B = 1293236.010990581
VAR_STRESS_CONS_B = 3489987.080636069
ES_STRESS_CONS_B = 3998354.3733627778
VAR_STRESS_IND_B = 2257617.2840700564
ES_STRESS_IND_B = 2586472.021981162
MULT_CRIT_B = 1.4326700599386524
VERD_B = "LIMITE SFONDATO SOTTO STRESS"
LIMITE_B = 2500000.0


def _righe_b():
    return [_F["mh488_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


class TestRegistry488:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_counts(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 790
        assert TITLE488 in titoli
        assert "tab489" in dvars

    def test_ui_indentata(self):
        src = self._src()
        assert "    with tab488:" in src

    def test_titolo_occorrenze(self):
        src = self._src()
        # header W488 + lista titoli + H1 nella UI
        assert src.count(TITLE488) == 3

    def test_dvar_line(self):
        src = self._src()
        assert "tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790 = st.tabs([" in src


class TestNum488:
    def test_ok(self):
        assert _F["mh488_num"](3, "x") == 3.0
        assert _F["mh488_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh488_num"](v, "x")


class TestSegno488:
    def test_ok(self):
        assert _F["mh488_segno"](1.0, "s") == 1.0
        assert _F["mh488_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh488_segno"](v, "s")


class TestMese488:
    def test_ok(self):
        assert _F["mh488_mese"]("2026-11", "m") == "2026-11"

    def test_ko(self):
        for v in ("2026-13", "26-11", "2026/11", 202611):
            with pytest.raises(ValueError):
                _F["mh488_mese"](v, "m")


class TestZ488:
    def test_99(self):
        assert _F["mh488_z"](0.99, "c") == Z99

    def test_975(self):
        assert _F["mh488_z"](0.975, "c") == Z975

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_z"](0.95, "c")


class TestNormali488:
    def test_phi_0(self):
        assert _F["mh488_phi"](0) == pytest.approx(0.3989422804014327)

    def test_Phi_0(self):
        assert _F["mh488_Phi"](0) == pytest.approx(0.5)

    def test_Phi_z99(self):
        assert _F["mh488_Phi"](Z99) == pytest.approx(0.99, abs=1e-12)


class TestMult488:
    def test_ok(self):
        assert _F["mh488_mult"](1.0) == 1.0
        assert _F["mh488_mult"](2.0) == 2.0
        assert _F["mh488_mult"](10.0) == 10.0

    def test_ko(self):
        for v in (0.99, 10.01, -2.0, "2"):
            with pytest.raises(ValueError):
                _F["mh488_mult"](v)


class TestLimite488:
    def test_ok(self):
        assert _F["mh488_limite"](2500000.0) == 2500000.0

    def test_ko(self):
        for v in (0.0, -100.0, "x", None):
            with pytest.raises(ValueError):
                _F["mh488_limite"](v)


class TestDv01Mtm488:
    def test_dv01(self):
        assert _F["mh488_dv01_linea"](1.0, 100000.0) == 100000.0
        assert _F["mh488_dv01_linea"](-1.0, 50000.0) == -50000.0
        with pytest.raises(ValueError):
            _F["mh488_dv01_linea"](1.0, -1.0)

    def test_mtm(self):
        assert _F["mh488_mtm_linea"](1.0, 100000.0, 95.0, 88.0) == -700000.0
        assert _F["mh488_mtm_linea"](-1.0, 50000.0, 91.0, 90.0) == 50000.0
        with pytest.raises(ValueError):
            _F["mh488_mtm_linea"](1.0, 100000.0, -95.0, 88.0)


class TestSigma488:
    def test_ok(self):
        assert _F["mh488_sigma_mtm_linea"](100000.0, 2.5, 88.0) == 220000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_sigma_mtm_linea"](100000.0, 0.0, 88.0)
        with pytest.raises(ValueError):
            _F["mh488_sigma_mtm_linea"](100000.0, 2.5, -88.0)


class TestVarEsLinea488:
    def test_demo_a(self):
        ve = _F["mh488_var_es_linea"](220000.0, Z99, 2.0)
        assert ve["var"] == pytest.approx(VAR_A)
        assert ve["es"] == pytest.approx(ES_A)
        assert ve["var_stress"] == pytest.approx(VAR_STRESS_A)
        assert ve["es_stress"] == pytest.approx(ES_STRESS_A)

    def test_stress_amplifica(self):
        ve = _F["mh488_var_es_linea"](220000.0, Z99, 3.0)
        assert ve["var_stress"] == pytest.approx(3.0 * ve["var"])
        assert ve["es_stress"] == pytest.approx(3.0 * ve["es"])

    def test_es_maggiore_var(self):
        ve = _F["mh488_var_es_linea"](220000.0, Z99, 2.0)
        assert ve["es"] >= ve["var"]
        assert ve["es_stress"] >= ve["var_stress"]

    def test_mult_1_identico(self):
        ve = _F["mh488_var_es_linea"](220000.0, Z99, 1.0)
        assert ve["var_stress"] == pytest.approx(ve["var"])
        assert ve["es_stress"] == pytest.approx(ve["es"])

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_var_es_linea"](-1.0, Z99, 2.0)
        with pytest.raises(ValueError):
            _F["mh488_var_es_linea"](220000.0, Z99, 0.5)


class TestRiga488:
    def test_campi(self):
        r = _F["mh488_riga"]("TTF gas", "2027-01", 100000.0, 1.0,
                             95.00, 88.00, 2.50)
        assert r["commodity"] == "TTF gas"
        assert r["scadenza"] == "2027-01"
        assert r["dv01"] == 100000.0
        assert r["mtm"] == -700000.0
        assert r["sigma_mtm"] == 220000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_riga"]("TTF gas", "2027-13", 100000.0, 1.0,
                             95.00, 88.00, 2.50)


class TestPortafoglio488:
    def test_demo_b(self):
        agg = _F["mh488_portafoglio"](_righe_b(), Z99, 2.0)
        assert agg["mtm_tot"] == pytest.approx(MTM_B)
        assert agg["var_cons"] == pytest.approx(VAR_CONS_B)
        assert agg["es_cons"] == pytest.approx(ES_CONS_B)
        assert agg["var_ind"] == pytest.approx(VAR_IND_B)
        assert agg["es_ind"] == pytest.approx(ES_IND_B)
        assert agg["var_stress_cons"] == pytest.approx(VAR_STRESS_CONS_B)
        assert agg["es_stress_cons"] == pytest.approx(ES_STRESS_CONS_B)
        assert agg["var_stress_ind"] == pytest.approx(VAR_STRESS_IND_B)
        assert agg["es_stress_ind"] == pytest.approx(ES_STRESS_IND_B)
        assert agg["amplificazione"] == 2.0

    def test_stress_scala_lineare(self):
        agg = _F["mh488_portafoglio"](_righe_b(), Z99, 3.0)
        assert agg["var_stress_cons"] == pytest.approx(3.0 * agg["var_cons"])
        assert agg["es_stress_cons"] == pytest.approx(3.0 * agg["es_cons"])

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_portafoglio"]([], Z99, 2.0)


class TestMultCritico488:
    def test_demo_b(self):
        mc = _F["mh488_moltiplicatore_critico"](VAR_CONS_B, LIMITE_B)
        assert mc == pytest.approx(MULT_CRIT_B)

    def test_coerente_con_verdetto(self):
        # al moltiplicatore critico lo stressed VaR tocca il limite
        assert VAR_CONS_B * MULT_CRIT_B == pytest.approx(LIMITE_B)

    def test_none_se_var_nullo(self):
        assert _F["mh488_moltiplicatore_critico"](0.0, LIMITE_B) is None

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_moltiplicatore_critico"](VAR_CONS_B, 0.0)


class TestVerdetto488:
    def test_sfondato(self):
        v = _F["mh488_verdetto"](_righe_b(), Z99, 2.0, LIMITE_B)
        assert v["verdetto"] == VERD_B
        assert v["var_stress_cons"] == pytest.approx(VAR_STRESS_CONS_B)
        assert v["mult_critico"] == pytest.approx(MULT_CRIT_B)
        assert v["limite"] == LIMITE_B
        assert v["mtm_tot"] == pytest.approx(MTM_B)

    def test_entro(self):
        v = _F["mh488_verdetto"](_righe_b(), Z99, 2.0, 5000000.0)
        assert v["verdetto"] == "ENTRO IL LIMITE SOTTO STRESS"
        assert v["mult_critico"] == pytest.approx(2.8653401198773047)

    def test_senza_stress_entro(self):
        v = _F["mh488_verdetto"](_righe_b(), Z99, 1.0, LIMITE_B)
        assert v["verdetto"] == "ENTRO IL LIMITE SOTTO STRESS"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh488_verdetto"](_righe_b(), Z99, 2.0, -1.0)
