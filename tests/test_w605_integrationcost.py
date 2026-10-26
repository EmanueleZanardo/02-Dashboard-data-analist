"""Test tab605 "🌐⚡ Integration cost: profile + balancing + grid".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper) e contro-verificati con gli helper stessi.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh605_num", "mh605_nneg", "mh605_pos", "mh605_pct",
           "mh605_str", "mh605_parse_serie", "mh605_prezzo_base",
           "mh605_prezzo_cattura", "mh605_costo_profilo",
           "mh605_costo_bilanciamento", "mh605_crf", "mh605_costo_rete",
           "mh605_integration_cost", "mh605_integration_pct",
           "mh605_valore_netto", "mh605_margine", "mh605_verdetto",
           "mh605_sensibilita_errore", "mh605_demo")

TITLE605 = "🌐⚡ Integration cost: profile + balancing + grid"

DEMO = _F["mh605_demo"]()
# Demo: prezzi 12x80 + 12x40 -> p_bar = (12*80+12*40)/24 = 60,0
# profilo 12 zeri + 12 uni -> sum g = 12
# p_cattura = (12*40*1)/12 = 40,0 ; pc = 60-40 = 20,0
# bc = 0,15 * 0,7978845608028654 * 20 = 2,393653682408596
# CRF(6%,25) = 0,06*1,06^25/(1,06^25-1) = 0,07822671821227395
# E_annua = 100 MW * 1000 h = 100000 MWh
# gc = 10e6 * 0,07822671821227395 / 100000 = 7,822671821227395
# ic = 20 + 2,393653682408596 + 7,822671821227395 = 30,216325503635993
# ic% = 30,216325503635993/40*100 = 75,54081375908999
# vn = 40 - 30,216325503635993 = 9,783674496364007
# margine = 9,783674496364007 - 25 = -15,216325503635993
P_BAR = 60.0
P_CAP = 40.0
PC = 20.0
BC = 2.393653682408596
CRF = 0.07822671821227395
GC = 7.822671821227395
IC = 30.216325503635993
ICPCT = 75.54081375908999
VN = 9.783674496364007
MARG = -15.216325503635993
# sensibilita' errore 0..30 passo 5 (pc=20, gc=GC, p_cap=40, lcoe=25):
# err=0:  bc=0 -> ic=27,822671821227395 vn=12,177328178772605
#                marg=-12,822671821227395
# err=30: bc=0,30*0,7978845608028654*20=4,787307364817192
#         ic=32,60997918604458 vn=7,390020813955417 marg=-17,609979186044583
S0_BC = 0.0
S0_IC = 27.822671821227395
S0_MARG = -12.822671821227395
S30_BC = 4.787307364817192
S30_IC = 32.60997918604458
S30_MARG = -17.609979186044583


class TestW605Validatori:
    def test_num(self):
        assert _F["mh605_num"](2, "x") == 2.0
        assert _F["mh605_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh605_num"](bad, "x")

    def test_nneg_pos_pct_str(self):
        assert _F["mh605_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh605_nneg"](-0.1, "x")
        assert _F["mh605_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh605_pos"](bad, "x")
        assert _F["mh605_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh605_pct"](bad, "x")
        assert _F["mh605_str"]("a", "x") == "a"
        with pytest.raises(ValueError):
            _F["mh605_str"](1, "x")

    def test_parse_serie(self):
        f = _F["mh605_parse_serie"]
        assert f("1, 2;3\n4", "s") == [1.0, 2.0, 3.0, 4.0]
        for bad in ("", "   ", "1, x", "1, nan"):
            with pytest.raises(ValueError):
                f(bad, "s")


class TestW605Prezzi:
    def test_prezzo_base(self):
        assert _F["mh605_prezzo_base"](DEMO["prezzi"]) == pytest.approx(P_BAR)
        with pytest.raises(ValueError):
            _F["mh605_prezzo_base"]([])

    def test_prezzo_cattura(self):
        assert _F["mh605_prezzo_cattura"](DEMO["prezzi"],
                                          DEMO["profilo"]) == \
            pytest.approx(P_CAP)
        for bad_p, bad_g in (([1.0], [1.0, 2.0]),
                             ([1.0, 2.0], [0.0, 0.0]),
                             ([1.0], [-1.0])):
            with pytest.raises(ValueError):
                _F["mh605_prezzo_cattura"](bad_p, bad_g)

    def test_costo_profilo(self):
        assert _F["mh605_costo_profilo"](P_BAR, P_CAP) == pytest.approx(PC)
        # profilo "inverso" (produce nelle ore care) -> pc negativo
        assert _F["mh605_costo_profilo"](40.0, 60.0) == pytest.approx(-20.0)


class TestW605Componenti:
    def test_balancing(self):
        assert _F["mh605_costo_bilanciamento"](15.0, 20.0) == \
            pytest.approx(BC)
        assert _F["mh605_costo_bilanciamento"](0.0, 20.0) == \
            pytest.approx(0.0)
        assert _F["mh605_costo_bilanciamento"](100.0, 10.0) == \
            pytest.approx(0.7978845608028654 * 10.0)
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh605_costo_bilanciamento"](bad, 20.0)

    def test_crf(self):
        assert _F["mh605_crf"](6.0, 25) == pytest.approx(CRF)
        assert _F["mh605_crf"](0.0, 10) == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh605_crf"](6.0, 0)

    def test_costo_rete(self):
        assert _F["mh605_costo_rete"](10_000_000.0, 6.0, 25,
                                      100_000.0) == pytest.approx(GC)
        assert _F["mh605_costo_rete"](0.0, 6.0, 25, 100_000.0) == \
            pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh605_costo_rete"](1.0, 6.0, 25, 0.0)

    def test_integration(self):
        assert _F["mh605_integration_cost"](PC, BC, GC) == pytest.approx(IC)
        assert _F["mh605_integration_pct"](IC, P_CAP) == pytest.approx(ICPCT)
        with pytest.raises(ValueError):
            _F["mh605_integration_pct"](IC, 0.0)

    def test_valore_netto_margine(self):
        assert _F["mh605_valore_netto"](P_CAP, IC) == pytest.approx(VN)
        assert _F["mh605_margine"](VN, 25.0) == pytest.approx(MARG)
        assert _F["mh605_margine"](VN, 0.0) == pytest.approx(VN)


class TestW605Verdetto:
    def test_bordi(self):
        v = _F["mh605_verdetto"]
        assert v(MARG)["verdetto"] == "NON_REDDITIZIO"
        assert v(5.0)["verdetto"] == "REDDITIZIO"
        assert v(100.0)["verdetto"] == "REDDITIZIO"
        assert v(4.99)["verdetto"] == "MARGINALE"
        assert v(-5.0)["verdetto"] == "MARGINALE"
        assert v(-5.01)["verdetto"] == "NON_REDDITIZIO"
        assert "msg" in v(0.0) and v(0.0)["msg"]


class TestW605Sensibilita:
    def _scan(self):
        return _F["mh605_sensibilita_errore"](
            DEMO["prezzi"], DEMO["profilo"], 20.0, 0.0, 30.0, 5.0,
            10_000_000.0, 6.0, 25, 100_000.0, 25.0)

    def test_geometria(self):
        sc = self._scan()
        assert len(sc) == 7
        assert sc[0]["errore_pct"] == pytest.approx(0.0)
        assert sc[-1]["errore_pct"] == pytest.approx(30.0)

    def test_righe_estreme(self):
        sc = self._scan()
        assert sc[0]["balancing"] == pytest.approx(S0_BC)
        assert sc[0]["ic"] == pytest.approx(S0_IC)
        assert sc[0]["margine"] == pytest.approx(S0_MARG)
        assert sc[-1]["balancing"] == pytest.approx(S30_BC)
        assert sc[-1]["ic"] == pytest.approx(S30_IC)
        assert sc[-1]["margine"] == pytest.approx(S30_MARG)

    def test_monotona(self):
        sc = self._scan()
        ics = [r["ic"] for r in sc]
        assert all(b > a for a, b in zip(ics, ics[1:]))

    def test_errori_input(self):
        args = (DEMO["prezzi"], DEMO["profilo"], 20.0, 0.0, 30.0, 5.0,
                10_000_000.0, 6.0, 25, 100_000.0, 25.0)
        with pytest.raises(ValueError):
            _F["mh605_sensibilita_errore"](*args[:3], 30.0, 0.0, 5.0,
                                           *args[6:])
        with pytest.raises(ValueError):
            _F["mh605_sensibilita_errore"](*args[:5], 0.0, *args[6:])

    def test_demo(self):
        d = DEMO
        assert len(d["prezzi"]) == 24
        assert len(d["profilo"]) == 24
        assert d["taglia_mw"] == 100.0
        assert d["lcoe"] == 25.0


class TestW605Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab605:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 720
        assert TITLE605 in titles
        assert TITLE605 in titles

    def test_chain(self):
        assert ", tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720 = st.tabs([" in self._src()
        assert "with tab605:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st605_[a-z0-9_]+", self._ui()))
        attese = {"st605_prezzi", "st605_profilo", "st605_oreeq",
                  "st605_errore", "st605_spread", "st605_capex",
                  "st605_tasso", "st605_anni", "st605_lcoe",
                  "st605_taglia", "st605_tabc", "st605_graf",
                  "st605_go", "st605_chart", "st605_tab", "st605_csv"}
        assert keys == attese, keys ^ attese

    def test_helpers(self):
        src = self._src()
        mh = set(re.findall(r"def (mh605_\w+)\(", src))
        attesi = {"mh605_num", "mh605_nneg", "mh605_pos", "mh605_pct",
                  "mh605_str", "mh605_parse_serie", "mh605_prezzo_base",
                  "mh605_prezzo_cattura", "mh605_costo_profilo",
                  "mh605_costo_bilanciamento", "mh605_crf",
                  "mh605_costo_rete", "mh605_integration_cost",
                  "mh605_integration_pct", "mh605_valore_netto",
                  "mh605_margine", "mh605_verdetto",
                  "mh605_sensibilita_errore", "mh605_demo"}
        assert mh == attesi, (mh ^ attesi)

    def test_no_secrets(self):
        src = self._ui().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src, pat
