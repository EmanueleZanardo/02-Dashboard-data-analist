"""Test tab600 "🔌🔋 V2G: ricavi da vehicle-to-grid".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh600_num", "mh600_nneg", "mh600_pos", "mh600_pct",
           "mh600_annuity", "mh600_crf", "mh600_energia_ciclo",
           "mh600_vincolo_soc", "mh600_arbitraggio", "mh600_breakeven",
           "mh600_bilancio", "mh600_payback", "mh600_van", "mh600_tir",
           "mh600_lcos", "mh600_verdetto", "mh600_demo")

TITLE600 = "🔌🔋 V2G: ricavi da vehicle-to-grid"

DEMO = _F["mh600_demo"]()
# Demo: N=20, B=60 kWh, DoD=40%, eta_rt=85%, p_carica=60 €/MWh,
#   p_scarica=200 €/MWh, degrado=0,03 €/kWh, SoC_part=80%, SoC_min=30%,
#   giorni=300, capex_veicolo=3000 €, opex=3%, tasso=5%, vita=10.
# E = 60*0,4*20 = 480 kWh/ciclo ; e_dod = 24 ; e_soc = 60*0,5 = 30 ;
#   e_max = 24 (non limitato)
# e_in = 480/0,85 = 564,7059
# C_car = 564,7059/1000*60 = 33,8824 ; R = 480/1000*200 = 96,0
# C_deg = 480*0,03 = 14,4 ; lordo = 96-33,8824 = 62,1176
# netto = 62,1176-14,4 = 47,7176
# spread = 200 - 60/0,85 - 30 = 99,4118 €/MWh ; p_be = 100,5882
# marg_annuo = 47,7176*300 = 14315,2941
# capex = 60000 ; opex = 1800 ; marg_annuo = 14315,2941-1800 = 12515,2941
# payback = 60000/12515,2941 = 4,7941 anni
# annuity(5,10) = (1-1,05^-10)/0,05 = 7,721735
# VAN = -60000 + 12515,2941*7,721735 = 36639,78
# CRF = 0,1295046 ; e_annua = 144 MWh
# LCOE = (60000*0,1295046 + 1800 + 33,8824*300)/144 = 137,0485 €/MWh
# TIR: 12515,2941*a(r,10) = 60000 -> a = 4,7941 -> r = 16,2187%
# verdetto: margine>0, van>0, tir 16,22 >= 5+5 -> OTTIMO
CAPEX = 20.0 * 3000.0
NETTO = 47.7176


def _arb_demo():
    return _F["mh600_arbitraggio"](480.0, 85.0, 60.0, 200.0, 0.03)


class TestW600Validatori:
    def test_num(self):
        assert _F["mh600_num"](2, "x") == 2.0
        assert _F["mh600_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh600_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh600_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh600_nneg"](-0.1, "x")
        assert _F["mh600_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh600_pos"](bad, "x")
        assert _F["mh600_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh600_pct"](bad, "x")

    def test_annuity_crf(self):
        assert _F["mh600_annuity"](5.0, 10.0) == pytest.approx(7.721735,
                                                              abs=1e-4)
        assert _F["mh600_annuity"](0.0, 10.0) == pytest.approx(10.0)
        assert _F["mh600_crf"](5.0, 10.0) == pytest.approx(0.1295046,
                                                         abs=1e-6)


class TestW600EnergiaVincolo:
    def test_energia_ciclo(self):
        assert _F["mh600_energia_ciclo"](60.0, 40.0, 20.0) == \
            pytest.approx(480.0)
        with pytest.raises(ValueError):
            _F["mh600_energia_ciclo"](60.0, 0.0, 20.0)
        with pytest.raises(ValueError):
            _F["mh600_energia_ciclo"](60.0, 40.0, 0.0)

    def test_vincolo_soc_non_limitato(self):
        v = _F["mh600_vincolo_soc"](60.0, 80.0, 30.0, 40.0)
        assert v["e_dod_kwh"] == pytest.approx(24.0)
        assert v["e_soc_kwh"] == pytest.approx(30.0)
        assert v["e_max_kwh"] == pytest.approx(24.0)
        assert v["limitato"] is False

    def test_vincolo_soc_limitato(self):
        v = _F["mh600_vincolo_soc"](60.0, 60.0, 50.0, 40.0)
        # e_dod = 24 ; e_soc = 60*0,1 = 6 -> limitato a 6
        assert v["e_max_kwh"] == pytest.approx(6.0)
        assert v["limitato"] is True

    def test_vincolo_soc_finestra_vuota(self):
        with pytest.raises(ValueError):
            _F["mh600_vincolo_soc"](60.0, 30.0, 30.0, 40.0)
        with pytest.raises(ValueError):
            _F["mh600_vincolo_soc"](60.0, 20.0, 30.0, 40.0)


class TestW600Arbitraggio:
    def test_demo(self):
        a = _arb_demo()
        assert a["e_scarica_kwh"] == pytest.approx(480.0)
        assert a["e_in_kwh"] == pytest.approx(564.7059, abs=1e-3)
        assert a["costo_carica_eur"] == pytest.approx(33.8824, abs=1e-3)
        assert a["ricavo_eur"] == pytest.approx(96.0)
        assert a["costo_degrado_eur"] == pytest.approx(14.4)
        assert a["margine_lordo_eur"] == pytest.approx(62.1176, abs=1e-3)
        assert a["margine_netto_eur"] == pytest.approx(NETTO, abs=1e-3)
        assert a["spread_eur_mwh"] == pytest.approx(99.4118, abs=1e-3)

    def test_spread_negativo(self):
        a = _F["mh600_arbitraggio"](480.0, 85.0, 200.0, 60.0, 0.03)
        assert a["margine_netto_eur"] < 0.0
        assert a["spread_eur_mwh"] < 0.0

    def test_breakeven(self):
        assert _F["mh600_breakeven"](60.0, 85.0, 0.03) == pytest.approx(
            100.5882, abs=1e-3)
        # al prezzo di pareggio il margine netto e' (quasi) zero
        a = _F["mh600_arbitraggio"](480.0, 85.0, 60.0, 100.5882, 0.03)
        assert a["margine_netto_eur"] == pytest.approx(0.0, abs=1e-2)

    def test_eta_vuota(self):
        with pytest.raises(ValueError):
            _F["mh600_arbitraggio"](480.0, 0.0, 60.0, 200.0, 0.03)
        with pytest.raises(ValueError):
            _F["mh600_breakeven"](60.0, 0.0, 0.03)


class TestW600BilancioFinanza:
    def test_bilancio(self):
        _netto_demo = _arb_demo()["margine_netto_eur"]
        b = _F["mh600_bilancio"](_netto_demo, 300.0, 20.0, 3000.0, 3.0)
        assert b["capex_eur"] == pytest.approx(CAPEX)
        assert b["opex_eur"] == pytest.approx(1800.0)
        assert b["margine_annuo_eur"] == pytest.approx(12515.2941,
                                                      abs=1e-3)
        with pytest.raises(ValueError):
            _F["mh600_bilancio"](_netto_demo, 366.0, 20.0, 3000.0, 3.0)

    def test_payback_van_tir(self):
        assert _F["mh600_payback"](CAPEX, 12515.2941) == pytest.approx(
            4.7941, abs=1e-3)
        assert _F["mh600_van"](CAPEX, 12515.2941, 5.0, 10.0) == \
            pytest.approx(36639.78, abs=1.0)
        assert _F["mh600_tir"](CAPEX, 12515.2941, 10.0) == pytest.approx(
            16.2187, abs=0.1)
        with pytest.raises(ValueError):
            _F["mh600_payback"](CAPEX, 0.0)
        with pytest.raises(ValueError):
            _F["mh600_tir"](CAPEX, 0.0, 10.0)
        with pytest.raises(ValueError):
            _F["mh600_tir"](0.0, 100.0, 10.0)

    def test_lcos(self):
        a = _arb_demo()
        b = _F["mh600_bilancio"](NETTO, 300.0, 20.0, 3000.0, 3.0)
        assert _F["mh600_lcos"](a, b, 5.0, 10.0, 300.0) == pytest.approx(
            137.0485, abs=1e-2)
        # V2G conviene nel caso demo: LCOE < prezzo di vendita
        assert _F["mh600_lcos"](a, b, 5.0, 10.0, 300.0) < 200.0
        a0 = dict(a)
        a0["e_scarica_kwh"] = 0.0
        with pytest.raises(ValueError):
            _F["mh600_lcos"](a0, b, 5.0, 10.0, 300.0)

    def test_verdetto(self):
        assert _F["mh600_verdetto"](100.0, 50.0, 15.0,
                                    5.0)["verdetto"] == "OTTIMO"
        assert _F["mh600_verdetto"](100.0, 50.0, 7.5,
                                    5.0)["verdetto"] == "BUONO"
        assert _F["mh600_verdetto"](100.0, 50.0, 4.0,
                                    5.0)["verdetto"] == "MARGINALE"
        assert _F["mh600_verdetto"](-10.0, -5.0, 0.0,
                                    5.0)["verdetto"] == "NON_REDDITIZIO"
        assert _F["mh600_verdetto"](100.0, -5.0, 3.0,
                                    5.0)["verdetto"] == "NON_REDDITIZIO"

    def test_verdetto_demo(self):
        tir = _F["mh600_tir"](CAPEX, 12515.2941, 10.0)
        v = _F["mh600_verdetto"](12515.2941, 36639.78, tir, 5.0)
        assert v["verdetto"] == "OTTIMO"

    def test_demo(self):
        assert DEMO["veicoli"] == 20.0
        assert DEMO["batt_kwh"] == 60.0
        assert DEMO["eta_rt_pct"] == 85.0
        assert DEMO["costo_degrado_eur_kwh"] == 0.03


class TestW600Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 790
        assert TITLE600 in titles
        assert TITLE600 in titles

    def test_chain(self):
        assert ", tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790 = st.tabs([" in self._src()
        assert "with tab600:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab600:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st600_[a-z0-9_]+", ui))
        attese = {"st600_veicoli", "st600_batt", "st600_dod",
                  "st600_eta", "st600_pc", "st600_ps", "st600_cdeg",
                  "st600_socpart", "st600_socmin", "st600_giorni",
                  "st600_capex", "st600_opex", "st600_tasso", "st600_anni",
                  "st600_sep", "st600_graf", "st600_go", "st600_tab",
                  "st600_chart", "st600_csv"}
        assert keys == attese, keys ^ attese

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab600:")[1].split(
                "# Footer")[0], pat
