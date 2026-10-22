"""Test tab597 "🌍📉 MACC: curva dei costi di abbattimento CO₂".

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

_F = _load("mh597_num", "mh597_nneg", "mh597_pos", "mh597_pct",
           "mh597_crf", "mh597_misura", "mh597_macc", "mh597_verdetto",
           "mh597_demo")

TITLE597 = "🌍📉 MACC: curva dei costi di abbattimento CO₂"

DEMO = _F["mh597_demo"]()
# Demo (tasso 5%): CRF(5,10)=0.129505 ; CRF(5,12)=0.112825 ;
#   CRF(5,15)=0.096342 ; CRF(5,8)=0.154722 ; CRF(5,25)=0.070952.
# LED: t=400*0.35=140 ; annuo=50000*0.129505+2000=8475.25 ; €/t=60.5373
# VSD: t=600*0.35=210 ; annuo=120000*0.112825+1000=14539.05 ; €/t=69.2336
# Recupero: t=1500*0.202=303 ; annuo=200000*0.096342+3000=22268.46 ;
#   €/t=73.4933
# PdC: t=2000*0.202=404 ; annuo=300000*0.096342+5000=33902.69 ; €/t=83.9175
# Flotta: t=1100*0.27=297 ; annuo=400000*0.154722+10000-45000=26888.73 ;
#   €/t=90.5344
# FV: t=1300*0.35=455 ; annuo=900000*0.070952+12000=75857.21 ; €/t=166.7191
# Tot t = 1809 ; medio pond = 181930.9/1809 = 100.5701
# cum: 140, 350, 653, 1057, 1354, 1809
ROW_LED = _F["mh597_misura"]("LED + smart lighting", 50000.0, 2000.0, 0.0,
                             400.0, 0.35, 10.0, 5.0)


def _righe_demo():
    return [_F["mh597_misura"](
        m["nome"], m["capex"], m["opex_annuo"], m["risp_op_annuo"],
        m["risparmio_mwh_anno"], m["ef_t_mwh"], m["vita_anni"],
        DEMO["tasso_pct"]) for m in DEMO["misure"]]


class TestW597Validatori:
    def test_num_ok(self):
        assert _F["mh597_num"](2, "x") == 2.0
        assert _F["mh597_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "2", None, [1], math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh597_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh597_nneg"](0, "x") == 0.0
        assert _F["mh597_nneg"](1.5, "x") == 1.5
        with pytest.raises(ValueError):
            _F["mh597_nneg"](-0.1, "x")

    def test_pos(self):
        assert _F["mh597_pos"](0.1, "x") == 0.1
        for bad in (0.0, -1.0, "x", True):
            with pytest.raises(ValueError):
                _F["mh597_pos"](bad, "x")

    def test_pct(self):
        assert _F["mh597_pct"](0, "x") == 0.0
        assert _F["mh597_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1, "x", True):
            with pytest.raises(ValueError):
                _F["mh597_pct"](bad, "x")


class TestW597Crf:
    def test_crf_5_10(self):
        assert _F["mh597_crf"](5, 10) == pytest.approx(0.129505, abs=1e-6)

    def test_crf_5_15(self):
        assert _F["mh597_crf"](5, 15) == pytest.approx(0.096342, abs=1e-6)

    def test_crf_zero(self):
        assert _F["mh597_crf"](0, 10) == pytest.approx(0.1)

    def test_crf_ko(self):
        for bad in (-1, 101, "5", True):
            with pytest.raises(ValueError):
                _F["mh597_crf"](bad, 10)
        with pytest.raises(ValueError):
            _F["mh597_crf"](5, 0)


class TestW597Misura:
    def test_led(self):
        r = ROW_LED
        assert r["nome"] == "LED + smart lighting"
        assert r["tco2_annue"] == pytest.approx(140.0)
        assert r["costo_annuo"] == pytest.approx(8475.25, abs=0.05)
        assert r["costo_t"] == pytest.approx(60.5373, abs=1e-3)

    def test_fv(self):
        r = _F["mh597_misura"]("FV su tetto (1 MWp)", 900000.0, 12000.0,
                               0.0, 1300.0, 0.35, 25.0, 5.0)
        assert r["tco2_annue"] == pytest.approx(455.0)
        assert r["costo_annuo"] == pytest.approx(75857.21, abs=0.1)
        assert r["costo_t"] == pytest.approx(166.7191, abs=1e-3)

    def test_risparmio_operativo(self):
        # la flotta sottrae il diesel evitato dal costo annuo
        r = _F["mh597_misura"]("Elettrificazione flotta", 400000.0,
                               10000.0, 45000.0, 1100.0, 0.27, 8.0, 5.0)
        assert r["costo_annuo"] == pytest.approx(26888.73, abs=0.1)
        assert r["costo_t"] == pytest.approx(90.5344, abs=1e-3)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh597_misura"]("", 1, 0, 0, 1, 0.35, 10, 5)
        with pytest.raises(ValueError):
            _F["mh597_misura"]("x", -1, 0, 0, 1, 0.35, 10, 5)
        with pytest.raises(ValueError):
            _F["mh597_misura"]("x", 1, 0, 0, 0, 0.35, 10, 5)
        with pytest.raises(ValueError):
            _F["mh597_misura"]("x", 1, 0, 0, 1, 0, 10, 5)
        with pytest.raises(ValueError):
            _F["mh597_misura"]("x", 1, 0, 0, 1, 0.35, 0, 5)


class TestW597Macc:
    def test_ordine_e_cumulate(self):
        m = _F["mh597_macc"](_righe_demo())
        nomi = [r["nome"] for r in m["righe"]]
        assert nomi == ["LED + smart lighting", "Motori efficienti (VSD)",
                        "Recupero calore di scarto",
                        "Pompa di calore vs caldaia",
                        "Elettrificazione flotta", "FV su tetto (1 MWp)"]
        assert [r["rank"] for r in m["righe"]] == [1, 2, 3, 4, 5, 6]
        assert [r["tco2_cumulate"] for r in m["righe"]] == [
            140.0, 350.0, 653.0, 1057.0, 1354.0, 1809.0]

    def test_totali(self):
        m = _F["mh597_macc"](_righe_demo())
        assert m["tot_tco2_annue"] == pytest.approx(1809.0)
        assert m["costo_medio_pond"] == pytest.approx(100.5701, abs=1e-3)
        assert m["n_misure"] == 6

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh597_macc"]([])
        with pytest.raises(ValueError):
            _F["mh597_macc"]([{"nome": "x"}])


class TestW597Verdetto:
    def test_sotto(self):
        v = _F["mh597_verdetto"](60.54, 75.0)
        assert v["conveniente"] is True
        assert v["verdetto"] == "SOTTO_PREZZO"
        assert v["delta"] == pytest.approx(14.46, abs=1e-6)

    def test_sopra(self):
        v = _F["mh597_verdetto"](166.72, 75.0)
        assert v["conveniente"] is False
        assert v["verdetto"] == "SOPRA_PREZZO"
        assert v["delta"] == pytest.approx(91.72, abs=1e-6)

    def test_uguale_non_conveniente(self):
        v = _F["mh597_verdetto"](75.0, 75.0)
        assert v["conveniente"] is False
        assert v["verdetto"] == "SOPRA_PREZZO"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh597_verdetto"]("x", 75.0)
        with pytest.raises(ValueError):
            _F["mh597_verdetto"](60.0, -1.0)


class TestW597Demo:
    def test_demo(self):
        assert DEMO["prezzo_co2"] == 75.0
        assert DEMO["tasso_pct"] == 5.0
        assert len(DEMO["misure"]) == 6
        assert DEMO["misure"][0]["nome"] == "LED + smart lighting"
        assert DEMO["misure"][-1]["capex"] == 900000.0


class TestW597Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 645
        assert TITLE597 in titles
        assert TITLE597 in titles

    def test_chain(self):
        assert ", tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645 = st.tabs([" in self._src()
        assert "with tab597:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab597:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st597_[a-z0-9_]+", ui))
        assert len(keys) >= 9, keys
        # chiavi dinamiche per misura: 6 misure x 6 input via f-string
        dyn = set(re.findall(r"st597_\{_i597\}_[a-z]+", ui))
        assert dyn == {"st597_{_i597}_capex", "st597_{_i597}_opex",
                       "st597_{_i597}_rispop", "st597_{_i597}_mwh",
                       "st597_{_i597}_ef", "st597_{_i597}_vita"}, dyn
        # unicita' effettiva: 6 misure x 6 + 9 statiche = 45 chiavi
        reali = {f"st597_{i}_{s}" for i in range(6)
                 for s in ("capex", "opex", "rispop", "mwh", "ef", "vita")}
        assert len(reali | keys) == 45

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab597:")[1].split(
                "# Footer")[0], pat
