"""Test tab536 '🔁🏦 Modifica di passività (IFRS 9 3.3.2)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh536_num", "mh536_pct", "mh536_str", "mh536_bool",
           "mh536_flussi", "mh536_pv", "mh536_passivita",
           "mh536_test_10pct", "mh536_demo")

TITLE536 = "🔁🏦 Modifica di passività (IFRS 9 3.3.2)"


def _fl(*pairs):
    return [{"periodo": t, "flusso": c} for t, c in pairs]


def _p(cid="P-1", d="x", vc=10000.0, tie=5.0, fo=None, fn=None,
       cn=0.0, fv=9500.0):
    return {"id": cid, "descrizione": d, "valore_contabile": vc,
            "tie_pct": tie,
            "flussi_originali": fo if fo is not None else _fl((1, 1000.0)),
            "flussi_nuovi": fn if fn is not None else _fl((1, 900.0)),
            "commissioni_nette": cn, "fv_nuova_passivita": fv}


class TestW536Validatori:
    def test_num_ok(self):
        assert _F["mh536_num"](2, "x") == 2.0
        assert _F["mh536_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh536_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh536_pct"](0.0, "x") == 0.0
        assert _F["mh536_pct"](100.0, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "50", None):
            with pytest.raises(ValueError):
                _F["mh536_pct"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh536_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh536_bool"](True, "x") is True
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh536_bool"](bad, "x")

    def test_flussi_ok(self):
        _out = _F["mh536_flussi"](
            [{"periodo": 1, "flusso": 100}, {"periodo": 2.5, "flusso": -50}],
            "f")
        assert _out == [{"periodo": 1.0, "flusso": 100.0},
                        {"periodo": 2.5, "flusso": -50.0}]

    def test_flussi_ko(self):
        _v = _F["mh536_flussi"]
        with pytest.raises(ValueError):
            _v("no", "f")
        with pytest.raises(ValueError):
            _v([], "f")
        with pytest.raises(ValueError):
            _v([{"periodo": 1}], "f")
        with pytest.raises(ValueError):
            _v([{"periodo": 0, "flusso": 10}], "f")
        with pytest.raises(ValueError):
            _v([{"periodo": -1, "flusso": 10}], "f")
        with pytest.raises(ValueError):
            _v([{"periodo": 1, "flusso": 0}], "f")
        with pytest.raises(ValueError):
            _v([{"periodo": True, "flusso": 10}], "f")
        with pytest.raises(ValueError):
            _v(["x"], "f")

    def test_pv_par(self):
        # cedola 100 + 1100 a 2 anni al 10% = bond a par 1000
        assert _F["mh536_pv"](_fl((1, 100.0), (2, 1100.0)), 10.0) == \
            pytest.approx(1000.0)

    def test_pv_tie_zero(self):
        assert _F["mh536_pv"](_fl((1, 300.0), (2, 700.0)), 0.0) == 1000.0

    def test_pv_tie_out_of_range(self):
        for bad in (100.0, -1.0, "5"):
            with pytest.raises(ValueError):
                _F["mh536_pv"](_fl((1, 100.0)), bad)


class TestW536Passivita:
    def test_passivita_ok(self):
        _p0 = _F["mh536_passivita"](_p())
        assert _p0["id"] == "P-1" and _p0["valore_contabile"] == 10000.0

    def test_passivita_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh536_passivita"]("x")

    def test_passivita_chiavi_mancanti(self):
        _d = _p()
        del _d["tie_pct"]
        with pytest.raises(ValueError):
            _F["mh536_passivita"](_d)

    def test_passivita_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh536_passivita"](_p(cid="  "))

    def test_passivita_valore_contabile_ko(self):
        for bad in (0.0, -1.0, True):
            with pytest.raises(ValueError):
                _F["mh536_passivita"](_p(vc=bad))

    def test_passivita_tie_ko(self):
        for bad in (100.0, -0.5, "5"):
            with pytest.raises(ValueError):
                _F["mh536_passivita"](_p(tie=bad))

    def test_passivita_commissioni_ko(self):
        with pytest.raises(ValueError):
            _F["mh536_passivita"](_p(cn=-1.0))

    def test_passivita_fv_ko(self):
        for bad in (0.0, -5.0):
            with pytest.raises(ValueError):
                _F["mh536_passivita"](_p(fv=bad))


class TestW536Test10pct:
    def test_non_sostanziale(self):
        _a5 = (1 - 1.05 ** -5) / 0.05
        _pv_o = 500000.0 * _a5 + 10000000.0 / 1.05 ** 5
        _pv_n = 480000.0 * _a5 + 10000000.0 / 1.05 ** 5 + 50000.0
        _r = _F["mh536_test_10pct"](_F["mh536_demo"]()[0])
        assert _r["pv_originale"] == pytest.approx(_pv_o)
        assert _r["pv_nuovi"] == pytest.approx(_pv_n)
        assert _r["sostanziale"] is False
        assert _r["esito"] == "MODIFICA_NON_SOSTANZIALE"
        assert _r["diff_pct"] < 10.0
        assert _r["utile_perdita"] == pytest.approx(10000000.0 - _pv_n)

    def test_sostanziale(self):
        _a10 = (1 - 1.05 ** -10) / 0.05
        _pv_n = 300000.0 * _a10 + 10000000.0 / 1.05 ** 10 + 100000.0
        _r = _F["mh536_test_10pct"](_F["mh536_demo"]()[1])
        assert _r["pv_nuovi"] == pytest.approx(_pv_n)
        assert _r["sostanziale"] is True
        assert _r["esito"] == "DERECOGNITION"
        assert _r["diff_pct"] >= 10.0
        assert _r["utile_perdita"] == pytest.approx(1400000.0)

    def test_soglia_esatta_10(self):
        # tie 0%: 1000 -> 900 = esattamente 10% -> sostanziale (>= 10)
        _r = _F["mh536_test_10pct"](
            _p(tie=0.0, fo=_fl((1, 1000.0)), fn=_fl((1, 900.0)), fv=950.0))
        assert _r["diff_pct"] >= 10.0
        assert _r["sostanziale"] is True
        assert _r["esito"] == "DERECOGNITION"

    def test_sotto_soglia(self):
        _r = _F["mh536_test_10pct"](
            _p(tie=0.0, fo=_fl((1, 1000.0)), fn=_fl((1, 900.001))))
        assert _r["diff_pct"] < 10.0
        assert _r["sostanziale"] is False
        assert _r["esito"] == "MODIFICA_NON_SOSTANZIALE"

    def test_diff_assoluta_positiva(self):
        # pv nuovi MAGGIORE degli originali: la differenza e' in valore
        # assoluto, non sostanziale sotto soglia -> utile negativo
        _r = _F["mh536_test_10pct"](
            _p(vc=1000.0, tie=0.0, fo=_fl((1, 1000.0)),
               fn=_fl((1, 1050.0))))
        assert _r["diff_pct"] == pytest.approx(5.0)
        assert _r["sostanziale"] is False
        assert _r["utile_perdita"] == pytest.approx(-50.0)

    def test_commissioni_incluse(self):
        _r = _F["mh536_test_10pct"](
            _p(tie=0.0, fo=_fl((1, 1000.0)), fn=_fl((1, 900.0)), cn=50.0))
        assert _r["pv_nuovi"] == pytest.approx(950.0)
        assert _r["diff_pct"] == pytest.approx(5.0)
        assert _r["esito"] == "MODIFICA_NON_SOSTANZIALE"

    def test_pv_orig_nullo(self):
        with pytest.raises(ValueError):
            _F["mh536_test_10pct"](
                _p(tie=0.0, fo=_fl((1, 500.0), (1, -500.0))))

    def test_demo_due_casi(self):
        _demo = _F["mh536_demo"]()
        assert len(_demo) == 2
        _esiti = [_F["mh536_test_10pct"](_d)["esito"] for _d in _demo]
        assert _esiti == ["MODIFICA_NON_SOSTANZIALE", "DERECOGNITION"]

    def test_nota_contabile(self):
        _demo = _F["mh536_demo"]()
        _n1 = _F["mh536_test_10pct"](_demo[0])["nota_contabile"]
        _n2 = _F["mh536_test_10pct"](_demo[1])["nota_contabile"]
        assert "B3.3.6" in _n1 and "B3.3.6" in _n2
        assert "NON sostanziale" in _n1
        assert "SOSTANZIALE" in _n2


class TestW536Registry:
    def test_titolo_536_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE536) == 3

    def test_registry_tab_count_536(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 776
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 776

    def test_tab536_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776 = st.tabs([" in src
        assert "with tab536:" in src

    def test_chiavi_st536_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st536_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
