"""Test tab617 "⛽🌱 Biocarburanti (HVO): il premium per decarbonizzare".

I valori della demo sono calcolati a mano: flotta 500.000 L/anno,
premium HVO 0,25 eur/L, quota blend 100 %, emissione diesel
2,68 kgCO2e/L, riduzione GHG 85 %, benchmark carbonio 100 eur/t ->
litri HVO 500.000, costo aggiuntivo 125.000 eur/anno, tCO2e evitate
1.139, MAC ~109,75 eur/tCO2, incidenza 0,25 eur/L -> MARGINALE
(MAC sopra il benchmark del 9,7 % < 15 %).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh617_num", "mh617_nneg", "mh617_pos", "mh617_frac01",
           "mh617_litri_hvo", "mh617_costo_aggiuntivo",
           "mh617_tco2_evitate", "mh617_mac", "mh617_incidenza_l",
           "mh617_verdetto", "mh617_sensitivita", "mh617_demo")

TITLE617 = "⛽🌱 Biocarburanti (HVO): il premium per decarbonizzare"

# Demo: 500.000 L/anno, premium 0,25, blend 100 %, 2,68 kg/L, -85 %,
# benchmark 100 eur/t
DEMO = _F["mh617_demo"]()
LITRI_HVO = 500000.0             # 500000*1,0
COSTO = 125000.0                # 500000*0,25
TCO2 = 1139.0                   # 500000*2,68/1000*0,85
MAC = 109.74539069358999        # 125000/1139
INCIDENZA = 0.25                # 125000/500000


class TestW617Validatori:
    def test_num(self):
        assert _F["mh617_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh617_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh617_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh617_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh617_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh617_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh617_frac01"](1.0, "x") == 1.0
        assert _F["mh617_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh617_frac01"](1.5, "x")


class TestW617Calcoli:
    def test_litri_e_costo(self):
        assert _F["mh617_litri_hvo"](500000.0, 1.0) == LITRI_HVO
        assert _F["mh617_litri_hvo"](500000.0, 0.5) == 250000.0
        assert _F["mh617_costo_aggiuntivo"](500000.0, 0.25, 1.0) == COSTO
        assert _F["mh617_costo_aggiuntivo"](500000.0, 0.25, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh617_costo_aggiuntivo"](500000.0, -0.01, 1.0)

    def test_tco2(self):
        assert _F["mh617_tco2_evitate"](500000.0, 1.0, 2.68, 0.85) == TCO2
        assert _F["mh617_tco2_evitate"](500000.0, 0.0, 2.68, 0.85) == 0.0
        assert _F["mh617_tco2_evitate"](500000.0, 1.0, 2.68, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh617_tco2_evitate"](500000.0, 1.0, -2.68, 0.85)

    def test_mac(self):
        assert _F["mh617_mac"](COSTO, TCO2) == pytest.approx(MAC)
        # nessuna tonnellata abbattuta -> None (non divisione per zero)
        assert _F["mh617_mac"](COSTO, 0.0) is None
        assert _F["mh617_mac"](0.0, 0.0) is None
        with pytest.raises(ValueError):
            _F["mh617_mac"](-1.0, TCO2)

    def test_incidenza(self):
        assert _F["mh617_incidenza_l"](COSTO, 500000.0) == INCIDENZA
        with pytest.raises(ValueError):
            _F["mh617_incidenza_l"](COSTO, 0.0)

    def test_verdetto(self):
        v = _F["mh617_verdetto"](MAC, 100.0)
        assert v["verdetto"] == "MARGINALE"
        assert v["mac"] == pytest.approx(MAC)
        v2 = _F["mh617_verdetto"](90.0, 100.0)
        assert v2["verdetto"] == "CONVIENE"
        v3 = _F["mh617_verdetto"](100.0, 100.0)
        assert v3["verdetto"] == "CONVIENE"
        v4 = _F["mh617_verdetto"](114.99, 100.0)
        assert v4["verdetto"] == "MARGINALE"
        v5 = _F["mh617_verdetto"](115.01, 100.0)
        assert v5["verdetto"] == "NON_CONVIENE"
        v6 = _F["mh617_verdetto"](None, 100.0)
        assert v6["verdetto"] == "NON_CALCOLABILE"
        assert v6["mac"] is None
        with pytest.raises(ValueError):
            _F["mh617_verdetto"](-5.0, 100.0)


class TestW617Demo:
    def test_demo_end_to_end(self):
        d = DEMO
        lh = _F["mh617_litri_hvo"](d["litri_anno"], d["quota_blend"])
        ca = _F["mh617_costo_aggiuntivo"](d["litri_anno"],
                                         d["premium_eur_l"],
                                         d["quota_blend"])
        tc = _F["mh617_tco2_evitate"](d["litri_anno"], d["quota_blend"],
                                      d["kgco2_l"], d["riduzione_ghg"])
        mc = _F["mh617_mac"](ca, tc)
        assert lh == LITRI_HVO
        assert ca == COSTO
        assert tc == TCO2
        assert mc == pytest.approx(MAC)
        assert _F["mh617_incidenza_l"](ca, d["litri_anno"]) == INCIDENZA
        v = _F["mh617_verdetto"](mc, d["benchmark_eur_t"])
        assert v["verdetto"] == "MARGINALE"


class TestW617Sensitivita:
    def _args(self):
        return (500000.0, 2.68, 0.85, 100.0)

    def test_griglia(self):
        rows = _F["mh617_sensitivita"](*self._args(), [0.25], [1.0])
        assert len(rows) == 1
        r = rows[0]
        assert r["costo_aggiuntivo"] == COSTO
        assert r["tco2_evitate"] == TCO2
        assert r["mac"] == pytest.approx(MAC)
        assert r["verdetto"] == "MARGINALE"

    def test_mac_invariante_alla_quota(self):
        rows = _F["mh617_sensitivita"](*self._args(), [0.25],
                                       [0.25, 0.5, 1.0])
        macs = [r["mac"] for r in rows]
        assert all(m == pytest.approx(MAC) for m in macs)
        assert rows[0]["costo_aggiuntivo"] < rows[2]["costo_aggiuntivo"]

    def test_mac_cresce_col_premium(self):
        rows = _F["mh617_sensitivita"](*self._args(), [0.10, 0.40], [1.0])
        assert rows[0]["mac"] < rows[1]["mac"]
        assert rows[0]["verdetto"] == "CONVIENE"
        assert rows[1]["verdetto"] == "NON_CONVIENE"

    def test_quota_zero_mac_none(self):
        rows = _F["mh617_sensitivita"](*self._args(), [0.25], [0.0])
        assert rows[0]["mac"] is None
        assert rows[0]["verdetto"] == "NON_CALCOLABILE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh617_sensitivita"](*self._args(), [], [1.0])
        with pytest.raises(ValueError):
            _F["mh617_sensitivita"](*self._args(), [0.25], [])


class TestW617Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab617:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 816
        assert TITLE617 in titles
        assert TITLE617 in titles

    def test_chain(self):
        assert ", tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816 = st.tabs([" in self._src()
        assert "with tab617:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st617_[a-z0-9_]+", self._ui()))
        attese = {"st617_litri", "st617_prem", "st617_quota", "st617_kg",
                  "st617_rid", "st617_bench", "st617_tab", "st617_graf",
                  "st617_go", "st617_fig", "st617_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st617_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W617 (21/10/2026)')[1]
        sec = sec.split('# W616 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
