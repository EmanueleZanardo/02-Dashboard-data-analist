"""Test tab542 '⚖️📑 Compensazione attività/passività finanziarie (IFRS 7.13A-13F)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh542_num", "mh542_str", "mh542_bool",
           "mh542_voce", "mh542_demo", "mh542_riepilogo")

TITLE542 = "⚖️📑 Compensazione attività/passività finanziarie (IFRS 7.13A-13F)"


def _v(vid="V-1", d="x", cp="CPTY", al=1000.0, pl=400.0, ca=0.0, cp2=0.0,
       dl=False, inn=False, sn=0.0, cc=0.0):
    return {"id": vid, "descrizione": d, "controparte": cp,
            "attivo_lordo": al, "passivo_lordo": pl,
            "comp_attivo": ca, "comp_passivo": cp2,
            "diritto_legale": dl, "intenzione_netto": inn,
            "strumenti_netting": sn, "collateral_cash": cc}


class TestW542Validatori:
    def test_num_ok(self):
        assert _F["mh542_num"](2, "x") == 2.0
        assert _F["mh542_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh542_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh542_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh542_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh542_bool"](True, "x") is True
        assert _F["mh542_bool"](False, "x") is False
        for bad in (1, 0, "sì", None, 1.0):
            with pytest.raises(ValueError):
                _F["mh542_bool"](bad, "x")


class TestW542Voce:
    def test_nessuna_compensazione(self):
        o = _F["mh542_voce"](_v())
        assert o["esito"] == "NESSUNA_COMPENSAZIONE"
        assert o["attivo_netto"] == pytest.approx(1000.0)
        assert o["passivo_netto"] == pytest.approx(400.0)
        assert o["esposizione_residua"] == pytest.approx(1000.0)
        assert o["anomalie"] == []

    def test_compensata(self):
        o = _F["mh542_voce"](_v(ca=400.0, cp2=400.0, dl=True, inn=True,
                               sn=100.0, cc=50.0))
        assert o["esito"] == "COMPENSATA"
        assert o["compensazione_ammessa"] is True
        assert o["attivo_netto"] == pytest.approx(600.0)
        assert o["passivo_netto"] == pytest.approx(0.0)
        assert o["esposizione_residua"] == pytest.approx(450.0)
        assert o["anomalie"] == []

    def test_solo_informativa(self):
        o = _F["mh542_voce"](_v(dl=True, inn=False, sn=400.0, cc=100.0))
        assert o["esito"] == "SOLO_INFORMATIVA"
        assert o["attivo_netto"] == pytest.approx(1000.0)
        assert o["esposizione_residua"] == pytest.approx(500.0)
        assert o["anomalie"] == []

    def test_compensazione_non_ammessa(self):
        o = _F["mh542_voce"](_v(ca=400.0, cp2=400.0, dl=True, inn=False))
        assert o["esito"] == "COMPENSAZIONE_NON_AMMESSA"
        assert o["compensazione_ammessa"] is False
        assert o["attivo_netto"] == pytest.approx(1000.0)
        assert len(o["anomalie"]) == 1
        assert "32.42" in o["anomalie"][0]

    def test_garanzie_eccedono(self):
        o = _F["mh542_voce"](_v(sn=900.0, cc=200.0))
        assert o["esito"] == "SOLO_INFORMATIVA"
        assert o["esposizione_residua"] == pytest.approx(-100.0)
        assert len(o["anomalie"]) == 1

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh542_voce"]("x")
        with pytest.raises(ValueError):
            _F["mh542_voce"]({k: 0 for k in ()} | {"id": "A"})
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(al=-1.0))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(pl=-5.0))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(ca=1000.01))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(cp2=400.01))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(sn=-1.0))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(cc=-1.0))
        with pytest.raises(ValueError):
            _F["mh542_voce"](_v(dl=1))


class TestW542Demo:
    def test_demo_esiti(self):
        righe = [_F["mh542_voce"](d) for d in _F["mh542_demo"]()]
        assert [r["esito"] for r in righe] == [
            "COMPENSATA", "SOLO_INFORMATIVA", "NESSUNA_COMPENSAZIONE"]
        assert righe[0]["esposizione_residua"] == pytest.approx(
            1500000.0)
        assert righe[1]["esposizione_residua"] == pytest.approx(300000.0)
        assert righe[2]["esposizione_residua"] == pytest.approx(
            1200000.0)


class TestW542Riepilogo:
    def _demo(self):
        return [_F["mh542_voce"](d) for d in _F["mh542_demo"]()]

    def test_totali_demo(self):
        ri = _F["mh542_riepilogo"](self._demo())
        assert ri["n"] == 3
        assert ri["attivo_lordo"] == pytest.approx(12700000.0)
        assert ri["comp_attivo"] == pytest.approx(6200000.0)
        assert ri["attivo_netto"] == pytest.approx(6500000.0)
        assert ri["passivo_netto"] == pytest.approx(2900000.0)
        assert ri["esposizione_residua"] == pytest.approx(3000000.0)
        assert ri["quota_compensata_pct"] == pytest.approx(
            6200000.0 / 12700000.0 * 100.0)
        assert ri["n_anomalie"] == 0

    def test_verdetto_compensazione_parziale(self):
        ri = _F["mh542_riepilogo"](self._demo())
        assert ri["verdetto"] == "COMPENSAZIONE_PARZIALE"

    def test_verdetto_netting_significativo(self):
        righe = [_F["mh542_voce"](_v("A", "a", "C", 100.0, 60.0, 60.0,
                                     60.0, True, True))]
        ri = _F["mh542_riepilogo"](righe)
        assert ri["verdetto"] == "NETTING_SIGNIFICATIVO"

    def test_verdetto_da_verificare(self):
        righe = [_F["mh542_voce"](_v("A", "a", "C", 100.0, 60.0, 60.0,
                                     60.0, True, False))]
        ri = _F["mh542_riepilogo"](righe)
        assert ri["verdetto"] == "COMPENSAZIONI_DA_VERIFICARE"

    def test_verdetto_solo_informativa(self):
        righe = [_F["mh542_voce"](_v("A", "a", "C", sn=10.0))]
        ri = _F["mh542_riepilogo"](righe)
        assert ri["verdetto"] == "SOLO_INFORMATIVA_NETTING"

    def test_verdetto_nessuna(self):
        righe = [_F["mh542_voce"](_v("A", "a", "C"))]
        ri = _F["mh542_riepilogo"](righe)
        assert ri["verdetto"] == "NESSUNA_COMPENSAZIONE"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh542_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh542_riepilogo"]("x")
        with pytest.raises(ValueError):
            _F["mh542_riepilogo"]([_F["mh542_voce"](_v())] * 5)
        with pytest.raises(ValueError):
            _F["mh542_riepilogo"](["x"])
        with pytest.raises(ValueError):
            _F["mh542_riepilogo"]([{"id": "A"}])


class TestW542Registry:
    def test_titolo_542_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE542) == 3

    def test_registry_tab_count_542(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 689
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 689

    def test_tab542_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689 = st.tabs([" in src
        assert "with tab542:" in src

    def test_chiavi_st542_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st542_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
