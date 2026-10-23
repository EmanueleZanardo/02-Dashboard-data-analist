"""Test tab596 "🌍🏠 ETS2: costo carbonio per edifici & trasporti".

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

_F = _load("mh596_num", "mh596_nneg", "mh596_pct", "mh596_anno",
           "mh596_ef_kg_l", "mh596_costo_litro", "mh596_costo_mwh_gas",
           "mh596_prezzo_finale", "mh596_quota_pct", "mh596_costo_auto",
           "mh596_costo_riscaldamento", "mh596_cap45", "mh596_fuel_row",
           "mh596_confronto", "mh596_demo")

TITLE596 = "🌍🏠 ETS2: costo carbonio per edifici & trasporti"

DEMO = _F["mh596_demo"]()
# Demo: prezzo_ets2 = 45.0 €/t, anno 2027.
#   diesel €/l = 45*2.68/1000 = 120.6/1000 = 0.1206
#   benzina €/l = 45*2.31/1000 = 103.95/1000 = 0.10395
#   gpl €/l = 45*1.53/1000 = 68.85/1000 = 0.06885
#   gas €/MWh = 45*0.202 = 9.09
#   finale diesel = 1.70+0.1206 = 1.8206
#   quota diesel = 0.1206/1.8206*100 = 6.62419%
#   auto diesel: litri = 15000*6/100 = 900 ; annuo = 900*0.1206 = 108.54 ;
#                €/100km = 6*0.1206 = 0.7236
#   auto benzina: litri = 12000*7/100 = 840 ; annuo = 840*0.10395 = 87.318 ;
#                 €/100km = 7*0.10395 = 0.72765
#   risc gas: 15000*9.09 = 136350.0 ; risc gasolio: 2000*0.1206 = 241.2
ROW_DIESEL = _F["mh596_fuel_row"]("Diesel", "€/l", 1.70, 0.1206)


class TestW596Validatori:
    def test_num_ok(self):
        assert _F["mh596_num"](2, "x") == 2.0
        assert _F["mh596_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "2", None, [1], math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh596_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh596_nneg"](0, "x") == 0.0
        assert _F["mh596_nneg"](1.5, "x") == 1.5
        with pytest.raises(ValueError):
            _F["mh596_nneg"](-0.1, "x")

    def test_pct(self):
        assert _F["mh596_pct"](0, "x") == 0.0
        assert _F["mh596_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1, "x", True):
            with pytest.raises(ValueError):
                _F["mh596_pct"](bad, "x")

    def test_anno(self):
        for a in (2027, 2028, 2029, 2030, 2027.0):
            assert _F["mh596_anno"](a) == int(a)
        for bad in (2026, 2031, 2027.5, "2027", True, None):
            with pytest.raises(ValueError):
                _F["mh596_anno"](bad)


class TestW596Conversioni:
    def test_ef(self):
        assert _F["mh596_ef_kg_l"]("diesel") == 2.68
        assert _F["mh596_ef_kg_l"]("Benzina") == 2.31
        assert _F["mh596_ef_kg_l"]("GASOLIO") == 2.68
        assert _F["mh596_ef_kg_l"]("gpl") == 1.53
        for bad in ("kerosene", "", None, 2.68):
            with pytest.raises(ValueError):
                _F["mh596_ef_kg_l"](bad)

    def test_costo_litro(self):
        assert _F["mh596_costo_litro"](45.0, "diesel") == pytest.approx(0.1206)
        assert _F["mh596_costo_litro"](45.0, "benzina") == pytest.approx(
            0.10395)
        assert _F["mh596_costo_litro"](45.0, "gpl") == pytest.approx(0.06885)
        assert _F["mh596_costo_litro"](0.0, "diesel") == 0.0
        with pytest.raises(ValueError):
            _F["mh596_costo_litro"](-1.0, "diesel")

    def test_costo_mwh_gas(self):
        # 45*0.202 = 9.09
        assert _F["mh596_costo_mwh_gas"](45.0) == pytest.approx(9.09)
        assert _F["mh596_costo_mwh_gas"](100.0) == pytest.approx(20.2)
        with pytest.raises(ValueError):
            _F["mh596_costo_mwh_gas"](-5.0)

    def test_prezzo_finale(self):
        assert _F["mh596_prezzo_finale"](1.70, 0.1206) == pytest.approx(1.8206)
        assert _F["mh596_prezzo_finale"](0.0, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh596_prezzo_finale"](-1.0, 0.1)

    def test_quota_pct(self):
        # 0.1206/1.8206*100 = 6.6241898
        assert _F["mh596_quota_pct"](0.1206, 1.8206) == pytest.approx(6.62419,
                                                                     abs=1e-4)
        assert _F["mh596_quota_pct"](0.0, 5.0) == 0.0
        for bad in ((1.0, 0.0), (1.0, -2.0)):
            with pytest.raises(ValueError):
                _F["mh596_quota_pct"](*bad)


class TestW596Usi:
    def test_auto_diesel(self):
        v = _F["mh596_costo_auto"](15000.0, 6.0, 0.1206)
        assert v["litri_anno"] == pytest.approx(900.0)
        assert v["costo_annuo"] == pytest.approx(108.54)
        assert v["costo_100km"] == pytest.approx(0.7236)

    def test_auto_benzina(self):
        v = _F["mh596_costo_auto"](12000.0, 7.0, 0.10395)
        assert v["litri_anno"] == pytest.approx(840.0)
        assert v["costo_annuo"] == pytest.approx(87.318)
        assert v["costo_100km"] == pytest.approx(0.72765)

    def test_auto_ko(self):
        for bad in ((0, 6.0, 0.1), (-5, 6.0, 0.1), (15000, 0, 0.1),
                    (15000, 6.0, -0.1)):
            with pytest.raises(ValueError):
                _F["mh596_costo_auto"](*bad)

    def test_riscaldamento(self):
        assert _F["mh596_costo_riscaldamento"](15000.0, 9.09) == pytest.approx(
            136350.0)
        assert _F["mh596_costo_riscaldamento"](2000.0, 0.1206) == pytest.approx(
            241.2)
        with pytest.raises(ValueError):
            _F["mh596_costo_riscaldamento"](0, 9.09)

    def test_cap45(self):
        sotto = _F["mh596_cap45"](45.0)
        assert sotto["verdetto"] == "SOTTO_CAP"
        sopra = _F["mh596_cap45"](45.01)
        assert sopra["verdetto"] == "CAP_ATTIVO"
        assert "20 Mt" in sopra["nota"]


class TestW596RigaConfronto:
    def test_fuel_row_diesel(self):
        r = ROW_DIESEL
        assert r["nome"] == "Diesel"
        assert r["unita"] == "€/l"
        assert r["prezzo_base"] == 1.70
        assert r["costo_ets2"] == pytest.approx(0.1206)
        assert r["prezzo_finale"] == pytest.approx(1.8206)
        assert r["quota_pct"] == pytest.approx(6.62419, abs=1e-4)

    def test_fuel_row_ko(self):
        with pytest.raises(ValueError):
            _F["mh596_fuel_row"]("", "€/l", 1.7, 0.12)
        with pytest.raises(ValueError):
            _F["mh596_fuel_row"]("x", "", 1.7, 0.12)

    def test_confronto_piu_colpito(self):
        # quote: diesel 6.6242%, benzina 5.6069%, gas 8.7328% ->
        # piu' colpito = Gas naturale
        #   benzina: 0.10395/1.85395*100 = 5.6069473%
        #   gas: 9.09/104.09*100 = 8.7328274%
        righe = [
            _F["mh596_fuel_row"]("Diesel", "€/l", 1.70, 0.1206),
            _F["mh596_fuel_row"]("Benzina", "€/l", 1.75, 0.10395),
            _F["mh596_fuel_row"]("Gas naturale", "€/MWh", 95.0, 9.09),
        ]
        c = _F["mh596_confronto"](righe)
        assert c["piu_colpito"] == "Gas naturale"
        assert c["quota_max"] == pytest.approx(8.73283, abs=1e-4)
        assert len(c["righe"]) == 3

    def test_confronto_ko(self):
        with pytest.raises(ValueError):
            _F["mh596_confronto"]([])
        with pytest.raises(ValueError):
            _F["mh596_confronto"]([{"nome": "x"}])


class TestW596Demo:
    def test_demo(self):
        assert DEMO["prezzo_ets2"] == 45.0
        assert DEMO["anno"] == 2027
        assert DEMO["prezzi_base"]["diesel"] == 1.70
        assert DEMO["auto_diesel"]["km_anno"] == 15000.0
        assert DEMO["risc_gas_kwh"] == 15000.0
        assert DEMO["risc_gasolio_l"] == 2000.0


class TestW596Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 659
        assert TITLE596 in titles
        assert TITLE596 in titles

    def test_chain(self):
        assert ", tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659 = st.tabs([" in self._src()
        assert "with tab596:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st596_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab596:")[1].split(
                "# Footer")[0], pat
