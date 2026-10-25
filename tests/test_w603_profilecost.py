"""Test tab603 "⚡📊 Profile cost: il costo della forma".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh603_num", "mh603_nneg", "mh603_pos", "mh603_pct",
           "mh603_str", "mh603_parse_serie", "mh603_media",
           "mh603_cattura", "mh603_fattore_valore", "mh603_costo_profilo",
           "mh603_costo_profilo_pct", "mh603_tabella_oraria",
           "mh603_curva_cannibal", "mh603_verdetto", "mh603_demo")

TITLE603 = "⚡📊 Profile cost: il costo della forma"

DEMO = _F["mh603_demo"]()
# Demo: 24 prezzi e 24 generazioni (FV 100 MWp, mezzogiorno depresso).
# prezzi: 7x80 + [75,70,65,60,55,52,55,60,65,70,75] + 4x90 + 2x85
#   somma = 560 + 707 + 360 + 170 = 1797 -> base = 1797/24 = 74,875? NO:
#   75+70+65+60+55+52+55+60+65+70+75 = 702 -> somma = 560+702+360+170 = 1792
#   base = 1792/24 = 74,66666666666667
# gen: 7x0 + [5,15,30,50,65,70,65,50,30,15,5] + 6x0
#   somma gen = 400 MW (di picco g_max = 70)
# Σ p·g = 5*75+15*70+30*65+50*60+65*55+70*52+65*55+50*60+30*65+15*70+5*75
#       = 375+1050+1950+3000+3575+3640+3575+3000+1950+1050+375 = 23540
# cattura = 23540/400 = 58,85
# pc = 74,66666666666667 − 58,85 = 15,816666666666666
# vf = 58,85/74,66666666666667 = 0,7881696428571429
# pc% = 15,816666666666666/74,66666666666667*100 = 21,183035714285715
# verdetto: vf < 0,80 -> COSTO_ELEVATO
BASE = 74.66666666666667
CAPT = 58.85
PC = 15.816666666666666
VF = 0.7881696428571429
PCPCT = 21.183035714285715


class TestW603Validatori:
    def test_num(self):
        assert _F["mh603_num"](2, "x") == 2.0
        assert _F["mh603_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh603_num"](bad, "x")

    def test_nneg_pos_pct_str(self):
        assert _F["mh603_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh603_nneg"](-0.1, "x")
        assert _F["mh603_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh603_pos"](bad, "x")
        assert _F["mh603_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh603_pct"](bad, "x")
        assert _F["mh603_str"]("abc", "x") == "abc"
        with pytest.raises(ValueError):
            _F["mh603_str"](123, "x")

    def test_parse_serie(self):
        p = _F["mh603_parse_serie"]
        assert p("1, 2;3\n4 5", "s") == [1.0, 2.0, 3.0, 4.0, 5.0]
        assert p("  10.5 ", "s") == [10.5]
        with pytest.raises(ValueError):
            p("", "s")
        with pytest.raises(ValueError):
            p("1, due", "s")
        with pytest.raises(ValueError):
            p("1, nan", "s")
        with pytest.raises(ValueError):
            p(123, "s")


class TestW603Core:
    def test_media(self):
        assert _F["mh603_media"]([1.0, 2.0, 3.0]) == pytest.approx(2.0)
        with pytest.raises(ValueError):
            _F["mh603_media"]([])

    def test_cattura(self):
        # hand: (10*1 + 20*3) / 4 = 70/4 = 17,5
        assert _F["mh603_cattura"]([10.0, 20.0], [1.0, 3.0]) == \
            pytest.approx(17.5)
        with pytest.raises(ValueError):
            _F["mh603_cattura"]([10.0], [1.0, 2.0])
        with pytest.raises(ValueError):
            _F["mh603_cattura"]([10.0, 20.0], [0.0, 0.0])

    def test_fattore_valore(self):
        assert _F["mh603_fattore_valore"](58.85, 74.66666666666667) == \
            pytest.approx(VF)
        assert _F["mh603_fattore_valore"](80.0, 80.0) == pytest.approx(1.0)
        with pytest.raises(ValueError):
            _F["mh603_fattore_valore"](58.85, 0)

    def test_costo_profilo(self):
        assert _F["mh603_costo_profilo"](CAPT, BASE) == pytest.approx(PC)
        # premio di forma: cattura > base -> costo negativo
        assert _F["mh603_costo_profilo"](90.0, 80.0) == pytest.approx(-10.0)

    def test_costo_profilo_pct(self):
        assert _F["mh603_costo_profilo_pct"](PC, BASE) == \
            pytest.approx(PCPCT)
        with pytest.raises(ValueError):
            _F["mh603_costo_profilo_pct"](PC, 0)

    def test_tabella_oraria(self):
        t = _F["mh603_tabella_oraria"]([10.0, 20.0, 30.0],
                                       [1.0, 3.0, 2.0], 20.0)
        assert len(t) == 3
        # quota gen: 1/6, 3/6, 2/6
        assert t[0]["quota_gen_pct"] == pytest.approx(100.0 / 6)
        assert t[1]["ricavo_eur"] == pytest.approx(60.0)
        assert t[2]["scost_vs_base"] == pytest.approx(10.0)
        assert t[0]["scost_pesato"] == pytest.approx(-10.0)
        # Σ ricavo = cattura * Σ gen
        cap = _F["mh603_cattura"]([10.0, 20.0, 30.0], [1.0, 3.0, 2.0])
        assert sum(r["ricavo_eur"] for r in t) == pytest.approx(cap * 6.0)
        assert sum(r["quota_gen_pct"] for r in t) == pytest.approx(100.0)
        with pytest.raises(ValueError):
            _F["mh603_tabella_oraria"]([10.0], [1.0, 2.0], 20.0)


class TestW603CurvaVerdetto:
    def test_curva_monotona(self):
        p, g = DEMO["prezzi"], DEMO["gen_mw"]
        righe = _F["mh603_curva_cannibal"](p, g, 0.8, [0.0, 2.0, 5.0, 10.0])
        assert len(righe) == 4
        pcs = [r["costo_profilo"] for r in righe]
        assert pcs[0] == pytest.approx(PC)
        # la cannibalizzazione alza il profile cost (monotona)
        assert all(b >= a for a, b in zip(pcs, pcs[1:]))
        vfs = [r["fattore_valore"] for r in righe]
        assert all(b <= a for a, b in zip(vfs, vfs[1:]))
        # q=10: base = 74,6667 − 0,8·10·(400/70)/24
        #       = 74,6667 − 1,9047619 = 72,76190476190476
        assert righe[3]["prezzo_medio"] == pytest.approx(72.76190476190476)
        assert righe[3]["costo_profilo"] == pytest.approx(19.81190476190476)
        with pytest.raises(ValueError):
            _F["mh603_curva_cannibal"](p, g, 0.8, [])
        with pytest.raises(ValueError):
            _F["mh603_curva_cannibal"](p, g, -1.0, [5.0])

    def test_verdetto_bordi(self):
        assert _F["mh603_verdetto"](1.10)["verdetto"] == "PREMIO"
        assert _F["mh603_verdetto"](1.05)["verdetto"] == "PREMIO"
        assert _F["mh603_verdetto"](1.04)["verdetto"] == "NEUTRO"
        assert _F["mh603_verdetto"](0.95)["verdetto"] == "NEUTRO"
        assert _F["mh603_verdetto"](0.94)["verdetto"] == "COSTO_MODERATO"
        assert _F["mh603_verdetto"](0.80)["verdetto"] == "COSTO_MODERATO"
        assert _F["mh603_verdetto"](0.79)["verdetto"] == "COSTO_ELEVATO"


class TestW603Demo:
    def test_demo_valori(self):
        assert len(DEMO["prezzi"]) == 24
        assert len(DEMO["gen_mw"]) == 24
        base = _F["mh603_media"](DEMO["prezzi"])
        assert base == pytest.approx(BASE)
        cap = _F["mh603_cattura"](DEMO["prezzi"], DEMO["gen_mw"])
        assert cap == pytest.approx(CAPT)
        pc = _F["mh603_costo_profilo"](cap, base)
        assert pc == pytest.approx(PC)
        vf = _F["mh603_fattore_valore"](cap, base)
        assert vf == pytest.approx(VF)
        assert _F["mh603_verdetto"](vf)["verdetto"] == "COSTO_ELEVATO"


class TestW603Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab603:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 716
        assert TITLE603 in titles
        assert TITLE603 in titles

    def test_chain(self):
        assert ", tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716 = st.tabs([" in self._src()
        assert "with tab603:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st603_[a-z0-9_]+", self._ui()))
        attese = {"st603_prezzi", "st603_gen", "st603_targa", "st603_k",
                  "st603_sep", "st603_quote", "st603_tabc", "st603_gcan",
                  "st603_go", "st603_tab", "st603_csv", "st603_chart",
                  "st603_csv2"}
        assert keys == attese, keys ^ attese

    def test_helpers(self):
        src = self._src()
        mh = set(re.findall(r"def (mh603_\w+)\(", src))
        attesi = {"mh603_num", "mh603_nneg", "mh603_pos", "mh603_pct",
                  "mh603_str", "mh603_parse_serie", "mh603_media",
                  "mh603_cattura", "mh603_fattore_valore",
                  "mh603_costo_profilo", "mh603_costo_profilo_pct",
                  "mh603_tabella_oraria", "mh603_curva_cannibal",
                  "mh603_verdetto", "mh603_demo"}
        assert mh == attesi, (mh ^ attesi)

    def test_no_secrets(self):
        src = self._ui().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src, pat
