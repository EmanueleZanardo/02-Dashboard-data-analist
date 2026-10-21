"""Test tab599 "🧊 Accumulo termico (TES): peak-shaving del calore".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh599_num", "mh599_nneg", "mh599_pos", "mh599_pct",
           "mh599_annuity", "mh599_crf", "mh599_volume", "mh599_bilancio",
           "mh599_payback", "mh599_van", "mh599_tir", "mh599_lcohs",
           "mh599_gas_equiv", "mh599_co2_evitata", "mh599_verdetto",
           "mh599_demo")

TITLE599 = "🧊 Accumulo termico (TES): peak-shaving del calore"

DEMO = _F["mh599_demo"]()
# Demo: E_giorno=2000 kWh, giorni=320, ΔT=40 K, COP=3.5, p_el=80 €/MWh,
#   p_gas=75 €/MWh, eta_caldaia=90%, capex_spec=150 €/kWhth,
#   capex_fisso=20000 €, opex_fisso=2%, tasso=5%, vita=15.
# V = 2000/(1.1633*40) = 42.9812 m³
# E_annuo = 2000*320/1000 = 640 ; E_gas_ev = 640/0.9 = 711.1111 ;
# C_gas = 711.1111*75 = 53333.333
# E_el = 640/3.5 = 182.8571 ; C_car = 182.8571*80 = 14628.571
# lordo = 53333.333-14628.571 = 38704.762
# capex = 2000*150+20000 = 320000 ; opex = 320000*0.02 = 6400
# margine = 38704.762-6400 = 32304.762
# payback = 320000/32304.762 = 9.9057 anni
# annuity(5,15) = (1-1.05^-15)/0.05 = 10.37966
# VAN = -320000 + 32304.762*10.37966 = 15312.38
# CRF(5,15) = 1/10.37966 = 0.0963423
# LCOHS = (320000*0.0963423 + 6400 + 14628.571)/640 = 81.0283 €/MWhth
# gas_equiv = 75/0.9 = 83.3333 €/MWhth
# TIR: 32304.762 * a(r,15) = 320000 -> a = 9.9057 -> r = 5.6997%
# CO2 = 711.1111*0.202 = 143.644 t
CAPEX = 2000.0 * 150.0 + 20000.0


def _bilancio_demo():
    return _F["mh599_bilancio"](2000.0, 320.0, 40.0, 3.5, 80.0, 75.0,
                                90.0, 150.0, 20000.0, 2.0)


class TestW599Validatori:
    def test_num(self):
        assert _F["mh599_num"](2, "x") == 2.0
        assert _F["mh599_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh599_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh599_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh599_nneg"](-0.1, "x")
        assert _F["mh599_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh599_pos"](bad, "x")
        assert _F["mh599_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh599_pct"](bad, "x")

    def test_annuity_crf(self):
        assert _F["mh599_annuity"](5.0, 15.0) == pytest.approx(10.37966,
                                                              abs=1e-4)
        assert _F["mh599_annuity"](0.0, 10.0) == pytest.approx(10.0)
        assert _F["mh599_crf"](5.0, 15.0) == pytest.approx(0.0963423,
                                                          abs=1e-6)


class TestW599VolumeBilancio:
    def test_volume(self):
        assert _F["mh599_volume"](2000.0, 40.0) == pytest.approx(
            42.9812, abs=1e-3)
        with pytest.raises(ValueError):
            _F["mh599_volume"](2000.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh599_volume"](-5.0, 40.0)

    def test_demo_hand(self):
        b = _bilancio_demo()
        assert b["volume_m3"] == pytest.approx(42.9812, abs=1e-3)
        assert b["e_annuo_mwh"] == pytest.approx(640.0)
        assert b["e_gas_evitata_mwh"] == pytest.approx(711.1111, abs=1e-3)
        assert b["costo_gas_evitato_eur"] == pytest.approx(53333.333,
                                                          abs=0.1)
        assert b["e_el_carica_mwh"] == pytest.approx(182.8571, abs=1e-3)
        assert b["costo_carica_eur"] == pytest.approx(14628.571, abs=0.1)
        assert b["risparmio_lordo_eur"] == pytest.approx(38704.762, abs=0.1)
        assert b["capex_eur"] == pytest.approx(CAPEX)
        assert b["opex_eur"] == pytest.approx(6400.0)
        assert b["margine_eur"] == pytest.approx(32304.762, abs=0.1)

    def test_capex_non_confonde_con_spec(self):
        # regressione: capex deve essere E*cspec + fisso, non solo E*cspec
        b = _F["mh599_bilancio"](1000.0, 300.0, 40.0, 3.0, 80.0, 70.0,
                                 90.0, 150.0, 25000.0, 2.0)
        assert b["capex_eur"] == pytest.approx(175000.0)
        assert b["volume_m3"] == pytest.approx(1000.0 / (1.1633 * 40.0))

    def test_input_non_validi(self):
        base = dict(e_giorno_kwh=2000.0, giorni_anno=320.0, delta_t_k=40.0,
                    cop=3.5, p_el_eur_mwh=80.0, p_gas_eur_mwh=75.0,
                    eta_caldaia_pct=90.0, capex_spec_eur_kwh=150.0,
                    capex_fisso_eur=20000.0, opex_fisso_pct=2.0)
        for k, v in (("e_giorno_kwh", 0), ("giorni_anno", 366),
                     ("delta_t_k", -1), ("cop", 0),
                     ("eta_caldaia_pct", 0), ("p_gas_eur_mwh", -5)):
            kw = dict(base)
            kw[k] = v
            with pytest.raises(ValueError):
                _F["mh599_bilancio"](**kw)


class TestW599Economia:
    def test_payback(self):
        assert _F["mh599_payback"](CAPEX, 32304.762) == pytest.approx(
            9.9057, abs=1e-3)
        with pytest.raises(ValueError):
            _F["mh599_payback"](CAPEX, 0.0)
        with pytest.raises(ValueError):
            _F["mh599_payback"](CAPEX, -100.0)

    def test_van(self):
        assert _F["mh599_van"](CAPEX, 32304.762, 5.0,
                               15.0) == pytest.approx(15312.38, abs=5.0)
        # tasso 0: VAN = -capex + margine*anni
        assert _F["mh599_van"](100.0, 10.0, 0.0,
                               15.0) == pytest.approx(50.0)

    def test_tir(self):
        tir = _F["mh599_tir"](CAPEX, 32304.762, 15.0)
        assert 5.5 < tir < 5.9
        # coerenza: NPV(tir) ~= 0
        npv = -CAPEX + 32304.762 * _F["mh599_annuity"](tir, 15.0)
        assert abs(npv) < 1.0
        with pytest.raises(ValueError):
            _F["mh599_tir"](CAPEX, 0.0, 15.0)
        with pytest.raises(ValueError):
            _F["mh599_tir"](0.0, 100.0, 15.0)

    def test_lcohs_gas_equiv(self):
        b = _bilancio_demo()
        assert _F["mh599_lcohs"](b, 5.0, 15.0) == pytest.approx(81.0283,
                                                               abs=1e-3)
        assert _F["mh599_gas_equiv"](75.0, 90.0) == pytest.approx(
            83.3333, abs=1e-3)
        # TES conviene al caso demo
        assert _F["mh599_lcohs"](b, 5.0, 15.0) < _F["mh599_gas_equiv"](
            75.0, 90.0)
        b0 = dict(b)
        b0["e_annuo_mwh"] = 0.0
        with pytest.raises(ValueError):
            _F["mh599_lcohs"](b0, 5.0, 15.0)

    def test_co2(self):
        assert _F["mh599_co2_evitata"](711.1111) == pytest.approx(
            143.644, abs=0.01)
        with pytest.raises(ValueError):
            _F["mh599_co2_evitata"](-1.0)

    def test_verdetto(self):
        assert _F["mh599_verdetto"](100.0, 50.0, 15.0,
                                    5.0)["verdetto"] == "OTTIMO"
        assert _F["mh599_verdetto"](100.0, 50.0, 7.5,
                                    5.0)["verdetto"] == "BUONO"
        assert _F["mh599_verdetto"](100.0, 50.0, 4.0,
                                    5.0)["verdetto"] == "MARGINALE"
        assert _F["mh599_verdetto"](-10.0, -5.0, 0.0,
                                    5.0)["verdetto"] == "NON_REDDITIZIO"
        assert _F["mh599_verdetto"](100.0, -5.0, 3.0,
                                    5.0)["verdetto"] == "NON_REDDITIZIO"

    def test_verdetto_demo(self):
        tir = _F["mh599_tir"](CAPEX, 32304.762, 15.0)
        v = _F["mh599_verdetto"](32304.762, 15312.38, tir, 5.0)
        assert v["verdetto"] == "BUONO"

    def test_demo(self):
        assert DEMO["e_giorno_kwh"] == 2000.0
        assert DEMO["delta_t_k"] == 40.0
        assert DEMO["cop"] == 3.5


class TestW599Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 615
        assert TITLE599 in titles
        assert TITLE599 in titles

    def test_chain(self):
        assert ", tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615 = st.tabs([" in self._src()
        assert "with tab599:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab599:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st599_[a-z0-9_]+", ui))
        attese = {"st599_egiorno", "st599_giorni", "st599_deltat",
                  "st599_cop", "st599_pel", "st599_pgas", "st599_etacal",
                  "st599_cspec", "st599_cfisso", "st599_ofisso",
                  "st599_tasso", "st599_anni", "st599_sep", "st599_graf",
                  "st599_go", "st599_tab", "st599_chart", "st599_csv"}
        assert keys == attese, keys ^ attese

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret", "token"):
            assert pat not in src.lower().split("with tab599:")[1].split(
                "# Footer")[0], pat
