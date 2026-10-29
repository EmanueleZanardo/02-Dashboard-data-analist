"""Test tab544 'Collateral & garanzie reali (IFRS 7.15)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh544_num", "mh544_str", "mh544_bool", "mh544_dir",
           "mh544_tipo", "mh544_voce", "mh544_demo", "mh544_riepilogo")

TITLE544 = "🏦📥 Collateral & garanzie reali (IFRS 7.15)"


def _v(vid="V-1", d="x", cp="cp", esp=1000.0, dr="RICEVUTA", tp="CONTANTE",
       fv=0.0, esc=True, esc2=False):
    return {"id": vid, "descrizione": d, "controparte": cp,
            "esposizione_eur": esp, "direzione": dr, "tipo": tp,
            "fair_value_garanzia": fv, "escutibile": esc, "escussa": esc2}


class TestW544Validatori:
    def test_num_ok(self):
        assert _F["mh544_num"](2, "x") == 2.0
        assert _F["mh544_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh544_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh544_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh544_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh544_bool"](True, "x") is True
        for bad in (1, 0, "s", None):
            with pytest.raises(ValueError):
                _F["mh544_bool"](bad, "x")

    def test_dir_ok_ko(self):
        for ok in ("RICEVUTA", "DATA"):
            assert _F["mh544_dir"](ok, "x") == ok
        for bad in ("ricevuta", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh544_dir"](bad, "x")

    def test_tipo_ok_ko(self):
        for ok in ("CONTANTE", "TITOLI", "LETTERA_CREDITO", "PEGNO_CREDITI",
                   "PEGNO_SCORTE", "GARANZIA_CORPORATE", "ALTRO"):
            assert _F["mh544_tipo"](ok, "x") == ok
        for bad in ("CASH", "", None):
            with pytest.raises(ValueError):
                _F["mh544_tipo"](bad, "x")


class TestW544Voce:
    def test_copertura_calcolo(self):
        o = _F["mh544_voce"](_v(esp=8500000.0, fv=8925000.0))
        assert o["copertura"] == pytest.approx(1.05)
        assert o["esito"] == "COPERTA"
        assert o["anomalie"] == []

    def test_esiti_soglie(self):
        assert _F["mh544_voce"](_v(esp=1000.0, fv=900.0))["esito"] == \
            "SOTTO_GARANZIA"
        assert _F["mh544_voce"](_v(esp=1000.0, fv=499.0))["esito"] == "CRITICA"
        assert _F["mh544_voce"](_v(esp=1000.0, fv=0.0))["esito"] == \
            "NESSUNA_COPERTURA"

    def test_garanzia_senza_esposizione_anomalia(self):
        o = _F["mh544_voce"](_v(esp=0.0, fv=500.0))
        assert o["anomalie"] == ["garanzia senza esposizione"]
        assert o["copertura"] is None
        assert o["esito"] == "COPERTA"

    def test_escussa_non_escutibile_anomalia(self):
        o = _F["mh544_voce"](_v(esp=1000.0, fv=1000.0, esc=False,
                                esc2=True))
        assert len(o["anomalie"]) == 1
        assert "non escutibile" in o["anomalie"][0]

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh544_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(esp=-1.0))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(fv=-5.0))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(dr="ALTROVE"))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(tp="ORO"))


class TestW544Demo:
    def test_demo_verdetto(self):
        demo = _F["mh544_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["COLL-DE-001", "COLL-IT-002",
                                          "COLL-UK-003"]
        ri = _F["mh544_riepilogo"](demo)
        assert ri["esposizione_tot"] == pytest.approx(12700000.0)
        assert ri["garanzia_tot"] == pytest.approx(13125000.0)
        assert ri["copertura"] == pytest.approx(13125000.0 / 12700000.0)
        assert ri["verdetto"] == "COPERTURA_ADEGUATA"
        assert ri["n_anomalie"] == 0
        assert ri["per_esito"] == {"COPERTA": 2, "SOTTO_GARANZIA": 1}
        assert ri["per_direzione"]["RICEVUTA"]["n"] == 2
        assert ri["per_direzione"]["DATA"]["copertura"] == \
            pytest.approx(1.25)


class TestW544Riepilogo:
    def test_verdetto_da_rafforzare_anomalia(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=0.0, fv=500.0)])
        assert ri["verdetto"] == "COPERTURE_DA_RAFFORZARE"
        assert ri["n_anomalie"] == 1

    def test_verdetto_da_rafforzare_copertura_bassa(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=1000.0, fv=800.0)])
        assert ri["verdetto"] == "COPERTURE_DA_RAFFORZARE"

    def test_verdetto_tesa(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=1000.0, fv=950.0)])
        assert ri["verdetto"] == "COPERTURA_TESA"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh544_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh544_riepilogo"]("non-lista")


class TestW544Registry:
    def test_titolo_544_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE544) == 3

    def test_registry_tab_count_544(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 806
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 806

    def test_tab544_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806 = st.tabs([" in src
        assert "with tab544:" in src

    def test_chiavi_st544_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st544_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
