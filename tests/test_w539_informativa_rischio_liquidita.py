"""Test tab539 '💧📋 Informativa rischio di liquidità (IFRS 7.39)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh539_num", "mh539_str", "mh539_int0", "mh539_bucket",
           "mh539_passivita", "mh539_demo", "mh539_informativa")

TITLE539 = "💧📋 Informativa rischio di liquidità (IFRS 7.39)"


def _p(pid="P-1", d="x", vc=100000.0, fl=110000.0, me=24):
    return {"id": pid, "descrizione": d, "valore_contabile": vc,
            "flussi_non_attualizzati": fl, "mesi_scadenza": me}


class TestW539Validatori:
    def test_num_ok(self):
        assert _F["mh539_num"](2, "x") == 2.0
        assert _F["mh539_num"](-1.5, "x") == -1.5
        assert _F["mh539_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh539_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh539_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh539_str"](bad, "x")

    def test_int0_ok_ko(self):
        assert _F["mh539_int0"](0, "x") == 0
        assert _F["mh539_int0"](36, "x") == 36
        for bad in (True, 1.5, -1, "3", None, 2.0):
            with pytest.raises(ValueError):
                _F["mh539_int0"](bad, "x")

    def test_bucket_bounds(self):
        assert _F["mh539_bucket"](0) == "a vista"
        assert _F["mh539_bucket"](1) == "≤3 mesi"
        assert _F["mh539_bucket"](3) == "≤3 mesi"
        assert _F["mh539_bucket"](4) == "3-12 mesi"
        assert _F["mh539_bucket"](12) == "3-12 mesi"
        assert _F["mh539_bucket"](13) == "1-5 anni"
        assert _F["mh539_bucket"](60) == "1-5 anni"
        assert _F["mh539_bucket"](61) == ">5 anni"
        assert _F["mh539_bucket"](120) == ">5 anni"

    def test_bucket_ko(self):
        for bad in (-1, 1.5, True, None, "3", 3.0):
            with pytest.raises(ValueError):
                _F["mh539_bucket"](bad)


class TestW539Passivita:
    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh539_passivita"]("x")

    def test_chiave_mancante(self):
        _d = _p()
        del _d["flussi_non_attualizzati"]
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_d)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(vc=0.0))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(vc=-100.0))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(fl=-5.0))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(me=-1))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(me=2.5))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(pid=""))
        with pytest.raises(ValueError):
            _F["mh539_passivita"](_p(pid="   "))

    def test_normalizzazione_e_bucket(self):
        _r = _F["mh539_passivita"](_p(vc=200000.0, fl=215000.0,
                                      me=10))
        assert _r["valore_contabile"] == pytest.approx(200000.0)
        assert _r["flussi_non_attualizzati"] == pytest.approx(215000.0)
        assert _r["bucket"] == "3-12 mesi"
        assert _r["anomalie"] == []

    def test_anomalia_flussi_minori(self):
        _r = _F["mh539_passivita"](_p(vc=100000.0, fl=99000.0,
                                      me=24))
        assert any("flussi < valore contabile" in a
                   for a in _r["anomalie"])

    def test_anomalia_a_vista_flussi_nulli(self):
        _r = _F["mh539_passivita"](_p(vc=1000.0, fl=0.0, me=0))
        assert any("a vista con flussi nulli" in a
                   for a in _r["anomalie"])
        assert _r["bucket"] == "a vista"

    def test_anomalia_flussi_3x(self):
        _r = _F["mh539_passivita"](_p(vc=1000.0, fl=3500.0, me=48))
        assert any("> 3x" in a for a in _r["anomalie"])

    def test_flussi_uguali_ok(self):
        _r = _F["mh539_passivita"](_p(vc=120000.0, fl=120000.0,
                                      me=2))
        assert _r["anomalie"] == []
        assert _r["bucket"] == "≤3 mesi"


class TestW539Demo:
    def test_demo_verdetto(self):
        _demo = _F["mh539_demo"]()
        assert len(_demo) == 3
        assert [p["id"] for p in _demo] == ["DEB-BNK-001",
                                            "PAY-SUP-002",
                                            "DER-IRS-003"]
        _an = [_F["mh539_passivita"](p) for p in _demo]
        assert [_r["bucket"] for _r in _an] == ["1-5 anni", "≤3 mesi",
                                                "1-5 anni"]
        assert all(_r["anomalie"] == [] for _r in _an)
        _ri = _F["mh539_informativa"](_an)
        assert _ri["totale_valore_contabile"] == pytest.approx(700000.0)
        assert _ri["totale_flussi"] == pytest.approx(747000.0)
        assert _ri["copertura"] == pytest.approx(1.0671428, rel=1e-6)
        assert _ri["quota_breve_pct"] == pytest.approx(16.0642570,
                                                      rel=1e-6)
        assert _ri["per_bucket"]["≤3 mesi"] == pytest.approx(120000.0)
        assert _ri["per_bucket"]["1-5 anni"] == pytest.approx(627000.0)
        assert _ri["per_bucket"]["a vista"] == pytest.approx(0.0)
        assert _ri["esposizione_max"] == pytest.approx(500000.0)
        assert _ri["esposizione_max_id"] == "DEB-BNK-001"
        assert _ri["n_anomalie"] == 0
        assert _ri["verdetto"] == "LIQUIDITA_ADEGUATA"


class TestW539Informativa:
    def test_verdetto_critica(self):
        _an = [_F["mh539_passivita"](_p("A", "a", 1000.0, 1000.0, 6)),
               _F["mh539_passivita"](_p("B", "b", 200.0, 100.0, 36))]
        _ri = _F["mh539_informativa"](_an)
        assert _ri["quota_breve_pct"] == pytest.approx(90.9090909,
                                                      rel=1e-6)
        assert _ri["verdetto"] == "LIQUIDITA_CRITICA"

    def test_verdetto_tesa_da_quota(self):
        _an = [_F["mh539_passivita"](_p("A", "a", 500.0, 500.0, 6)),
               _F["mh539_passivita"](_p("B", "b", 500.0, 500.0, 36))]
        _ri = _F["mh539_informativa"](_an)
        assert _ri["verdetto"] == "LIQUIDITA_TESA"
        assert _ri["n_anomalie"] == 0

    def test_verdetto_tesa_da_anomalie(self):
        _an = [_F["mh539_passivita"](_p("A", "a", 1000.0, 900.0,
                                        36))]
        _ri = _F["mh539_informativa"](_an)
        assert _ri["verdetto"] == "LIQUIDITA_TESA"
        assert _ri["n_anomalie"] == 1

    def test_quota_breve_zero_tutto_lungo(self):
        _an = [_F["mh539_passivita"](_p("A", "a", 5000.0, 6000.0,
                                        84))]
        _ri = _F["mh539_informativa"](_an)
        assert _ri["quota_breve_pct"] == pytest.approx(0.0)
        assert _ri["per_bucket"][">5 anni"] == pytest.approx(6000.0)
        assert _ri["verdetto"] == "LIQUIDITA_ADEGUATA"

    def test_informativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh539_informativa"]([])
        with pytest.raises(ValueError):
            _F["mh539_informativa"]("x")
        with pytest.raises(ValueError):
            _F["mh539_informativa"](
                [_F["mh539_passivita"](_p())] * 5)
        with pytest.raises(ValueError):
            _F["mh539_informativa"](["x"])
        with pytest.raises(ValueError):
            _F["mh539_informativa"]([{"id": "A"}])


class TestW539Registry:
    def test_titolo_539_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE539) == 3

    def test_registry_tab_count_539(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 832
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 832

    def test_tab539_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830, tab831, tab832 = st.tabs([" in src
        assert "with tab539:" in src

    def test_chiavi_st539_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st539_[^\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
