"""Test tab595 "🚢⛽ Bunker fuel: VLSFO vs LNG vs metanolo vs ammoniaca".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh595_num", "mh595_nneg", "mh595_pct", "mh595_eff",
           "mh595_lhv_mwh_t", "mh595_eur_mwh_th", "mh595_costo_propulsivo",
           "mh595_costo_ets", "mh595_target_fueleu", "mh595_penale_fueleu",
           "mh595_co2_wtw_mwh", "mh595_fuel", "mh595_confronto",
           "mh595_voyage", "mh595_demo")

TITLE595 = "🚢⛽ Bunker fuel: VLSFO vs LNG vs metanolo vs ammoniaca"

DEMO = _F["mh595_demo"]()
VLSFO = DEMO["fuels"][0]
# Caso base VLSFO demo: prezzo 520 €/t, LHV 40.2 GJ/t, EF 3.114 tCO2/t,
# eta 50%, WtW 91.16 g/MJ, EUA 82.5, phase-in 100%, share 50%, anno 2025.
#   lhv = 40.2/3.6 = 11.1666667 MWh_th/t
#   eur_mwh_th = 520/11.1666667 = 520*3.6/40.2 = 1872/40.2 = 46.5671641791
#   costo_prop = 46.5671641791/0.5 = 93.1343283582
#   ets = 82.5*3.114/11.1666667/0.5*1.0*0.5
#       = 82.5*3.114*3.6/40.2 (i due 0.5 si cancellano)
#       = 82.5*11.2104/40.2 = 924.858/40.2 = 23.0064179104
#   target25 = 91.16*0.98 = 89.3368 ; eccesso = 1.8232
#   penale = 1.8232*3600*2400/(1e6*41) = 1.8232*0.2107317073 = 0.3842060488
#   fueleu_mwh = 0.3842060488/0.5 = 0.7684120976
#   totale = 93.1343283582+23.0064179104+0.7684120976 = 116.9091583662
#   wtw = 91.16*3.6/1000/0.5 = 0.328176/0.5 = 0.656352 t/MWh
#   eur_t = 520 + 82.5*3.114*1.0*0.5 (=128.4525)
#           + 0.3842060488*11.1666667 (=4.290296...) = 652.742796...
ROW_VLSFO = _F["mh595_fuel"](
    "VLSFO", 520.0, 40.2, 3.114, 50.0, 91.16, 82.5, 100.0, 50.0, 2025)
PEN25 = 1.8232 * 3600.0 * 2400.0 / (1000000.0 * 41.0)  # 0.3842060488


class TestW595Validatori:
    def test_num_ok(self):
        assert _F["mh595_num"](2, "x") == 2.0
        assert _F["mh595_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "2", None, [1], math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh595_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh595_nneg"](0, "x") == 0.0
        assert _F["mh595_nneg"](1.5, "x") == 1.5
        with pytest.raises(ValueError):
            _F["mh595_nneg"](-0.1, "x")

    def test_pct(self):
        assert _F["mh595_pct"](0, "x") == 0.0
        assert _F["mh595_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1, "x", True):
            with pytest.raises(ValueError):
                _F["mh595_pct"](bad, "x")

    def test_eff(self):
        assert _F["mh595_eff"](50, "e") == pytest.approx(0.5)
        assert _F["mh595_eff"](100, "e") == pytest.approx(1.0)
        for bad in (0, -1, 100.01, "x", True):
            with pytest.raises(ValueError):
                _F["mh595_eff"](bad, "e")


class TestW595Conversioni:
    def test_lhv(self):
        # 40.2/3.6 = 11.1666667 MWh_th/t
        assert _F["mh595_lhv_mwh_t"](40.2) == pytest.approx(11.1666667)
        for bad in (0, -5):
            with pytest.raises(ValueError):
                _F["mh595_lhv_mwh_t"](bad)

    def test_eur_mwh_th(self):
        # 520*3.6/40.2 = 1872/40.2 = 46.5671641791
        assert _F["mh595_eur_mwh_th"](520, 40.2) == pytest.approx(
            46.5671641791)
        assert _F["mh595_eur_mwh_th"](0, 40.2) == 0.0

    def test_costo_propulsivo(self):
        # 46.5671641791/0.5 = 93.1343283582
        assert _F["mh595_costo_propulsivo"](46.5671641791, 50) == \
            pytest.approx(93.1343283582)

    def test_costo_ets(self):
        # 82.5*11.2104/40.2 = 924.858/40.2 = 23.0064179104
        assert _F["mh595_costo_ets"](82.5, 3.114, 40.2, 50, 100, 50) == \
            pytest.approx(23.0064179104)
        # phase-in 0 -> nessun costo ETS
        assert _F["mh595_costo_ets"](82.5, 3.114, 40.2, 50, 0, 50) == 0.0
        # share 100 raddoppia vs share 50
        assert _F["mh595_costo_ets"](82.5, 3.114, 40.2, 50, 100, 100) == \
            pytest.approx(2 * 23.0064179104)

    def test_target_fueleu(self):
        # 91.16*0.98 = 89.3368 ; 91.16*0.94 = 85.6904
        assert _F["mh595_target_fueleu"](2025) == pytest.approx(89.3368)
        assert _F["mh595_target_fueleu"](2030) == pytest.approx(85.6904)
        assert _F["mh595_target_fueleu"](2050) == pytest.approx(18.232)
        for bad in (2027, 2024, 2025.5, "2025"):
            with pytest.raises(ValueError):
                _F["mh595_target_fueleu"](bad)

    def test_penale_fueleu(self):
        assert _F["mh595_penale_fueleu"](91.16, 2025) == pytest.approx(PEN25)
        # sotto il target: nessuna penale
        assert _F["mh595_penale_fueleu"](80.0, 2025) == 0.0
        assert _F["mh595_penale_fueleu"](89.3368, 2025) == 0.0
        # 2030: eccesso 91.16-85.6904 = 5.4696 ; *0.2107317073 = 1.152618...
        assert _F["mh595_penale_fueleu"](91.16, 2030) == pytest.approx(
            5.4696 * 0.2107317073)

    def test_co2_wtw_mwh(self):
        # 91.16*3.6/1000/0.5 = 0.656352 tCO2eq/MWh prop.
        assert _F["mh595_co2_wtw_mwh"](91.16, 50) == pytest.approx(0.656352)


class TestW595Fuel:
    def test_riga_vlsfo(self):
        r = ROW_VLSFO
        assert r["nome"] == "VLSFO"
        assert r["eur_mwh_th"] == pytest.approx(46.5671641791)
        assert r["costo_propulsivo"] == pytest.approx(93.1343283582)
        assert r["ets_mwh"] == pytest.approx(23.0064179104)
        assert r["fueleu_mwh"] == pytest.approx(PEN25 / 0.5)
        assert r["totale_mwh"] == pytest.approx(116.9091583662)
        assert r["co2_wtw_mwh"] == pytest.approx(0.656352)
        # 520 + 128.4525 + 0.3842060488*11.1666667 = 652.742796...
        assert r["eur_t_tot"] == pytest.approx(652.742796, abs=1e-4)

    def test_lng_fueleu_zero(self):
        # 83.0 < 89.3368 -> FuelEU 0; ETS = 82.5*2.75/(48/3.6)/0.49*1.0*0.5
        # = 17.015625/0.49 = 34.7257653061 ; *0.5 = 17.3628826531
        lng = _F["mh595_fuel"]("LNG", 720.0, 48.0, 2.75, 49.0, 83.0,
                               82.5, 100.0, 50.0, 2025)
        assert lng["fueleu_mwh"] == 0.0
        assert lng["ets_mwh"] == pytest.approx(17.3628826531)
        # 720/(48/3.6) = 54.0 ; /0.49 = 110.2040816 ; + ETS = 127.5669643
        assert lng["totale_mwh"] == pytest.approx(127.5669643)

    def test_nome_ko(self):
        for bad in ("", "  ", 5, None):
            with pytest.raises(ValueError):
                _F["mh595_fuel"](bad, 520.0, 40.2, 3.114, 50.0, 91.16,
                                 82.5, 100.0, 50.0, 2025)


class TestW595Confronto:
    def _righe(self):
        d = DEMO
        return [_F["mh595_fuel"](f["nome"], f["prezzo_t"], f["lhv_gj_t"],
                                 f["ef_tco2_t"], f["eff_pct"], f["wtw_g_mj"],
                                 d["eua"], d["phasein_pct"], d["share_pct"],
                                 d["anno"]) for f in d["fuels"]]

    def test_best_vlsfo(self):
        # VLSFO 116.91 < LNG 127.57 < MeOH 508.79 < NH3 537.63
        c = _F["mh595_confronto"](self._righe())
        assert c["piu_economico"] == "VLSFO"
        assert c["totale_best"] == pytest.approx(116.9091583662)
        assert c["delta_best_vs_rif"] == pytest.approx(0.0)
        assert c["riferimento"] == "VLSFO"

    def test_delta_lng(self):
        # 127.5669643 - 116.9091584 = 10.6578059 ; % = 9.1161%
        c = _F["mh595_confronto"](self._righe())
        lng = [r for r in c["righe"] if r["nome"] == "LNG"][0]
        assert lng["delta_vs_rif"] == pytest.approx(10.6578059)
        assert lng["delta_pct_vs_rif"] == pytest.approx(9.1161, abs=1e-3)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh595_confronto"]([])
        with pytest.raises(ValueError):
            _F["mh595_confronto"]([{"nome": "x"}])


class TestW595Voyage:
    def test_viaggio_vlsfo(self):
        # 30 t/g x 20 gg = 600 t ; 600*652.742796 = 391645.68 ;
        # /20 = 19582.28 €/giorno
        v = _F["mh595_voyage"](ROW_VLSFO, 30.0, 20.0)
        assert v["tonnellate"] == pytest.approx(600.0)
        assert v["costo_viaggio"] == pytest.approx(391645.68, abs=0.5)
        assert v["costo_giorno"] == pytest.approx(19582.28, abs=0.05)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh595_voyage"](ROW_VLSFO, 0, 20.0)
        with pytest.raises(ValueError):
            _F["mh595_voyage"](ROW_VLSFO, 30.0, -1)
        with pytest.raises(ValueError):
            _F["mh595_voyage"]({"nome": "x"}, 30.0, 20.0)


class TestW595Demo:
    def test_demo(self):
        assert DEMO["eua"] == 82.5
        assert DEMO["phasein_pct"] == 100.0
        assert DEMO["share_pct"] == 50.0
        assert DEMO["anno"] == 2025
        assert len(DEMO["fuels"]) == 4
        assert [f["nome"] for f in DEMO["fuels"]] == [
            "VLSFO", "LNG", "Metanolo green", "Ammoniaca green"]


class TestW595Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 749
        assert TITLE595 in titles
        assert TITLE595 in titles

    def test_chain(self):
        assert ", tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749 = st.tabs([" in self._src()
        assert "with tab595:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st595_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab595:")[1].split(
                "# Footer")[0], pat
