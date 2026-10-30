"""Test tab587 "M&V IPMVP: verifica dei risparmi energetici": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh587_num", "mh587_num_nneg", "mh587_pos", "mh587_str",
           "mh587_parse12", "mh587_ols", "mh587_tcritico",
           "mh587_baseline_aggiustata", "mh587_verifica", "mh587_demo")

TITLE587 = "🧾⚖️ M&V IPMVP: verifica dei risparmi energetici"


class TestW587Validatori:
    def test_num_ok(self):
        assert _F["mh587_num"](2, "x") == 2.0
        assert _F["mh587_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh587_num"](bad, "x")

    def test_num_nneg_ko(self):
        for bad in (-0.1, True, "x", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh587_num_nneg"](bad, "x")
        assert _F["mh587_num_nneg"](0.0, "x") == 0.0

    def test_pos_ko(self):
        for bad in (0.0, -1.0, True, "x", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh587_pos"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh587_str"](bad, "x")


class TestW587Parse12:
    def test_ok(self):
        v = _F["mh587_parse12"]("1, 2;3\n4 5,6,7,8,9,10,11,12", "p")
        assert v == [float(i) for i in range(1, 13)]

    def test_conteggio_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_parse12"]("1,2,3", "p")
        with pytest.raises(ValueError):
            _F["mh587_parse12"](", ".join(["1"] * 13), "p")

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_parse12"]("1, -2, " + ", ".join(["3"] * 10), "p")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_parse12"]("1, x, " + ", ".join(["3"] * 10), "p")


class TestW587Ols:
    def test_retta_esatta(self):
        o = _F["mh587_ols"]([1, 2, 3, 4, 5], [3, 5, 7, 9, 11])
        assert o["pendenza"] == pytest.approx(2.0)
        assert o["intercetta"] == pytest.approx(1.0)
        assert o["r2"] == pytest.approx(1.0)
        assert o["se_residuo"] == pytest.approx(0.0)
        assert o["n"] == 5

    def test_r2_debole(self):
        o = _F["mh587_ols"]([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
        assert o["pendenza"] == pytest.approx(0.6)
        assert o["intercetta"] == pytest.approx(2.2)
        assert o["r2"] == pytest.approx(0.6)

    def test_n_minimo_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_ols"]([1, 2], [3, 4])

    def test_driver_costante_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_ols"]([5, 5, 5, 5], [1, 2, 3, 4])

    def test_lunghezze_diverse_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_ols"]([1, 2, 3], [1, 2])


class TestW587TCritico:
    def test_valori_noti(self):
        assert _F["mh587_tcritico"](10, 95) == pytest.approx(2.228)
        assert _F["mh587_tcritico"](1, 90) == pytest.approx(6.314)
        assert _F["mh587_tcritico"](30, 99) == pytest.approx(2.750)

    def test_oltre_30_normale(self):
        assert _F["mh587_tcritico"](31, 95) == pytest.approx(1.960)
        assert _F["mh587_tcritico"](100, 99) == pytest.approx(2.576)

    def test_livello_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_tcritico"](10, 80)

    def test_df_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_tcritico"](0, 95)
        with pytest.raises(ValueError):
            _F["mh587_tcritico"](True, 95)


class TestW587BaselineAggiustata:
    def test_ok(self):
        adj = _F["mh587_baseline_aggiustata"](
            {"pendenza": 2.0, "intercetta": 10.0}, [0.0, 5.0])
        assert adj == pytest.approx([10.0, 20.0])

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh587_baseline_aggiustata"](
                {"pendenza": 2.0, "intercetta": 10.0}, [])


class TestW587Verifica:
    def _demo(self):
        return _F["mh587_demo"]()

    def test_demo_confermato(self):
        d = self._demo()
        r = _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 d["rep_kwh"], d["rep_drv"], livello=90)
        assert r["verdetto"] == "RISPARMIO_CONFERMATO"
        assert r["risparmio_totale"] == pytest.approx(15840.0, abs=1.0)
        assert r["baseline_totale"] == pytest.approx(132000.0, abs=1.0)
        assert r["risparmio_pct"] == pytest.approx(12.0, abs=0.01)
        assert r["incertezza_u"] == pytest.approx(320.9, abs=1.0)
        assert r["modello"]["r2"] == pytest.approx(0.9999, abs=1e-4)
        assert r["n_anomalie"] == 0
        assert len(r["mesi"]) == 12
        assert len(r["risparmi_mensili"]) == 12

    def test_modello_debole(self):
        b = [100, 200, 150, 300, 250, 180, 220, 190, 260, 210, 170, 240]
        x = [float(i) for i in range(1, 13)]
        r = _F["mh587_verifica"](b, x, b, x)
        assert r["verdetto"] == "MODELLO_DEBOLE"
        assert r["modello"]["r2"] < 0.75

    def test_non_significativo(self):
        d = self._demo()
        r = _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 d["bas_kwh"], d["bas_drv"])
        assert r["verdetto"] == "RISPARMIO_NON_SIGNIFICATIVO"
        assert abs(r["risparmio_totale"]) < 1e-6

    def test_aumento_consumi(self):
        d = self._demo()
        r = _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 [1.25 * v for v in d["rep_kwh"]],
                                 d["bas_drv"])
        assert r["verdetto"] == "AUMENTO_CONSUMI"
        assert r["risparmio_totale"] < 0

    def test_estrapolazione_anomalia(self):
        d = self._demo()
        rd = [999.0] + d["bas_drv"][1:]
        r = _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 d["rep_kwh"], rd)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert "estrapolazione" in r["anomalie"][0]

    def test_lunghezza_ko(self):
        d = self._demo()
        with pytest.raises(ValueError):
            _F["mh587_verifica"](d["bas_kwh"][:11], d["bas_drv"],
                                 d["rep_kwh"], d["rep_drv"])

    def test_livello_ko(self):
        d = self._demo()
        with pytest.raises(ValueError):
            _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 d["rep_kwh"], d["rep_drv"],
                                 livello=80)

    def test_mesi_coerenti(self):
        d = self._demo()
        r = _F["mh587_verifica"](d["bas_kwh"], d["bas_drv"],
                                 d["rep_kwh"], d["rep_drv"])
        for i, m in enumerate(r["mesi"]):
            assert m["mese"] == i + 1
            assert m["risparmio_kwh"] == pytest.approx(
                m["baseline_aggiustata"] - m["consumo_reale"])


class TestW587Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_presente(self):
        assert f'"{TITLE587}"' in self._src()

    def test_conteggio_tab(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 824
        assert TITLE587 in titles

    def test_chain_tab_var(self):
        assert ", tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824 = st.tabs([" in self._src()
        assert "with tab587:" in self._src()

    def test_chiavi_univoche(self):
        keys = set(re.findall(r"st587_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
