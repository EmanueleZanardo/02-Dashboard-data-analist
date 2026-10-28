"""Test tab559 'FVA: funding valuation adjustment del portafoglio': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh559_num", "mh559_str", "mh559_ge0", "mh559_bps", "mh559_csa",
           "mh559_netting", "mh559_demo", "mh559_riepilogo")

TITLE559 = "\U0001F4B8\U0001F4CA FVA: funding valuation adjustment del portafoglio"


def _n(nid="N-1", cp="CP", ee=(1000000.0, 0.0, 0.0, 0.0, 0.0, 0.0),
      sp=100.0, ta=0.0, cs="CSA_NO"):
    return _F["mh559_netting"](nid, cp, ee, sp, ta, cs)


class TestW559Validatori:
    def test_num_ok(self):
        assert _F["mh559_num"](2, "x") == 2.0
        assert _F["mh559_num"](0, "x") == 0.0
        assert _F["mh559_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh559_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh559_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh559_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh559_ge0"](0, "x") == 0.0

    def test_bps_ok(self):
        assert _F["mh559_bps"](0) == 0.0
        assert _F["mh559_bps"](10000) == 10000.0

    def test_bps_ko(self):
        for bad in (-1, 10000.01, "100"):
            with pytest.raises(ValueError):
                _F["mh559_bps"](bad)

    def test_csa_ok(self):
        assert _F["mh559_csa"]("csa_si") == "CSA_SI"
        assert _F["mh559_csa"]("CSA_NO") == "CSA_NO"

    def test_csa_ko(self):
        for bad in (None, "", "CSA_FORSE"):
            with pytest.raises(ValueError):
                _F["mh559_csa"](bad)


class TestW559Netting:
    def test_ok_semplice(self):
        n = _n()
        assert n["id"] == "N-1"
        assert n["controparte"] == "CP"
        assert n["ee"] == [1000000.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        assert n["spread_bps"] == 100.0
        assert n["tasso_pct"] == 0.0
        assert n["csa"] == "CSA_NO"
        assert n["ee_totale"] == 1000000.0
        # 1e6 * 1% * 0.25 anni * DF=1
        assert n["fva_lordo"] == pytest.approx(2500.0)
        assert n["fva"] == pytest.approx(2500.0)

    def test_csa_dimezza(self):
        a = _n(cs="CSA_NO")
        b = _n(cs="CSA_SI")
        assert b["fva"] == pytest.approx(a["fva"] * 0.5)
        assert b["fva_lordo"] == pytest.approx(a["fva_lordo"])

    def test_sconto_riduce(self):
        a = _n(ta=0.0)
        b = _n(ta=10.0)
        assert b["fva"] < a["fva"]

    def test_ko(self):
        with pytest.raises(ValueError):
            _n(nid="  ")
        with pytest.raises(ValueError):
            _n(cp="")
        with pytest.raises(ValueError):
            _n(ee=(1.0, 2.0))
        with pytest.raises(ValueError):
            _n(ee=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))
        with pytest.raises(ValueError):
            _n(ee=(100.0, -1.0, 0.0, 0.0, 0.0, 0.0))
        with pytest.raises(ValueError):
            _n(sp=10001.0)
        with pytest.raises(ValueError):
            _n(cs="BOH")


class TestW559Riepilogo:
    def test_demo(self):
        d = _F["mh559_demo"]()
        assert len(d) == 4
        r = _F["mh559_riepilogo"](d)
        assert r["n_netting"] == 4
        assert r["n_anomalie"] == 0
        assert r["ee_totale"] == pytest.approx(64000000.0)
        assert r["fva_totale"] == pytest.approx(389147.2, rel=1e-4)
        assert r["fva_su_ee"] == pytest.approx(0.00608, rel=1e-3)
        assert r["verdetto"] == "FVA_CONTENUTO"
        assert len(r["analizzati"]) == 4

    def test_id_duplicato(self):
        r = _F["mh559_riepilogo"]([_n("DUP"), _n("dup")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a.lower()
                   for a in r["analizzati"][1]["anomalie"])

    def test_ee_nullo(self):
        r = _F["mh559_riepilogo"](
            [_n(ee=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"
        assert r["n_anomalie"] == 1

    def test_spread_nullo(self):
        r = _F["mh559_riepilogo"]([_n(sp=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["fva_totale"] == 0.0

    def test_significativo(self):
        r = _F["mh559_riepilogo"]([_n(sp=10000.0)])
        assert r["fva_su_ee"] >= 0.02
        assert r["verdetto"] == "FVA_SIGNIFICATIVO"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh559_riepilogo"]([])


class TestW559Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_559_presente(self):
        assert self._src().count(TITLE559) == 3

    def test_counts_559(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 780
        assert TITLE559 in titoli
        assert "tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780 = st.tabs([" in src

    def test_chiavi_559_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st559_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st559_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
