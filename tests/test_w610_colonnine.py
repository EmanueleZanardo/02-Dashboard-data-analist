"""Test tab610 "🔌🚗 Colonnine di ricarica pubblica: il business case".

I valori della demo sono calcolati a mano nei commenti e contro-verificati
per plausibilita' (4x150 kW, 3,5 h/giorno, margine 0,37 eur/kWh -> VAN
ampiamente positivo, payback anno 2, break-even 0,59 h/giorno).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh610_num", "mh610_nneg", "mh610_pos", "mh610_frac01",
           "mh610_ore", "mh610_intero", "mh610_energia_annua_kwh",
           "mh610_ricavo_annuo", "mh610_costo_annuo", "mh610_ebitda",
           "mh610_flussi", "mh610_van", "mh610_tir", "mh610_payback",
           "mh610_breakeven_ore", "mh610_verdetto", "mh610_demo")

TITLE610 = "🔌🚗 Colonnine di ricarica pubblica: il business case"

# Demo: n=4, kw=150, ore=3,5, capex_u=45000, opex=48000, tariffa=0,55,
# costo_energia=0,18, anni=10, ramp=3, tasso=6%
DEMO = _F["mh610_demo"]()
E_FULL = 766500.0        # 4*150*3,5*365 kWh/anno
RIC3 = 421575.0          # E_FULL * 0,55
COSTO3 = 185970.0        # 48000 + E_FULL * 0,18
EBITDA3 = 235605.0       # RIC3 - COSTO3
CF0 = -180000.0          # -4 * 45000
VAN6 = 1291569.57        # somma flussi scontati al 6%
TIR_DEMO = 0.731588
PAYBACK = 2
BREAKEVEN = 0.592373     # 48000 / (4*150*365*0,37)


def _flussi_demo():
    d = DEMO
    return _F["mh610_flussi"](d["n"], d["kw"], d["ore_giorno"],
                              d["capex_unitario"], d["opex_fisso"],
                              d["tariffa"], d["costo_energia"],
                              d["anni"], d["anni_ramp"])


class TestW610Validatori:
    def test_num(self):
        assert _F["mh610_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh610_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh610_nneg"](0, "x") == 0.0
        assert _F["mh610_pos"](0.5, "x") == 0.5
        with pytest.raises(ValueError):
            _F["mh610_nneg"](-0.1, "x")
        with pytest.raises(ValueError):
            _F["mh610_pos"](0, "x")

    def test_frac01_ore(self):
        assert _F["mh610_frac01"](1, "x") == 1.0
        assert _F["mh610_ore"](24, "x") == 24.0
        with pytest.raises(ValueError):
            _F["mh610_frac01"](1.01, "x")
        with pytest.raises(ValueError):
            _F["mh610_ore"](24.1, "x")

    def test_intero(self):
        assert _F["mh610_intero"](4, "x", 1, 10) == 4
        assert _F["mh610_intero"](4.0, "x", 1, 10) == 4
        for bad in (True, 4.5, "4", 0, 11, float("nan")):
            with pytest.raises(ValueError):
                _F["mh610_intero"](bad, "x", 1, 10)


class TestW610Conti:
    def test_energia(self):
        assert _F["mh610_energia_annua_kwh"](4, 150.0, 3.5) == E_FULL
        with pytest.raises(ValueError):
            _F["mh610_energia_annua_kwh"](4, 150.0, 25.0)

    def test_ricavo_costo_ebitda(self):
        assert _F["mh610_ricavo_annuo"](E_FULL, 0.55) == pytest.approx(RIC3)
        assert _F["mh610_costo_annuo"](E_FULL, 48000.0, 0.18) == \
            pytest.approx(COSTO3)
        assert _F["mh610_ebitda"](RIC3, COSTO3) == pytest.approx(EBITDA3)

    def test_flussi_struttura(self):
        F = _flussi_demo()
        assert len(F) == 11  # anno 0..10
        assert F[0]["flusso"] == pytest.approx(CF0)
        assert F[0]["cumulato"] == pytest.approx(CF0)
        # ramp-up lineare: anno1 = 1/3, anno2 = 2/3, anno3 = pieno
        assert F[1]["energia_kwh"] == pytest.approx(E_FULL / 3.0)
        assert F[2]["energia_kwh"] == pytest.approx(2.0 * E_FULL / 3.0)
        assert F[3]["energia_kwh"] == pytest.approx(E_FULL)
        assert F[3]["ricavo"] == pytest.approx(RIC3)
        assert F[3]["costo"] == pytest.approx(COSTO3)
        assert F[3]["ebitda"] == pytest.approx(EBITDA3)
        assert F[10]["cumulato"] == pytest.approx(sum(r["flusso"] for r in F))

    def test_flussi_ramp_oltre_anni_errore(self):
        with pytest.raises(ValueError):
            _F["mh610_flussi"](4, 150.0, 3.5, 45000.0, 48000.0, 0.55, 0.18,
                              5, 6)

    def test_van(self):
        fl = [r["flusso"] for r in _flussi_demo()]
        assert _F["mh610_van"](fl, 0.0) == pytest.approx(sum(fl))
        assert _F["mh610_van"](fl, 0.06) == pytest.approx(VAN6, abs=1.0)
        assert _F["mh610_van"]([-100.0, 110.0], 0.10) == pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh610_van"]([], 0.06)

    def test_tir(self):
        assert _F["mh610_tir"]([-100.0, 60.0, 60.0]) == \
            pytest.approx(0.130662, abs=1e-4)
        fl = [r["flusso"] for r in _flussi_demo()]
        assert _F["mh610_tir"](fl) == pytest.approx(TIR_DEMO, abs=1e-4)
        assert _F["mh610_tir"]([-100.0, -10.0]) is None
        assert _F["mh610_tir"]([100.0, 10.0]) is None
        assert _F["mh610_tir"]([0.0, 0.0]) is None
        with pytest.raises(ValueError):
            _F["mh610_tir"]([])

    def test_payback(self):
        fl = [r["flusso"] for r in _flussi_demo()]
        assert _F["mh610_payback"](fl) == PAYBACK
        assert _F["mh610_payback"]([-100.0, 10.0, 10.0]) is None
        assert _F["mh610_payback"]([-100.0, 150.0]) == 1

    def test_breakeven(self):
        assert _F["mh610_breakeven_ore"](4, 150.0, 48000.0, 0.55, 0.18) == \
            pytest.approx(BREAKEVEN, abs=1e-6)
        # margine nullo o negativo -> mai in pareggio
        assert _F["mh610_breakeven_ore"](4, 150.0, 48000.0, 0.10, 0.18) \
            is None
        assert _F["mh610_breakeven_ore"](4, 150.0, 48000.0, 0.18, 0.18) \
            is None

    def test_verdetto(self):
        assert _F["mh610_verdetto"](1000.0, 2, 10)["verdetto"] == "CONVIENE"
        assert _F["mh610_verdetto"](1000.0, 8, 10)["verdetto"] == "MARGINALE"
        assert _F["mh610_verdetto"](1000.0, None, 10)["verdetto"] == \
            "MARGINALE"
        assert _F["mh610_verdetto"](-5.0, 2, 10)["verdetto"] == \
            "NON_CONVIENE"

    def test_demo_determinismo(self):
        assert _F["mh610_demo"]() == _F["mh610_demo"]()
        assert DEMO["n"] == 4 and DEMO["anni"] == 10


class TestW610Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab610:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 701
        assert TITLE610 in titles
        assert TITLE610 in titles

    def test_chain(self):
        assert ", tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701 = st.tabs([" in self._src()
        assert "with tab610:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st610_[a-z0-9_]+", self._ui()))
        attese = {"st610_n", "st610_kw", "st610_ore", "st610_capex",
                  "st610_opex", "st610_tariffa", "st610_costoen",
                  "st610_anni", "st610_ramp", "st610_tasso",
                  "st610_graf", "st610_tab", "st610_go", "st610_chart",
                  "st610_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st610_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W610 (21/10/2026)')[1]
        sec = sec.split('# W609 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
