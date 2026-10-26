"""Test tab598 "🪵 Biomassa legnosa: business case (CHP)".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh598_num", "mh598_nneg", "mh598_pos", "mh598_pct",
           "mh598_annuity", "mh598_crf", "mh598_bilancio", "mh598_payback",
           "mh598_van", "mh598_tir", "mh598_lcoh", "mh598_breakeven_bio",
           "mh598_verdetto", "mh598_demo")

TITLE598 = "🪵 Biomassa legnosa: business case (CHP)"

DEMO = _F["mh598_demo"]()
# Demo: P_el=500 kWe, eta_el=18%, eta_th=65%, ore=7000, PCI=3.4 MWh/t,
#   p_bio=95 €/t, p_el=180 €/MWh, p_th=45 €/MWhth, quota=80%,
#   capex=4500 €/kWe -> 2 250 000 €, opex fisso 4%, opex var 12 €/MWh.
# P_th = 500*65/18 = 1805.5556 kWt ; P_fuel = 500/0.18 = 2777.7778 kWt
# E_el = 500*7000/1000 = 3500 ; E_th = 1805.5556*7 = 12638.8889 ;
# E_fuel = 2777.7778*7 = 19444.4444 MWh
# t_bio = 19444.4444/3.4 = 5718.9542 t ; costo_comb = 5718.9542*95 = 543300.65
# ric_el = 3500*180 = 630000 ; E_th_val = 12638.8889*0.8 = 10111.1111 ;
# ric_th = 10111.1111*45 = 455000
# opex = 2250000*0.04 + 3500*12 = 90000+42000 = 132000
# margine = 630000+455000-543300.65-132000 = 409699.35
# payback = 2250000/409699.35 = 5.4918 anni
# annuity(5,20) = (1-1.05^-20)/0.05 = 12.46221
# VAN = -2250000 + 409699.35*12.46221 = 2855759.43
# TIR: 409699.35 * a(r,20) = 2250000 -> a = 5.4918 -> r = 17.4831%
#   (verifica: a(17.4831%,20) = 5.49179)
# CRF(5,20) = 1/12.46221 = 0.0802426
# LCOH = (2250000*0.0802426 + 132000 + 543300.65 - 630000)/10111.1111
#      = 225846.51/10111.1111 = 22.3365 €/MWhth
# breakeven_bio = (630000+455000-132000)/5718.9542 = 953000/5718.9542
#              = 166.6389 €/t
CAPEX = 4500.0 * 500.0


def _bilancio_demo():
    return _F["mh598_bilancio"](500.0, 18.0, 65.0, 7000.0, 3.4, 95.0,
                                180.0, 45.0, 80.0, CAPEX, 4.0, 12.0)


class TestW598Validatori:
    def test_num(self):
        assert _F["mh598_num"](2, "x") == 2.0
        assert _F["mh598_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh598_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh598_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh598_nneg"](-0.1, "x")
        assert _F["mh598_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh598_pos"](bad, "x")
        assert _F["mh598_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh598_pct"](bad, "x")

    def test_annuity_crf(self):
        assert _F["mh598_annuity"](5.0, 20.0) == pytest.approx(12.46221,
                                                              abs=1e-4)
        assert _F["mh598_annuity"](0.0, 10.0) == pytest.approx(10.0)
        assert _F["mh598_crf"](5.0, 20.0) == pytest.approx(0.0802426,
                                                          abs=1e-6)


class TestW598Bilancio:
    def test_demo_hand(self):
        b = _bilancio_demo()
        assert b["p_el_kwe"] == pytest.approx(500.0)
        assert b["p_th_kwt"] == pytest.approx(1805.5556, abs=1e-3)
        assert b["p_fuel_kwt"] == pytest.approx(2777.7778, abs=1e-3)
        assert b["e_el_mwh"] == pytest.approx(3500.0)
        assert b["e_th_mwh"] == pytest.approx(12638.8889, abs=1e-3)
        assert b["e_fuel_mwh"] == pytest.approx(19444.4444, abs=1e-3)
        assert b["t_bio_anno"] == pytest.approx(5718.9542, abs=1e-3)
        assert b["e_th_val_mwh"] == pytest.approx(10111.1111, abs=1e-3)
        assert b["costo_comb_eur"] == pytest.approx(543300.65, abs=0.1)
        assert b["ricavo_el_eur"] == pytest.approx(630000.0)
        assert b["ricavo_th_eur"] == pytest.approx(455000.0)
        assert b["opex_eur"] == pytest.approx(132000.0)
        assert b["margine_eur"] == pytest.approx(409699.35, abs=0.1)
        assert b["capex_eur"] == pytest.approx(CAPEX)

    def test_potenza_non_confonde_con_prezzo(self):
        # regressione: _p_el era assegnato due volte (potenza e prezzo)
        b = _bilancio_demo()
        assert b["p_el_kwe"] == pytest.approx(500.0)
        assert b["e_el_mwh"] == pytest.approx(500.0 * 7000.0 / 1000.0)

    def test_input_non_validi(self):
        base = dict(p_el_kwe=500.0, eta_el_pct=18.0, eta_th_pct=65.0,
                    ore_anno=7000.0, pci_mwh_t=3.4, prezzo_bio_eur_t=95.0,
                    p_el_eur_mwh=180.0, p_th_eur_mwh=45.0, quota_th_pct=80.0,
                    capex_eur=CAPEX, opex_fisso_pct=4.0,
                    opex_var_eur_mwh=12.0)
        for k, v in (("p_el_kwe", 0), ("eta_el_pct", 0), ("ore_anno", 9000),
                     ("pci_mwh_t", -1), ("prezzo_bio_eur_t", -5)):
            kw = dict(base)
            kw[k] = v
            with pytest.raises(ValueError):
                _F["mh598_bilancio"](**kw)


class TestW598Economia:
    def test_payback(self):
        assert _F["mh598_payback"](CAPEX, 409699.35) == pytest.approx(
            5.4918, abs=1e-3)
        with pytest.raises(ValueError):
            _F["mh598_payback"](CAPEX, 0.0)
        with pytest.raises(ValueError):
            _F["mh598_payback"](CAPEX, -100.0)

    def test_van(self):
        assert _F["mh598_van"](CAPEX, 409699.35, 5.0,
                               20.0) == pytest.approx(2855759.43, abs=5.0)
        # tasso 0: VAN = -capex + margine*anni
        assert _F["mh598_van"](100.0, 10.0, 0.0,
                               20.0) == pytest.approx(100.0)

    def test_tir(self):
        tir = _F["mh598_tir"](CAPEX, 409699.35, 20.0)
        assert 17.3 < tir < 17.7
        # coerenza: NPV(tir) ~= 0
        npv = -CAPEX + 409699.35 * _F["mh598_annuity"](tir, 20.0)
        assert abs(npv) < 1.0
        # caso semplice: capex 100, margine 10, 20 anni -> TIR ~= 7.75%
        t2 = _F["mh598_tir"](100.0, 10.0, 20.0)
        assert 7.7 < t2 < 7.8
        with pytest.raises(ValueError):
            _F["mh598_tir"](CAPEX, 0.0, 20.0)
        with pytest.raises(ValueError):
            _F["mh598_tir"](0.0, 100.0, 20.0)

    def test_lcoh(self):
        b = _bilancio_demo()
        assert _F["mh598_lcoh"](b, 5.0, 20.0) == pytest.approx(22.3365,
                                                              abs=1e-3)
        b0 = dict(b)
        b0["e_th_val_mwh"] = 0.0
        with pytest.raises(ValueError):
            _F["mh598_lcoh"](b0, 5.0, 20.0)

    def test_breakeven(self):
        b = _bilancio_demo()
        assert _F["mh598_breakeven_bio"](b) == pytest.approx(166.6389,
                                                            abs=1e-3)
        # al prezzo di break-even il margine si azzera
        b2 = _F["mh598_bilancio"](500.0, 18.0, 65.0, 7000.0, 3.4,
                                  _F["mh598_breakeven_bio"](b), 180.0, 45.0,
                                  80.0, CAPEX, 4.0, 12.0)
        assert b2["margine_eur"] == pytest.approx(0.0, abs=1.0)

    def test_verdetto(self):
        assert _F["mh598_verdetto"](409699.35, 2855759.43,
                                    17.48)["verdetto"] == "OTTIMO"
        assert _F["mh598_verdetto"](100.0, 50.0,
                                    10.0)["verdetto"] == "BUONO"
        assert _F["mh598_verdetto"](100.0, 50.0,
                                    5.0)["verdetto"] == "MARGINALE"
        assert _F["mh598_verdetto"](-10.0, -5.0,
                                    0.0)["verdetto"] == "NON_REDDITIZIO"
        assert _F["mh598_verdetto"](100.0, -5.0,
                                    3.0)["verdetto"] == "NON_REDDITIZIO"

    def test_demo(self):
        assert DEMO["p_el_kwe"] == 500.0
        assert DEMO["pci_mwh_t"] == 3.4
        assert DEMO["combustibile"].startswith("Cippato")


class TestW598Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 733
        assert TITLE598 in titles
        assert TITLE598 in titles

    def test_chain(self):
        assert ", tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733 = st.tabs([" in self._src()
        assert "with tab598:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab598:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st598_[a-z0-9_]+", ui))
        attese = {"st598_comb", "st598_pci", "st598_pbio", "st598_pkw",
                  "st598_etael", "st598_etath", "st598_ore", "st598_pel",
                  "st598_pth", "st598_quota", "st598_capex", "st598_ofisso",
                  "st598_ovar", "st598_tasso", "st598_anni", "st598_pgas",
                  "st598_etacal", "st598_sep", "st598_graf", "st598_go",
                  "st598_tab", "st598_chart", "st598_csv"}
        assert keys == attese, keys ^ attese

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab598:")[1].split(
                "# Footer")[0], pat
