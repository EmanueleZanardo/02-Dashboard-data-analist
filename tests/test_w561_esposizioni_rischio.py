"""Test tab561 'Esposizioni ai rischi e origine (IFRS 7.31)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh561_num", "mh561_str", "mh561_ge0", "mh561_tipo",
           "mh561_voce", "mh561_demo", "mh561_riepilogo")

TITLE561 = ("\U0001F9ED\U0001F4CA Esposizioni ai rischi e origine "
            "(IFRS 7.31)")


def _v(rid="R-1", tp="RISCHIO_MERCATO", es=1000000.0, ep=800000.0,
       og="origine", po="politiche", me="metodo"):
    return _F["mh561_voce"](rid, tp, es, ep, og, po, me)


class TestW561Validatori:
    def test_num_ok(self):
        assert _F["mh561_num"](2, "x") == 2.0
        assert _F["mh561_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh561_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh561_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh561_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh561_ge0"](0, "x") == 0.0

    def test_ge0_ko(self):
        with pytest.raises(ValueError):
            _F["mh561_ge0"](-0.01, "x")

    def test_tipo_ok(self):
        assert _F["mh561_tipo"]("rischio_mercato") == "RISCHIO_MERCATO"
        assert _F["mh561_tipo"]("RISCHIO_CREDITO") == "RISCHIO_CREDITO"
        assert _F["mh561_tipo"](" RISCHIO_LIQUIDITA ") == "RISCHIO_LIQUIDITA"

    def test_tipo_ko(self):
        for bad in ("RISCHIO_OPERATIVO", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh561_tipo"](bad)


class TestW561Voce:
    def test_voce_ok(self):
        v = _v()
        assert v["id"] == "R-1"
        assert v["tipo"] == "RISCHIO_MERCATO"
        assert v["esposizione"] == 1000000.0
        assert v["esposizione_precedente"] == 800000.0
        assert v["delta_pct"] == pytest.approx(0.25)

    def test_voce_delta_none(self):
        v = _v(ep=0.0)
        assert v["delta_pct"] is None

    def test_voce_testo_non_str(self):
        with pytest.raises(ValueError):
            _v(og=None)
        with pytest.raises(ValueError):
            _v(po=123)

    def test_voce_strip(self):
        v = _v(og="  abc  ")
        assert v["origine"] == "abc"


class TestW561Riepilogo:
    def test_demo(self):
        d = _F["mh561_demo"]()
        assert len(d) == 3
        r = _F["mh561_riepilogo"](d)
        assert r["n_voci"] == 3
        assert r["n_tipi"] == 3
        assert r["n_anomalie"] == 0
        assert r["esposizione_totale"] == pytest.approx(56900000.0)
        assert r["esposizione_precedente_totale"] == pytest.approx(
            51700000.0)
        assert r["delta_tot_pct"] == pytest.approx(
            5200000.0 / 51700000.0)
        assert r["analizzate"][0]["quota"] == pytest.approx(
            38200000.0 / 56900000.0)
        assert r["verdetto"] == "RISCHIO_MERCATO_DOMINANTE"
        assert [p["tipo"] for p in r["per_tipo"]] == [
            "RISCHIO_MERCATO", "RISCHIO_CREDITO", "RISCHIO_LIQUIDITA"]

    def test_demo_deterministica(self):
        assert _F["mh561_demo"]() == _F["mh561_demo"]()

    def test_tipo_duplicato(self):
        r = _F["mh561_riepilogo"]([_v("A-1"), _v("A-2")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a.lower()
                   for a in r["analizzate"][1]["anomalie"])

    def test_esposizione_nulla_con_informativa(self):
        r = _F["mh561_riepilogo"]([_v(es=0.0, ep=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nulla" in a.lower()
                   for a in r["analizzate"][0]["anomalie"])

    def test_testi_mancanti(self):
        r = _F["mh561_riepilogo"]([_v(og="", po="  ", me="")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 3

    def test_diversificato_soglia_alta(self):
        d = _F["mh561_demo"]()
        r = _F["mh561_riepilogo"](d, 0.99)
        assert r["verdetto"] == "ESPOSIZIONI_DIVERSIFICATE"

    def test_soglia_fuori_range(self):
        d = _F["mh561_demo"]()
        for bad in (0.0, 1.0, -0.1, 1.5):
            with pytest.raises(ValueError):
                _F["mh561_riepilogo"](d, bad)

    def test_vuota(self):
        r = _F["mh561_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"
        assert r["n_voci"] == 0
        assert r["n_anomalie"] == 0
        assert r["delta_tot_pct"] is None


class TestW561Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_561_presente(self):
        assert self._src().count(TITLE561) == 3

    def test_counts_561(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 808
        assert TITLE561 in titoli
        assert "tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808 = st.tabs([" in src

    def test_chiavi_561_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st561_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st561_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 12
