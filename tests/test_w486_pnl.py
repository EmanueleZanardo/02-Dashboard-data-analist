"""Test tab486 '🧾🔍 P&L spiegato dalle greche: theta, delta e rho contro il ΔMtM realizzato': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh486_num", "mh486_segno", "mh486_mese", "mh486_mese_ord",
           "mh486_ord_mese", "mh486_data", "mh486_fine_mese", "mh486_tasso",
           "mh486_curva", "mh486_prezzo", "mh486_posizione", "mh486_tau",
           "mh486_riga", "mh486_portafoglio", "mh486_verdetto")

TITLE486 = "🧾🔍 P&L spiegato dalle greche: theta, delta e rho contro il ΔMtM realizzato"
TITLE485 = "🏦 Rho del portafoglio forward: il MtM sotto il tasso d'interesse"

# Curva TTF a t1 in backwardation (prezzi calanti con la scadenza)
CURVA_TTF = {"2026-11": 92.0, "2026-12": 90.0, "2027-01": 88.0,
             "2027-02": 87.0, "2027-03": 86.0}
# Curva Power DE a t1 in contango (prezzi crescenti con la scadenza)
CURVA_DE = {"2026-11": 100.0, "2026-12": 104.0, "2027-01": 108.0,
            "2027-02": 112.0, "2027-03": 116.0, "2027-04": 120.0}
DATA_NEW = "2026-10-15"
GIORNI = 30
R_OLD = 0.03
R_NEW = 0.035

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00,
# f_old 90.00 -> f_new 88.00 in 30 giorni, tassi 3% -> 3.5%.
F_TAU0_A = 89.97125256673462
F_TAU1_A = 88.0
MTM_OLD_A = -494364.6467299509
MTM_NEW_A = -692793.0040160946
D_MTM_A = -198428.3572861437
THETA_A = -197125.256673462
DELTA_A = 0.0
RHO_A = 1025.0100114390204
SPIEGATO_A = -196100.24666202298
RESIDUO_A = -2328.1106241207162

# Demo B: portafoglio 3 linee (TTF long 2027-01, TTF short 2026-12,
# Power DE long 2027-03), stesse curve/tassi/giorni.
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00,
     "f_old": 90.00, "f_new": 88.00},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00,
     "f_old": 92.00, "f_new": 90.00},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00,
     "f_old": 112.00, "f_new": 116.00},
]
CURVE_B = {"TTF gas": CURVA_TTF, "Power baseload DE": CURVA_DE}
D_MTM_B = 688136.3236315451
THETA_B = 689938.398357117
DELTA_B = 0.0
RHO_B = -1730.19724747096
RESIDUO_B = -71.87747810102883
VERD_B = 'SPIEGATO'
PCT_B = 1.0001044523819373

# Demo C: la forma della curva e' cambiata (curva t1 piatta a 88, ma il
# prezzo vecchio era 100) -> residuo grande -> DA INDAGARE.
CURVA_PIATTA = {"2026-11": 88.0, "2026-12": 88.0, "2027-01": 88.0}
RESIDUO_C = -1188182.6607574846
VERD_C = 'DA INDAGARE'


def _approx(a, b):
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6), f"{a} != {b}"


class TestRegistry486:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 821

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE486 in titoli
        assert "tab487" in dvars

    def test_ui_indentata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "    with tab486:" in src

    def test_titolo_occorrenze(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        # header W486 + lista titoli + H1 nella UI
        assert src.count(TITLE486) == 3

    def test_dvar_line(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "tab486, tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821 = st.tabs([" in src


class TestNum486:
    def test_ok(self):
        assert _F["mh486_num"](3, "x") == 3.0
        assert _F["mh486_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh486_num"](v, "x")


class TestSegno486:
    def test_ok(self):
        assert _F["mh486_segno"](1.0, "s") == 1.0
        assert _F["mh486_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh486_segno"](v, "s")


class TestMese486:
    def test_ok(self):
        assert _F["mh486_mese"]("2026-11", "m") == "2026-11"

    def test_ko(self):
        for v in ("2026-13", "26-11", "2026/11", 202611):
            with pytest.raises(ValueError):
                _F["mh486_mese"](v, "m")

    def test_ord_roundtrip(self):
        o = _F["mh486_mese_ord"]("2026-11")
        assert _F["mh486_ord_mese"](o) == "2026-11"
        assert _F["mh486_mese_ord"](_F["mh486_ord_mese"](o + 1)) == o + 1

    def test_ord_mese_ko(self):
        for v in (0, -5, 3.5, True):
            with pytest.raises(ValueError):
                _F["mh486_ord_mese"](v)


class TestData486:
    def test_ok(self):
        d = _F["mh486_data"]("2026-10-15", "d")
        assert (d.year, d.month, d.day) == (2026, 10, 15)

    def test_ko(self):
        for v in ("2026-13-01", "15-10-2026", "2026-02-30", 20261015):
            with pytest.raises(ValueError):
                _F["mh486_data"](v, "d")


class TestTasso486:
    def test_ok(self):
        assert _F["mh486_tasso"](0.03, "r") == 0.03
        assert _F["mh486_tasso"](-0.10, "r") == -0.10
        assert _F["mh486_tasso"](0.50, "r") == 0.50

    def test_ko(self):
        for v in (-0.101, 0.501, "3%"):
            with pytest.raises(ValueError):
                _F["mh486_tasso"](v, "r")


class TestCurva486:
    def test_ordinata(self):
        p = _F["mh486_curva"]({"2027-01": 88.0, "2026-12": 90.0}, "c")
        assert [x[0] for x in p] == sorted(x[0] for x in p)
        assert len(p) == 2

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_curva"]({}, "c")

    def test_prezzo_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_curva"]({"2026-12": -1.0}, "c")

    def test_mese_errato_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_curva"]({"2026-13": 90.0}, "c")


class TestPrezzo486:
    def test_punto_esatto(self):
        p = _F["mh486_curva"](CURVA_TTF, "c")
        o = _F["mh486_mese_ord"]("2027-01")
        _approx(_F["mh486_prezzo"](p, float(o)), 88.0)

    def test_interpolato(self):
        p = _F["mh486_curva"](CURVA_TTF, "c")
        o = _F["mh486_mese_ord"]("2026-12") + 0.5
        _approx(_F["mh486_prezzo"](p, float(o)), 89.0)

    def test_clamp(self):
        p = _F["mh486_curva"](CURVA_TTF, "c")
        o0 = _F["mh486_mese_ord"]("2026-11")
        o1 = _F["mh486_mese_ord"]("2027-03")
        _approx(_F["mh486_prezzo"](p, float(o0) - 5), 92.0)
        _approx(_F["mh486_prezzo"](p, float(o1) + 5), 86.0)


class TestPosizione486:
    def test_ok(self):
        p = _F["mh486_posizione"](
            {"commodity": "TTF", "scadenza": "2027-01", "volume_mwh": 10.0,
             "segno": 1.0, "f_fix": 95.0, "f_old": 90.0, "f_new": 88.0}, 0)
        assert p["f_old"] == 90.0 and p["f_new"] == 88.0

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh486_posizione"](
                {"commodity": "TTF", "scadenza": "2027-01", "volume_mwh": 10.0,
                 "segno": 1.0, "f_fix": 95.0, "f_old": 90.0}, 0)

    def test_degeneri(self):
        base = {"commodity": "TTF", "scadenza": "2027-01", "volume_mwh": 10.0,
                "segno": 1.0, "f_fix": 95.0, "f_old": 90.0, "f_new": 88.0}
        for k, v in (("volume_mwh", 0.0), ("volume_mwh", -1.0),
                     ("f_fix", -1.0), ("f_old", -1.0), ("f_new", -1.0),
                     ("segno", 0.0), ("scadenza", "2027-13")):
            bad = dict(base)
            bad[k] = v
            with pytest.raises(ValueError):
                _F["mh486_posizione"](bad, 0)


class TestTau486:
    def test_giorni_positivi(self):
        g, tau = _F["mh486_tau"]("2026-10-15", "2027-01")
        assert g == 108
        _approx(tau, 108 / 365.25)

    def test_scadenza_passata_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_tau"]("2027-02-01", "2027-01")


class TestRiga486:
    def test_demo_a_valori(self):
        r = _F["mh486_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00,
                             90.00, 88.00, CURVA_TTF, DATA_NEW, GIORNI,
                             R_OLD, R_NEW)
        _approx(r["f_roll_old"], F_TAU0_A)
        _approx(r["f_roll_new"], F_TAU1_A)
        _approx(r["mtm_old"], MTM_OLD_A)
        _approx(r["mtm_new"], MTM_NEW_A)
        _approx(r["delta_mtm"], D_MTM_A)
        _approx(r["theta"], THETA_A)
        _approx(r["delta"], DELTA_A)
        _approx(r["rho"], RHO_A)
        _approx(r["spiegato"], SPIEGATO_A)
        _approx(r["residuo"], RESIDUO_A)

    def test_identita_attribuzione(self):
        r = _F["mh486_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00,
                             90.00, 88.00, CURVA_TTF, DATA_NEW, GIORNI,
                             R_OLD, R_NEW)
        _approx(r["theta"] + r["delta"] + r["rho"] + r["residuo"],
                r["delta_mtm"])

    def test_demo_a_segni(self):
        # long in backwardation con prezzo in calo: tutto negativo
        assert D_MTM_A < 0
        assert THETA_A < 0
        assert DELTA_A == 0.0  # f_new == f(tau1) di curva
        assert RHO_A > 0  # tasso su: sconto maggiore su MtM negativo

    def test_giorni_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00,
                             90.00, 88.00, CURVA_TTF, DATA_NEW, 0,
                             R_OLD, R_NEW)


class TestPortafoglio486:
    def test_demo_b_totali(self):
        a = _F["mh486_portafoglio"](POS_B, CURVE_B, DATA_NEW, GIORNI,
                                    R_OLD, R_NEW)
        _approx(a["delta_mtm_tot"], D_MTM_B)
        _approx(a["theta_tot"], THETA_B)
        _approx(a["delta_tot"], DELTA_B)
        _approx(a["rho_tot"], RHO_B)
        _approx(a["residuo_tot"], RESIDUO_B)
        assert a["n_posizioni"] == 3

    def test_per_commodity(self):
        a = _F["mh486_portafoglio"](POS_B, CURVE_B, DATA_NEW, GIORNI,
                                    R_OLD, R_NEW)
        assert set(a["per_commodity"]) == {"TTF gas", "Power baseload DE"}
        tot = sum(b["delta_mtm"] for b in a["per_commodity"].values())
        _approx(tot, D_MTM_B)

    def test_curva_mancante(self):
        with pytest.raises(ValueError):
            _F["mh486_portafoglio"](POS_B, {"TTF gas": CURVA_TTF}, DATA_NEW,
                                    GIORNI, R_OLD, R_NEW)

    def test_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh486_portafoglio"]([], CURVE_B, DATA_NEW, GIORNI,
                                   R_OLD, R_NEW)


class TestVerdetto486:
    def test_demo_b(self):
        v = _F["mh486_verdetto"](POS_B, CURVE_B, DATA_NEW, GIORNI,
                                 R_OLD, R_NEW)
        assert v["verdetto"] == VERD_B
        _approx(v["spiegato_pct"], PCT_B)
        _approx(v["residuo_tot"], RESIDUO_B)
        assert v["giorni"] == float(GIORNI)

    def test_nessun_movimento(self):
        pos = [{"commodity": "TTF gas", "scadenza": "2027-01",
                "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 88.00,
                "f_old": 88.00, "f_new": 88.00}]
        curve = {"TTF gas": {"2026-11": 88.0, "2026-12": 88.0,
                             "2027-01": 88.0, "2027-02": 88.0}}
        v = _F["mh486_verdetto"](pos, curve, DATA_NEW, GIORNI, R_OLD, R_OLD)
        assert v["verdetto"] == "NESSUN MOVIMENTO"
        assert v["spiegato_pct"] is None

    def test_da_indagare(self):
        # curva t1 piatta a 88 ma il prezzo vecchio era 100: la forma della
        # curva e' cambiata -> residuo enorme -> DA INDAGARE
        pos = [{"commodity": "TTF gas", "scadenza": "2027-01",
                "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00,
                "f_old": 100.00, "f_new": 88.00}]
        curve = {"TTF gas": CURVA_PIATTA}
        v = _F["mh486_verdetto"](pos, curve, DATA_NEW, GIORNI, R_OLD, R_NEW)
        assert v["verdetto"] == VERD_C
        _approx(v["residuo_tot"], RESIDUO_C)
        assert abs(RESIDUO_C) > 0.20 * abs(v["delta_mtm_tot"])

    def test_chiavi(self):
        v = _F["mh486_verdetto"](POS_B, CURVE_B, DATA_NEW, GIORNI,
                                 R_OLD, R_NEW)
        assert set(v) == {"verdetto", "delta_mtm_tot", "spiegato_tot",
                          "residuo_tot", "spiegato_pct", "giorni"}
