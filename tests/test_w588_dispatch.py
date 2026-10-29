"""Test tab588 "🔋⏱️ Dispatch ottimale accumulo day-ahead": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh588_num", "mh588_num_nneg", "mh588_pos", "mh588_pctpos",
           "mh588_str", "mh588_parse24", "mh588_dispatch", "mh588_demo")

TITLE588 = "🔋⏱️ Dispatch ottimale accumulo day-ahead"


class TestW588Validatori:
    def test_num_ok(self):
        assert _F["mh588_num"](2, "x") == 2.0
        assert _F["mh588_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh588_num"](bad, "x")

    def test_num_nneg_ko(self):
        with pytest.raises(ValueError):
            _F["mh588_num_nneg"](-0.1, "x")
        assert _F["mh588_num_nneg"](0, "x") == 0.0

    def test_pos_ko(self):
        for bad in (0, -1.0):
            with pytest.raises(ValueError):
                _F["mh588_pos"](bad, "x")

    def test_pctpos_ok_ko(self):
        assert _F["mh588_pctpos"](92.0, "e") == 92.0
        assert _F["mh588_pctpos"](100, "e") == 100.0
        for bad in (0, -5.0, 100.1, "90"):
            with pytest.raises(ValueError):
                _F["mh588_pctpos"](bad, "e")

    def test_str_ko(self):
        for bad in (123, "   ", None):
            with pytest.raises(ValueError):
                _F["mh588_str"](bad, "x")

    def test_parse24_ok(self):
        t = ", ".join(["10"] * 12 + ["100"] * 12)
        assert _F["mh588_parse24"](t, "p") == [10.0] * 12 + [100.0] * 12
        t2 = "\n".join(str(i) for i in range(24))
        assert _F["mh588_parse24"](t2, "p") == [float(i) for i in range(24)]
        t3 = "; ".join(["1.5"] * 24)
        assert _F["mh588_parse24"](t3, "p") == [1.5] * 24

    def test_parse24_ko(self):
        with pytest.raises(ValueError):
            _F["mh588_parse24"](", ".join(["1"] * 23), "p")
        with pytest.raises(ValueError):
            _F["mh588_parse24"](", ".join(["1"] * 24 + ["2"]), "p")
        with pytest.raises(ValueError):
            _F["mh588_parse24"](", ".join(["-1"] + ["1"] * 23), "p")
        with pytest.raises(ValueError):
            _F["mh588_parse24"](", ".join(["a"] + ["1"] * 23), "p")


class TestW588Dispatch:
    def _blocco(self):
        return [10.0] * 12 + [100.0] * 12

    def test_blocco_spread(self):
        # Carica 10 MWh a 10 €, scarica a 100 €: 10*(100-10) = 900
        r = _F["mh588_dispatch"](self._blocco(), 10.0, 100.0, 100.0,
                                 100.0, 0.0)
        assert r["profitto"] == pytest.approx(900.0, abs=1e-4)
        assert r["cicli_equivalenti"] == pytest.approx(1.0, abs=1e-6)
        assert r["throughput_ac"] == pytest.approx(20.0, abs=1e-6)
        assert r["verdetto"] == "ARBITRAGGIO_PROFITTEVOLE"
        assert len(r["ore"]) == 24

    def test_efficienza_90(self):
        # 10*(100*0.9 - 10/0.9) = 788.888...
        r = _F["mh588_dispatch"](self._blocco(), 10.0, 100.0, 90.0,
                                 90.0, 0.0)
        assert r["profitto"] == pytest.approx(788.8888889, abs=1e-3)

    def test_prezzi_piatti(self):
        r = _F["mh588_dispatch"]([50.0] * 24, 10.0, 100.0, 100.0,
                                 100.0, 0.0)
        assert r["profitto"] == 0.0
        assert r["throughput_ac"] == 0.0
        assert r["verdetto"] == "NESSUN_ARBITRAGGIO"
        assert any("piatti" in n for n in r["note"])

    def test_degrado_annulla_arbitraggio(self):
        r = _F["mh588_dispatch"](self._blocco(), 10.0, 100.0, 100.0,
                                 100.0, 0.0, c_deg=100.0)
        assert r["profitto"] == 0.0
        assert r["throughput_ac"] == 0.0
        assert r["verdetto"] == "NESSUN_ARBITRAGGIO"

    def test_potenza_limitante(self):
        # Una sola ora a 10 € e una a 100 €, P=5 MW: 5*(100-10) = 450
        p = [10.0] + [50.0] * 22 + [100.0]
        r = _F["mh588_dispatch"](p, 10.0, 5.0, 100.0, 100.0, 0.0)
        assert r["profitto"] == pytest.approx(450.0, abs=1e-4)
        assert r["energia_scaricata_soc"] == pytest.approx(5.0, abs=1e-6)

    def test_picco_prima_del_minimo(self):
        # Non si viaggia nel tempo: con SoC pieno si scarica al picco
        r = _F["mh588_dispatch"]([100.0] * 12 + [10.0] * 12, 10.0,
                                 100.0, 100.0, 100.0, 10.0)
        assert r["profitto"] == pytest.approx(1000.0, abs=1e-4)
        assert r["soc_finale"] == pytest.approx(0.0, abs=1e-6)

    def test_soc_finale_vincolato(self):
        r = _F["mh588_dispatch"](self._blocco(), 10.0, 100.0, 100.0,
                                 100.0, 0.0, soc_finale=0.0)
        assert r["profitto"] == pytest.approx(900.0, abs=1e-4)
        assert r["soc_finale"] == pytest.approx(0.0, abs=1e-6)

    def test_monotona_crescente(self):
        p = [10.0 + i * (90.0 / 23) for i in range(24)]
        r = _F["mh588_dispatch"](p, 10.0, 100.0, 100.0, 100.0, 0.0)
        assert r["profitto"] == pytest.approx(900.0, abs=1e-4)
        # Carica tutta all'ora 0, scarica tutta all'ora 23
        assert r["ore"][0]["delta_soc"] == pytest.approx(10.0, abs=1e-6)
        assert r["ore"][23]["delta_soc"] == pytest.approx(-10.0,
                                                          abs=1e-6)

    def test_vincoli_soc_rispettati(self):
        dm = _F["mh588_demo"]()
        r = _F["mh588_dispatch"](dm["prezzi"], dm["e_max"], dm["p_max"],
                                 dm["eta_c_pct"], dm["eta_d_pct"],
                                 dm["soc_ini"], soc_min=dm["soc_min"],
                                 soc_max=dm["soc_max"],
                                 c_deg=dm["c_deg"],
                                 livelli=dm["livelli"])
        for o in r["ore"]:
            assert 2.0 - 1e-9 <= o["soc_inizio"] <= 18.0 + 1e-9
            assert 2.0 - 1e-9 <= o["soc_fine"] <= 18.0 + 1e-9
            assert abs(o["delta_soc"]) <= 10.0 + 1e-9
        assert abs(sum(o["cash"] for o in r["ore"]) - r["profitto"]) < 1e-3

    def test_demo_profittevole(self):
        dm = _F["mh588_demo"]()
        r = _F["mh588_dispatch"](dm["prezzi"], dm["e_max"], dm["p_max"],
                                 dm["eta_c_pct"], dm["eta_d_pct"],
                                 dm["soc_ini"], soc_min=dm["soc_min"],
                                 soc_max=dm["soc_max"],
                                 c_deg=dm["c_deg"],
                                 livelli=dm["livelli"])
        assert r["verdetto"] == "ARBITRAGGIO_PROFITTEVOLE"
        assert r["profitto"] > 0.0
        assert r["cicli_equivalenti"] > 0.0
        assert r["profitto"] == pytest.approx(
            r["ricavo_lordo_energia"] - r["costo_degrado"], abs=1e-3)

    def test_degrado_contabilizzato(self):
        r = _F["mh588_dispatch"](self._blocco(), 10.0, 100.0, 100.0,
                                 100.0, 0.0, c_deg=2.0)
        assert r["costo_degrado"] == pytest.approx(40.0, abs=1e-4)
        assert r["profitto"] == pytest.approx(860.0, abs=1e-3)

    def test_input_ko(self):
        d = _F["mh588_dispatch"]
        base = dict(e_max=10.0, p_max=100.0, eta_c_pct=100.0,
                    eta_d_pct=100.0, soc_ini=0.0)
        with pytest.raises(ValueError):
            d([1.0] * 23, **base)                      # non 24 prezzi
        with pytest.raises(ValueError):
            d([-1.0] + [1.0] * 23, **base)              # prezzo negativo
        with pytest.raises(ValueError):
            d(self._blocco(), e_max=0, **{k: v for k, v in base.items()
                                          if k != "e_max"})
        with pytest.raises(ValueError):
            d(self._blocco(), eta_c_pct=0, **{k: v for k, v in
                                              base.items()
                                              if k != "eta_c_pct"})
        with pytest.raises(ValueError):
            d(self._blocco(), eta_d_pct=101.0, **{k: v for k, v in
                                                  base.items()
                                                  if k != "eta_d_pct"})
        with pytest.raises(ValueError):
            d(self._blocco(), soc_ini=11.0, **{k: v for k, v in
                                               base.items()
                                               if k != "soc_ini"})
        with pytest.raises(ValueError):
            d(self._blocco(), soc_min=6.0, soc_max=5.0,
              **{k: v for k, v in base.items()})
        with pytest.raises(ValueError):
            d(self._blocco(), soc_min=5.0, soc_max=5.0,
              **{k: v for k, v in base.items()})
        with pytest.raises(ValueError):
            d(self._blocco(), c_deg=-1.0, **{k: v for k, v in
                                             base.items()})
        with pytest.raises(ValueError):
            d(self._blocco(), livelli=9, **{k: v for k, v in
                                            base.items()})
        with pytest.raises(ValueError):
            d(self._blocco(), soc_finale=11.0, **{k: v for k, v in
                                                  base.items()})
        with pytest.raises(ValueError):
            d(self._blocco(), True, 100.0, 100.0, 100.0, 0.0)  # bool


class TestW588Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_presente(self):
        assert f'"{TITLE588}"' in self._src()

    def test_conteggio_tab(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 801
        assert TITLE588 in titles

    def test_chain_tab_var(self):
        assert ", tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801 = st.tabs([" in self._src()
        assert "with tab588:" in self._src()

    def test_chiavi_univoche(self):
        keys = set(re.findall(r"st588_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
