"""Test tab567 "XVA: CVA + DVA + FVA + KVA + ColVA": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh567_num", "mh567_str", "mh567_pct", "mh567_posizione",
           "mh567_demo", "mh567_riepilogo")

TITLE567 = ("\U0001F4CA\U0001F3E6 XVA: CVA + DVA + FVA + KVA + ColVA "
            "(aggiustamenti di valutazione)")


def _v(pid="CP-1", descrizione="pos", epe=10_000_000.0, ene=2_000_000.0,
       pd=2.0, lgd=60.0, fca=100.0, cap=3_000_000.0, coc=10.0, **kw):
    return _F["mh567_posizione"](pid, descrizione, epe, ene, pd, lgd,
                                 fca, cap, coc, **kw)


class TestW567Validatori:
    def test_num_ok(self):
        assert _F["mh567_num"](2, "x") == 2.0
        assert _F["mh567_num"](-3.5, "x") == -3.5
        assert _F["mh567_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh567_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh567_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh567_str"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh567_pct"](0, "x") == 0.0
        assert _F["mh567_pct"](100, "x") == 100.0
        assert _F["mh567_pct"](2.5, "x") == 2.5

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "x", None):
            with pytest.raises(ValueError):
                _F["mh567_pct"](bad, "x")


class TestW567Posizione:
    def test_hand_computed(self):
        # CP-002 della demo: cva=-798000, dva=+22800, fva=-392000,
        # kva=-1080000, colva=-700000, xva=-2947200
        p = _F["mh567_posizione"]("CP-002", "Trading house",
                                  28_000_000.0, 9_500_000.0, 3.8, 75.0,
                                  140.0, 9_000_000.0, 12.0,
                                  ois_pct=2.5, csa_pct=0.0)
        assert p["cva"] == pytest.approx(-798_000.0)
        assert p["dva"] == pytest.approx(22_800.0)
        assert p["fva"] == pytest.approx(-392_000.0)
        assert p["kva"] == pytest.approx(-1_080_000.0)
        assert p["colva"] == pytest.approx(-700_000.0)
        assert p["xva"] == pytest.approx(-2_947_200.0)

    def test_colva_nulla_ois_uguale_csa(self):
        p = _v(ois_pct=2.5, csa_pct=2.5)
        assert p["colva"] == pytest.approx(0.0)

    def test_colva_segno(self):
        # CSA remunera piu' dell'OIS -> ColVA positiva (beneficio)
        p = _v(ois_pct=2.5, csa_pct=3.0)
        assert p["colva"] == pytest.approx(50_000.0)

    def test_default_ipotesi_globali(self):
        p = _v()
        # cva=-120000, dva=+4800, fva=-100000, kva=-300000, colva=0
        assert p["xva"] == pytest.approx(-515_200.0)

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(pd=101.0)
        with pytest.raises(ValueError):
            _v(lgd=-1.0)
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(epe=math.nan)


class TestW567Demo:
    def test_demo_shape(self):
        d = _F["mh567_demo"]()
        assert len(d) == 3
        assert all(set(p) >= {"cva", "dva", "fva", "kva", "colva",
                              "xva"} for p in d)

    def test_demo_verdetto(self):
        r = _F["mh567_riepilogo"](_F["mh567_demo"]())
        assert r["verdetto"] == "XVA_SIGNIFICATIVO"
        assert r["n_anomalie"] == 0
        assert r["epe_totale"] == pytest.approx(46_900_000.0)
        # |-4373130| / 46900000 * 100 ~= 9.3247
        assert r["xva_su_epe_pct"] == pytest.approx(9.3247, rel=1e-4)

    def test_demo_xva_totale(self):
        r = _F["mh567_riepilogo"](_F["mh567_demo"]())
        assert r["xva_totale"] == pytest.approx(-4_373_130.0)


class TestW567Riepilogo:
    def test_xva_contenuto_soglia_alta(self):
        r = _F["mh567_riepilogo"](_F["mh567_demo"](), soglia_pct=50.0)
        assert r["verdetto"] == "XVA_CONTENUTO"

    def test_nessuna_posizione(self):
        r = _F["mh567_riepilogo"]([_v(epe=0.0, ene=0.0)])
        assert r["verdetto"] == "NESSUNA_POSIZIONE"

    def test_anomalia_id_duplicato(self):
        r = _F["mh567_riepilogo"]([_v(pid="CP-X"), _v(pid="cp-x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_epe_negativa(self):
        r = _F["mh567_riepilogo"]([_v(pid="A"), _v(pid="Z", epe=-5.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_anomalia_ene_negativa(self):
        r = _F["mh567_riepilogo"]([_v(ene=-5.0)])
        assert r["n_anomalie"] == 1

    def test_anomalia_capitale_negativo(self):
        r = _F["mh567_riepilogo"]([_v(cap=-5.0)])
        assert r["n_anomalie"] == 1

    def test_anomalia_fca_negativo(self):
        r = _F["mh567_riepilogo"]([_v(fca=-10.0)])
        assert r["n_anomalie"] == 1

    def test_anomalie_prevalgono_su_significativo(self):
        r = _F["mh567_riepilogo"]([_v(pid="CP-X"), _v(pid="CP-X")],
                                  soglia_pct=0.5)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_sopra_soglia_per_posizione(self):
        r = _F["mh567_riepilogo"](_F["mh567_demo"](), soglia_pct=5.0)
        sopra = [p["sopra_soglia"] for p in r["analizzate"]]
        assert sopra == [False, True, True]

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh567_riepilogo"]([])

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh567_riepilogo"](_F["mh567_demo"](), soglia_pct=101.0)


class TestW567Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE567}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 732
        assert TITLE567 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732 = st.tabs([" in src
        assert "with tab567:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st567_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
