"""Test tab604 "☀️🔌 Rapporto DC/AC: clipping vs capex".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper) e contro-verificati con gli helper stessi.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh604_num", "mh604_nneg", "mh604_pos", "mh604_pct",
           "mh604_str", "mh604_parse_serie", "mh604_profilo_dc",
           "mh604_energia_giorno", "mh604_clipping_giorno",
           "mh604_clipping_pct", "mh604_pac_da_ratio",
           "mh604_capex_inverter", "mh604_clipping_annuo_eur",
           "mh604_van_annuo", "mh604_scansione", "mh604_ottimo",
           "mh604_verdetto", "mh604_demo")

TITLE604 = "☀️🔌 Rapporto DC/AC: clipping vs capex"

DEMO = _F["mh604_demo"]()
# Demo: profilo 24h [kW/kWp], FV 10 MWp = 10000 kWp.
# somma profilo = 0,02+0,10+0,25+0,45+0,62+0,74+0,80+0,82+0,78+0,68
#               + 0,52+0,33+0,15+0,04 = 6,30 kWh/kWp/giorno
# E_giorno = 6,30 × 10000 / 1000 = 63,0 MWh
# picco = 0,82 × 10000 = 8200 kW
# r = 1,3 -> Pac = 8200/1,3 = 6307,692307692308 kW
# ore oltre Pac: 7400, 8000, 8200, 7800, 6800 (6200 resta sotto)
# clip kW = 1092,3077+1692,3077+1892,3077+1492,3077+492,3077 = 6661,5385
# E_clip = 6,661538461538463 MWh/giorno
# clip% = 6,661538461538463/63 × 100 = 10,573870573870575 %
# capex = 6307,692307692308 × 90 = 567692,3076923076 €
# annuo = 6,661538461538463 × 365 × 70 = 170202,30769230775 €/anno
# annuity(6%, 25a) = (1 − 1,06^-25)/0,06 = 12,783356158268413
# VAN = 170202,30769230775 × 12,783356158268413 = 2175756,7181899576 €
# tot(1,3) = 567692,3076923076 + 2175756,7181899576 = 2743449,025882265 €
# r = 1,0 -> Pac = 8200, clip = 0, tot = 8200 × 90 = 738000 €
# r = 1,05 -> Pac = 7809,5238; clip = (8000−7809,5238)+(8200−7809,5238)
#           = 190,4762+390,4762 = 580,9524 kW -> 0,5809523809523817 MWh/g
E_GIORNO = 63.0
PICCO = 8200.0
PAC13 = 6307.692307692308
ECLIP13 = 6.661538461538463
PCT13 = 10.573870573870575
CAPEX13 = 567692.3076923076
ANNUO13 = 170202.30769230775
ANNUITY = 12.783356158268413
VAN13 = 2175756.7181899576
TOT13 = 2743449.025882265
TOT10 = 738000.0
ECLIP105 = 0.5809523809523817


class TestW604Validatori:
    def test_num(self):
        assert _F["mh604_num"](2, "x") == 2.0
        assert _F["mh604_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh604_num"](bad, "x")

    def test_nneg_pos_pct_str(self):
        assert _F["mh604_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh604_nneg"](-0.1, "x")
        assert _F["mh604_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh604_pos"](bad, "x")
        assert _F["mh604_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh604_pct"](bad, "x")
        assert _F["mh604_str"]("a", "x") == "a"
        with pytest.raises(ValueError):
            _F["mh604_str"](1, "x")

    def test_parse_serie(self):
        f = _F["mh604_parse_serie"]
        assert f("1, 2;3\n4", "s") == [1.0, 2.0, 3.0, 4.0]
        for bad in ("", "   ", "1, x", "1, nan"):
            with pytest.raises(ValueError):
                f(bad, "s")


class TestW604Fisica:
    def test_profilo_dc(self):
        pdc = _F["mh604_profilo_dc"](DEMO["profilo"], 10000.0)
        assert len(pdc) == 24
        assert max(pdc) == pytest.approx(PICCO)
        assert pdc[12] == pytest.approx(0.80 * 10000.0)
        for bad_prof, bad_tag in (([], 100.0), ([0.0] * 24, 100.0),
                                  ([0.1, -0.2], 100.0), ([0.1], 0.0)):
            with pytest.raises(ValueError):
                _F["mh604_profilo_dc"](bad_prof, bad_tag)

    def test_energia_giorno(self):
        pdc = _F["mh604_profilo_dc"](DEMO["profilo"], 10000.0)
        assert _F["mh604_energia_giorno"](pdc) == pytest.approx(E_GIORNO)
        with pytest.raises(ValueError):
            _F["mh604_energia_giorno"]([])

    def test_clipping_giorno(self):
        pdc = _F["mh604_profilo_dc"](DEMO["profilo"], 10000.0)
        assert _F["mh604_clipping_giorno"](pdc, PICCO) == pytest.approx(0.0)
        assert _F["mh604_clipping_giorno"](pdc, PAC13) == \
            pytest.approx(ECLIP13)
        assert _F["mh604_clipping_giorno"](pdc, 7809.52380952381) == \
            pytest.approx(ECLIP105)
        with pytest.raises(ValueError):
            _F["mh604_clipping_giorno"](pdc, 0.0)

    def test_clipping_pct(self):
        assert _F["mh604_clipping_pct"](ECLIP13, E_GIORNO) == \
            pytest.approx(PCT13)
        assert _F["mh604_clipping_pct"](0.0, E_GIORNO) == pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh604_clipping_pct"](1.0, 0.0)

    def test_pac_da_ratio(self):
        assert _F["mh604_pac_da_ratio"](PICCO, 1.3) == pytest.approx(PAC13)
        assert _F["mh604_pac_da_ratio"](PICCO, 1.0) == pytest.approx(PICCO)
        with pytest.raises(ValueError):
            _F["mh604_pac_da_ratio"](PICCO, 0.0)


class TestW604Economia:
    def test_capex_inverter(self):
        assert _F["mh604_capex_inverter"](PAC13, 90.0) == \
            pytest.approx(CAPEX13)
        assert _F["mh604_capex_inverter"](PAC13, 0.0) == pytest.approx(0.0)

    def test_clipping_annuo(self):
        assert _F["mh604_clipping_annuo_eur"](ECLIP13, 70.0) == \
            pytest.approx(ANNUO13)
        assert _F["mh604_clipping_annuo_eur"](0.0, 70.0) == pytest.approx(0.0)

    def test_van_annuo(self):
        assert _F["mh604_van_annuo"](1.0, 6.0, 25) == pytest.approx(ANNUITY)
        assert _F["mh604_van_annuo"](ANNUO13, 6.0, 25) == pytest.approx(VAN13)
        assert _F["mh604_van_annuo"](100.0, 0.0, 10) == pytest.approx(1000.0)
        with pytest.raises(ValueError):
            _F["mh604_van_annuo"](100.0, 6.0, 0)


class TestW604Scansione:
    def _scan(self):
        return _F["mh604_scansione"](DEMO["profilo"], 10000.0, 90.0, 70.0,
                                     6.0, 25)

    def test_geometria_scan(self):
        sc = self._scan()
        assert len(sc) == 25
        assert sc[0]["ratio"] == pytest.approx(0.80)
        assert sc[-1]["ratio"] == pytest.approx(2.00)
        assert sc[0]["clip_mwh_g"] == pytest.approx(0.0)

    def test_riga_130(self):
        sc = self._scan()
        r13 = [r for r in sc if abs(r["ratio"] - 1.3) < 1e-9][0]
        assert r13["pac_kw"] == pytest.approx(PAC13)
        assert r13["clip_mwh_g"] == pytest.approx(ECLIP13)
        assert r13["clip_pct"] == pytest.approx(PCT13)
        assert r13["capex_inv"] == pytest.approx(CAPEX13)
        assert r13["van_clip"] == pytest.approx(VAN13)
        assert r13["costo_tot"] == pytest.approx(TOT13)

    def test_ottimo(self):
        sc = self._scan()
        ot = _F["mh604_ottimo"](sc)
        assert ot["ratio"] == pytest.approx(1.00)
        assert ot["costo_tot"] == pytest.approx(TOT10)
        assert ot["clip_mwh_g"] == pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh604_ottimo"]([])

    def test_verdetto(self):
        v = _F["mh604_verdetto"]
        assert v(1.30, 1.00)["verdetto"] == "SOVRA_CARICATO"
        assert v(1.00, 1.00)["verdetto"] == "OTTIMALE"
        assert v(1.04, 1.00)["verdetto"] == "OTTIMALE"
        assert v(0.85, 1.00)["verdetto"] == "SOTTO_UTILIZZATO"
        for bad in (0.0, -1.0):
            with pytest.raises(ValueError):
                v(bad, 1.00)

    def test_demo(self):
        d = DEMO
        assert len(d["profilo"]) == 24
        assert d["taglia_mwp"] == 10.0
        assert d["r_scelto"] == 1.30


class TestW604Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab604:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 741
        assert TITLE604 in titles
        assert TITLE604 in titles

    def test_chain(self):
        assert ", tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741 = st.tabs([" in self._src()
        assert "with tab604:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st604_[a-z0-9_]+", self._ui()))
        attese = {"st604_profilo", "st604_taglia", "st604_cinv",
                  "st604_prezzo", "st604_tasso", "st604_anni",
                  "st604_rscelto", "st604_tabc", "st604_graf", "st604_go",
                  "st604_chart", "st604_chart2", "st604_tab", "st604_csv"}
        assert keys == attese, keys ^ attese

    def test_helpers(self):
        src = self._src()
        mh = set(re.findall(r"def (mh604_\w+)\(", src))
        attesi = {"mh604_num", "mh604_nneg", "mh604_pos", "mh604_pct",
                  "mh604_str", "mh604_parse_serie", "mh604_profilo_dc",
                  "mh604_energia_giorno", "mh604_clipping_giorno",
                  "mh604_clipping_pct", "mh604_pac_da_ratio",
                  "mh604_capex_inverter", "mh604_clipping_annuo_eur",
                  "mh604_van_annuo", "mh604_scansione", "mh604_ottimo",
                  "mh604_verdetto", "mh604_demo"}
        assert mh == attesi, (mh ^ attesi)

    def test_no_secrets(self):
        src = self._ui().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src, pat
