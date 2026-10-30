"""Test tab548 'Fair value vs valore contabile (IFRS 7.25)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh548_num", "mh548_str", "mh548_classe", "mh548_metodo",
           "mh548_voce", "mh548_demo", "mh548_riepilogo")

TITLE548 = "💲📊 Fair value vs valore contabile (IFRS 7.25)"


def _v(vid="V-1", d="x", cl="CREDITI", vc=1000.0, fv=1000.0,
       mt="LIVELLO_2"):
    return {"id": vid, "descrizione": d, "classe": cl,
            "valore_contabile": vc, "fair_value": fv, "metodo": mt}


class TestW548Validatori:
    def test_num_ok(self):
        assert _F["mh548_num"](2, "x") == 2.0
        assert _F["mh548_num"](0, "x") == 0.0
        assert _F["mh548_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh548_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh548_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh548_str"](bad, "x")

    def test_classe_ok_ko(self):
        for ok in ("DERIVATI_TRADING", "PPA_FORWARD", "CREDITI",
                   "CASSA_DISPONIBILITA", "FINANZIAMENTI",
                   "ALTRE_PASSIVITA"):
            assert _F["mh548_classe"](ok, "x") == ok
        for bad in ("CREDITI_PP", "crediti", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh548_classe"](bad, "x")

    def test_metodo_ok_ko(self):
        for ok in ("LIVELLO_1", "LIVELLO_2", "LIVELLO_3"):
            assert _F["mh548_metodo"](ok, "x") == ok
        for bad in ("LIVELLO_4", "livello_1", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh548_metodo"](bad, "x")


class TestW548Voce:
    def test_scostamento_calcolo(self):
        o = _F["mh548_voce"](_v(vc=1000.0, fv=1120.0))
        assert o["scostamento"] == pytest.approx(120.0)
        assert o["scostamento_pct"] == pytest.approx(0.12)
        assert any("10%" in a for a in o["anomalie"])

    def test_allineato_ok(self):
        o = _F["mh548_voce"](_v(vc=2300000.0, fv=2300000.0, mt="LIVELLO_1"))
        assert o["scostamento"] == pytest.approx(0.0)
        assert o["scostamento_pct"] == pytest.approx(0.0)
        assert o["anomalie"] == []

    def test_contenuto_ok(self):
        o = _F["mh548_voce"](_v(vc=1000.0, fv=1040.0, mt="LIVELLO_2"))
        assert o["anomalie"] == []
        assert o["scostamento_pct"] == pytest.approx(0.04)

    def test_anomalia_10pct_boundary(self):
        o = _F["mh548_voce"](_v(vc=1000.0, fv=1100.0))
        assert o["anomalie"] == []
        o2 = _F["mh548_voce"](_v(vc=1000.0, fv=1100.01))
        assert any("10%" in a for a in o2["anomalie"])

    def test_anomalia_vc_zero(self):
        o = _F["mh548_voce"](_v(vc=0.0, fv=500.0))
        assert o["scostamento_pct"] is None
        assert any("senza valore contabile" in a for a in o["anomalie"])

    def test_zero_zero_ok(self):
        o = _F["mh548_voce"](_v(vc=0.0, fv=0.0))
        assert o["scostamento_pct"] == pytest.approx(0.0)
        assert o["anomalie"] == []

    def test_anomalia_livello3_boundary(self):
        o = _F["mh548_voce"](_v(vc=1000.0, fv=1050.0, mt="LIVELLO_3"))
        assert o["anomalie"] == []
        o2 = _F["mh548_voce"](_v(vc=1000.0, fv=1050.01, mt="LIVELLO_3"))
        assert any("livello 3" in a for a in o2["anomalie"])

    def test_livello3_sotto_10pct_solo_sua_anomalia(self):
        o = _F["mh548_voce"](_v(vc=1000.0, fv=1070.0, mt="LIVELLO_3"))
        assert len(o["anomalie"]) == 1
        assert "livello 3" in o["anomalie"][0]

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh548_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh548_voce"](_v(vc=-1.0))
        with pytest.raises(ValueError):
            _F["mh548_voce"](_v(fv=-5.0))
        with pytest.raises(ValueError):
            _F["mh548_voce"](_v(cl="X"))
        with pytest.raises(ValueError):
            _F["mh548_voce"](_v(mt="X"))
        with pytest.raises(ValueError):
            _F["mh548_voce"](_v(vid=""))


class TestW548Demo:
    def test_demo_verdetto(self):
        demo = _F["mh548_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["PPA-DE-001", "FIN-IT-002",
                                          "TRD-UK-003"]
        ri = _F["mh548_riepilogo"](demo)
        assert ri["vc_tot"] == pytest.approx(59300000.0)
        assert ri["fv_tot"] == pytest.approx(58400000.0)
        assert ri["scost_tot"] == pytest.approx(-900000.0)
        assert ri["quota_scost"] == pytest.approx(900000.0 / 59300000.0)
        assert ri["verdetto"] == "VALORI_ALLINEATI"
        assert ri["n_anomalie"] == 0
        assert ri["per_classe"]["FINANZIAMENTI"]["scost"] == pytest.approx(
            -1800000.0)
        assert ri["per_classe"]["PPA_FORWARD"]["scost"] == pytest.approx(
            900000.0)


class TestW548Riepilogo:
    def test_verdetto_anomalia_scostamento(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1250.0)])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_verdetto_anomalia_boundary(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1100.0)])
        assert ri["verdetto"] == "SCOSTAMENTI_TESI"
        ri2 = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1100.01)])
        assert ri2["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_verdetto_teso_boundary(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1050.0)])
        assert ri["verdetto"] == "VALORI_ALLINEATI"
        ri2 = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1050.01)])
        assert ri2["verdetto"] == "SCOSTAMENTI_TESI"

    def test_verdetto_allineati(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", vc=1000.0, fv=1000.0)])
        assert ri["verdetto"] == "VALORI_ALLINEATI"
        assert ri["quota_scost"] == pytest.approx(0.0)

    def test_nessuno_strumento(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", vc=0.0, fv=0.0)])
        assert ri["verdetto"] == "NESSUNO_STRUMENTO"

    def test_per_classe(self):
        ri = _F["mh548_riepilogo"]([_v(vid="A", cl="FINANZIAMENTI",
                                       vc=800.0, fv=760.0),
                                    _v(vid="B", cl="FINANZIAMENTI",
                                       vc=200.0, fv=215.0)])
        assert set(ri["per_classe"]) == {"FINANZIAMENTI"}
        assert ri["per_classe"]["FINANZIAMENTI"]["vc"] == pytest.approx(
            1000.0)
        assert ri["per_classe"]["FINANZIAMENTI"]["fv"] == pytest.approx(
            975.0)
        assert ri["per_classe"]["FINANZIAMENTI"]["scost"] == pytest.approx(
            -25.0)
        assert ri["verdetto"] == "VALORI_ALLINEATI"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh548_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh548_riepilogo"]("non-lista")


class TestW548Registry:
    def test_titolo_548_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE548) == 3

    def test_registry_tab_count_548(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 808
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 808

    def test_chain_estesa(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808 = st.tabs([" in src
