"""Test tab572 "Fair value hedges del rischio di credito (IFRS 7.11)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh572_num", "mh572_str", "mh572_posizione", "mh572_demo",
           "mh572_riepilogo")

TITLE572 = "🔗📊 Fair value hedges del rischio di credito (IFRS 7.11)"


def _p(pid="HDG-1", descrizione="posizione", fv=100_000_000.0,
       ex=100_000_000.0, no=60_000_000.0, pa=-2_000_000.0,
       ca=-8_000_000.0, ph=1_900_000.0, ch=7_500_000.0):
    return _F["mh572_posizione"](pid, descrizione, fv, ex, no, pa, ca,
                                 ph, ch)


class TestW572Validatori:
    def test_num_ok(self):
        assert _F["mh572_num"](2, "x") == 2.0
        assert _F["mh572_num"](-3.5, "x") == -3.5
        assert _F["mh572_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh572_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh572_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh572_str"](bad, "x")


class TestW572Posizione:
    def test_hand_computed(self):
        r = _p(pid="HDG-001", fv=45_000_000.0, ex=45_000_000.0,
               no=40_000_000.0, pa=-800_000.0, ca=-3_200_000.0,
               ph=750_000.0, ch=3_000_000.0)
        assert r["id"] == "HDG-001"
        assert r["residuo"] == pytest.approx(5_000_000.0)
        assert r["hedge_ratio"] == pytest.approx(40.0 / 45.0)
        assert r["netta_cumulata"] == pytest.approx(-200_000.0)

    def test_residuo_floor_zero(self):
        # overhedge entro il 2x: la voce non respinge, residuo floora a 0
        r = _p(ex=100.0, no=150.0, fv=100.0, ca=0.0, ch=0.0)
        assert r["residuo"] == 0.0
        assert r["hedge_ratio"] == pytest.approx(1.5)

    def test_hedge_ratio_none_exp_zero(self):
        r = _p(ex=0.0, no=0.0, fv=0.0, ca=0.0, ch=0.0)
        assert r["hedge_ratio"] is None
        assert r["residuo"] == 0.0

    def test_str_strip(self):
        r = _p(pid="  HDG-X ", descrizione=" pos ")
        assert r["id"] == "HDG-X"
        assert r["descrizione"] == "pos"


class TestW572Riepilogo:
    def test_demo_rischio_residuo_significativo(self):
        r = _F["mh572_riepilogo"](_F["mh572_demo"]())
        # exp 85M, nominale 67M -> residuo 18M > 10M
        assert r["esposizione_max_totale"] == pytest.approx(85_000_000.0)
        assert r["nominale_hedge_totale"] == pytest.approx(67_000_000.0)
        assert r["residuo_totale"] == pytest.approx(18_000_000.0)
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "RISCHIO_RESIDUO_SIGNIFICATIVO"

    def test_demo_netta_cumulata_efficacia(self):
        r = _F["mh572_riepilogo"](_F["mh572_demo"]())
        netta = [a["netta_cumulata"] for a in r["analizzate"]]
        assert netta == pytest.approx([-200_000.0, -100_000.0,
                                       -20_000.0])

    def test_copertura_adeguata(self):
        r = _F["mh572_riepilogo"](
            [_p(pid="HDG-A", ex=50_000_000.0, no=50_000_000.0,
                fv=50_000_000.0, ca=-1_000_000.0, ch=990_000.0)])
        assert r["residuo_totale"] == pytest.approx(0.0)
        assert r["verdetto"] == "COPERTURA_ADEGUATA"

    def test_residuo_boundary_soglia(self):
        # residuo == soglia -> non significativo (>, non >=)
        r = _F["mh572_riepilogo"](
            [_p(ex=20_000_000.0, no=10_000_000.0, fv=20_000_000.0,
                ca=0.0, ch=0.0)],
            soglia_residuo_eur=10_000_000.0)
        assert r["residuo_totale"] == pytest.approx(10_000_000.0)
        assert r["verdetto"] == "COPERTURA_ADEGUATA"

    def test_soglia_personalizzata(self):
        r = _F["mh572_riepilogo"](_F["mh572_demo"](),
                                  soglia_residuo_eur=20_000_000.0)
        assert r["verdetto"] == "COPERTURA_ADEGUATA"

    def test_id_duplicato_anomalia(self):
        r = _F["mh572_riepilogo"]([_p(pid="HDG-X"), _p(pid="hdg-x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a
                   for a in r["analizzate"][1]["anomalie"])

    def test_fv_negativo_anomalia(self):
        r = _F["mh572_riepilogo"]([_p(fv=-5.0, ca=0.0, ch=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("fair value" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_esposizione_negativa_anomalia(self):
        r = _F["mh572_riepilogo"]([_p(ex=-5.0, ca=0.0, ch=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("negativa" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_nominale_negativo_anomalia(self):
        r = _F["mh572_riepilogo"]([_p(no=-1.0, ca=0.0, ch=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_overhedge_anomalo(self):
        r = _F["mh572_riepilogo"]([_p(ex=100.0, no=250.0, fv=100.0,
                                      ca=0.0, ch=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("overhedge" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_overhedge_boundary_2x_ok(self):
        # nominale == 2x esposizione: non anomalo (>, non >=)
        r = _F["mh572_riepilogo"]([_p(ex=100.0, no=200.0, fv=100.0,
                                      ca=0.0, ch=0.0)])
        assert r["n_anomalie"] == 0

    def test_cumulata_eccede_fv_anomalia(self):
        r = _F["mh572_riepilogo"]([_p(fv=100.0, ca=-150.0, ch=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("eccede" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_cumulata_eccede_fv_non_scatta_se_fv_negativo(self):
        # fv negativo: solo l'anomalia sul FV, non il doppio conteggio
        r = _F["mh572_riepilogo"]([_p(fv=-10.0, ca=-150.0, ch=0.0)])
        assert r["n_anomalie"] == 1
        assert any("fair value" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_nessuna_posizione_precede_anomalie(self):
        # convenzione tab566/567/568: NESSUNA_* prima di ANOMALIE_DA_VERIFICARE
        r = _F["mh572_riepilogo"](
            [_p(pid="HDG-Z", fv=-5.0, ex=0.0, no=0.0,
                pa=0.0, ca=0.0, ph=0.0, ch=0.0)])
        assert r["n_anomalie"] == 1
        assert r["verdetto"] == "NESSUNA_POSIZIONE"

    def test_voci_vuote_ko(self):
        with pytest.raises(ValueError):
            _F["mh572_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (0.0, -100.0):
            with pytest.raises(ValueError):
                _F["mh572_riepilogo"](_F["mh572_demo"](),
                                      soglia_residuo_eur=bad)


class TestW572Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE572}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 818
        assert TITLE572 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818 = st.tabs([" in src
        assert "with tab572:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st572_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
