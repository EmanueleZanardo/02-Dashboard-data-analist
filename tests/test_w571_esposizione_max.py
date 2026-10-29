"""Test tab571 "Esposizione max al rischio di credito (IFRS 7.36)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh571_num", "mh571_str", "mh571_classe", "mh571_qualita",
           "mh571_esposizione", "mh571_demo", "mh571_riepilogo")

TITLE571 = ("\U0001F6E1\uFE0F\U0001F4CA Esposizione max al rischio di credito "
            "(IFRS 7.36)")


def _e(pid="EXP-1", descrizione="classe", cl="DERIVATI_OTC",
       lo=100_000_000.0, ga=60_000_000.0, ne=10_000_000.0, qu="ALTA"):
    return _F["mh571_esposizione"](pid, descrizione, cl, lo, ga, ne, qu)


class TestW571Validatori:
    def test_num_ok(self):
        assert _F["mh571_num"](2, "x") == 2.0
        assert _F["mh571_num"](-3.5, "x") == -3.5
        assert _F["mh571_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh571_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh571_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh571_str"](bad, "x")

    def test_classe_ok(self):
        assert _F["mh571_classe"]("derivati_otc", "x") == "DERIVATI_OTC"
        assert _F["mh571_classe"]("TITOLI_DEBITO", "x") == "TITOLI_DEBITO"

    def test_classe_ko(self):
        for bad in ("XYZ", "", None, "AZIONI"):
            with pytest.raises(ValueError):
                _F["mh571_classe"](bad, "x")

    def test_qualita_ok(self):
        assert _F["mh571_qualita"]("alta", "x") == "ALTA"
        assert _F["mh571_qualita"]("NON_DICHIARATA", "x") == "NON_DICHIARATA"

    def test_qualita_ko(self):
        for bad in ("OTTIMA", "", None):
            with pytest.raises(ValueError):
                _F["mh571_qualita"](bad, "x")


class TestW571Esposizione:
    def test_hand_computed(self):
        r = _e(pid="EXP-001", cl="DERIVATI_OTC", lo=120_000_000.0,
               ga=90_000_000.0, ne=10_000_000.0, qu="ALTA")
        assert r["id"] == "EXP-001"
        assert r["classe"] == "DERIVATI_OTC"
        assert r["mitigata"] == pytest.approx(100_000_000.0)
        assert r["netta"] == pytest.approx(20_000_000.0)
        assert r["copertura_pct"] == pytest.approx(83.3333333333)
        assert r["qualita"] == "ALTA"

    def test_netta_floor_zero(self):
        # mitigazione eccedente: la voce non respinge, netta floora a 0
        r = _e(lo=100.0, ga=70.0, ne=50.0)
        assert r["netta"] == 0.0
        assert r["copertura_pct"] == pytest.approx(120.0)

    def test_copertura_none_lorda_zero(self):
        r = _e(lo=0.0, ga=0.0, ne=0.0)
        assert r["copertura_pct"] is None
        assert r["netta"] == 0.0

    def test_copertura_none_lorda_negativa(self):
        r = _e(lo=-10.0, ga=0.0, ne=0.0)
        assert r["copertura_pct"] is None


class TestW571Riepilogo:
    def test_demo_copertura_insufficiente(self):
        r = _F["mh571_riepilogo"](_F["mh571_demo"]())
        # lorda 205M, mitigata 155M -> 75,6098% < 80%
        assert r["lorda_totale"] == pytest.approx(205_000_000.0)
        assert r["mitigata_totale"] == pytest.approx(155_000_000.0)
        assert r["netta_totale"] == pytest.approx(50_000_000.0)
        assert r["copertura_media_pct"] == pytest.approx(75.6097560976)
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "COPERTURA_INSUFFICIENTE"

    def test_copertura_sopra_soglia_ok(self):
        r = _F["mh571_riepilogo"]([_e(lo=100.0, ga=85.0, ne=0.0)],
                                  soglia_copertura_pct=80.0)
        assert r["copertura_media_pct"] == pytest.approx(85.0)
        assert r["verdetto"] == "ESPOSIZIONE_SOTTO_CONTROLLO"

    def test_copertura_boundary_soglia(self):
        # copertura == soglia -> non insufficiente (<, non <=)
        r = _F["mh571_riepilogo"]([_e(lo=100.0, ga=80.0, ne=0.0)],
                                  soglia_copertura_pct=80.0)
        assert r["verdetto"] == "ESPOSIZIONE_SOTTO_CONTROLLO"

    def test_id_duplicato_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(pid="EXP-X"), _e(pid="exp-x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a
                   for a in r["analizzate"][1]["anomalie"])

    def test_lorda_negativa_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(lo=-5.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("negativa" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_classe_nulla_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(lo=0.0, ga=0.0, ne=0.0)])
        assert r["n_anomalie"] == 1
        assert any("nulla" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_garanzie_negative_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(ga=-1.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_netting_negativo_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(ne=-1.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_mitigazione_eccedente_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(lo=100.0, ga=60.0, ne=50.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("eccedente" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_qualita_non_dichiarata_anomalia(self):
        r = _F["mh571_riepilogo"]([_e(qu="NON_DICHIARATA")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("qualita'" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_qualita_non_dichiarata_senza_lorda(self):
        # lorda 0: solo "classe nulla", la 7.36(c) non scatta
        r = _F["mh571_riepilogo"](
            [_e(lo=0.0, ga=0.0, ne=0.0, qu="NON_DICHIARATA")])
        assert r["n_anomalie"] == 1
        assert any("nulla" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_nessuna_esposizione_precede_anomalie(self):
        # convenzione tab570: NESSUNA_* prima di ANOMALIE_DA_VERIFICARE
        r = _F["mh571_riepilogo"]([_e(lo=0.0, ga=0.0, ne=0.0)])
        assert r["n_anomalie"] == 1
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"

    def test_voci_vuote_ko(self):
        with pytest.raises(ValueError):
            _F["mh571_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (0.0, -100.0):
            with pytest.raises(ValueError):
                _F["mh571_riepilogo"](_F["mh571_demo"](),
                                      soglia_copertura_pct=bad)


class TestW571Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE571}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 786
        assert TITLE571 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786 = st.tabs([" in src
        assert "with tab571:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st571_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
