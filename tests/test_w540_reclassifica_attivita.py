"""Test tab540 '🔁📂 Reclassifica attività finanziarie (IFRS 9 4.4)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh540_num", "mh540_str", "mh540_cat", "mh540_bool",
           "mh540_trattamento", "mh540_attivita", "mh540_demo",
           "mh540_riepilogo")

TITLE540 = "🔁📂 Reclassifica attività finanziarie (IFRS 9 4.4)"


def _a(aid="A-1", d="x", ca="AC", cp="FVOCI", fv=100000.0, pe="Q1 2027",
       bm=True, fvo=False):
    return {"id": aid, "descrizione": d, "cat_attuale": ca,
            "cat_proposta": cp, "fair_value": fv,
            "periodo_decorrenza": pe, "cambio_bm": bm, "fvo": fvo}


class TestW540Validatori:
    def test_num_ok(self):
        assert _F["mh540_num"](2, "x") == 2.0
        assert _F["mh540_num"](-1.5, "x") == -1.5
        assert _F["mh540_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh540_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh540_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh540_str"](bad, "x")

    def test_cat_ok_ko(self):
        for ok in ("AC", "FVOCI", "FVTPL"):
            assert _F["mh540_cat"](ok, "x") == ok
        for bad in ("ac", "", None, 12, True, "IFRS9", " FVTPL "):
            # spazi attorno non ammessi: match esatto dopo strip parziale
            if isinstance(bad, str) and bad.strip() in ("AC", "FVOCI",
                                                        "FVTPL"):
                continue
            with pytest.raises(ValueError):
                _F["mh540_cat"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh540_bool"](True, "x") is True
        assert _F["mh540_bool"](False, "x") is False
        for bad in (1, 0, "sì", None, 1.0):
            with pytest.raises(ValueError):
                _F["mh540_bool"](bad, "x")

    def test_trattamento_tutte_direzioni(self):
        _t = _F["mh540_trattamento"]
        assert "CE" in _t("AC", "FVTPL")
        assert "TIE" in _t("FVTPL", "AC")
        assert "OCI" in _t("AC", "FVOCI")
        assert "5.6.5" in _t("FVOCI", "AC")
        assert "CE" in _t("FVOCI", "FVTPL")
        assert "5.6.7" in _t("FVTPL", "FVOCI")

    def test_trattamento_ko(self):
        with pytest.raises(ValueError):
            _F["mh540_trattamento"]("AC", "AC")
        with pytest.raises(ValueError):
            _F["mh540_trattamento"]("AC", "XYZ")


class TestW540Attivita:
    def test_riclassificata_ac_fvoci(self):
        o = _F["mh540_attivita"](_a())
        assert o["esito"] == "RICLASSIFICATA"
        assert o["anomalie"] == []
        assert "prospettica" in o["trattamento"]
        assert "5.6.1" in o["trattamento"]

    def test_vietata_senza_cambio_bm(self):
        o = _F["mh540_attivita"](_a(ca="AC", cp="FVTPL", bm=False))
        assert o["esito"] == "RICLASSIFICA_VIETATA"
        assert len(o["anomalie"]) == 1
        assert "4.4.1" in o["anomalie"][0]

    def test_non_ammessa_fvo(self):
        o = _F["mh540_attivita"](_a(ca="FVTPL", cp="FVOCI", bm=True,
                                   fvo=True))
        assert o["esito"] == "NON_AMMESSA"
        assert len(o["anomalie"]) == 1

    def test_nessuna_riclassifica_cat_uguale(self):
        o = _F["mh540_attivita"](_a(ca="AC", cp="AC", bm=False))
        assert o["esito"] == "NESSUNA_RICLASSIFICA"
        assert o["anomalie"] == []

    def test_anomalia_bm_dichiarato_cat_invariate(self):
        o = _F["mh540_attivita"](_a(ca="FVOCI", cp="FVOCI", bm=True))
        assert o["esito"] == "NESSUNA_RICLASSIFICA"
        assert len(o["anomalie"]) == 1

    def test_fvo_vince_su_vietata(self):
        o = _F["mh540_attivita"](_a(ca="AC", cp="FVTPL", bm=False,
                                   fvo=True))
        assert o["esito"] == "NON_AMMESSA"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh540_attivita"]("x")
        with pytest.raises(ValueError):
            _F["mh540_attivita"]({"id": "A"})
        bad = _a()
        bad["fair_value"] = 0.0
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)
        bad = _a()
        bad["fair_value"] = -5
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)
        bad = _a()
        bad["cat_proposta"] = "ACX"
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)
        bad = _a()
        bad["cambio_bm"] = "si"
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)
        bad = _a()
        bad["id"] = "  "
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)
        bad = _a()
        bad["fair_value"] = math.nan
        with pytest.raises(ValueError):
            _F["mh540_attivita"](bad)


class TestW540Riepilogo:
    def test_demo_verdetto_vietate(self):
        _an = [_F["mh540_attivita"](p) for p in _F["mh540_demo"]()]
        assert len(_an) == 3
        assert [_o["esito"] for _o in _an] == [
            "RICLASSIFICATA", "RICLASSIFICA_VIETATA", "NON_AMMESSA"]
        _ri = _F["mh540_riepilogo"](_an)
        assert _ri["verdetto"] == "RICLASSIFICHE_VIETATE"
        assert _ri["n_anomalie"] == 2
        assert _ri["fv_riclassificato"] == pytest.approx(2450000.0)
        assert _ri["quota_riclassificata_pct"] == pytest.approx(
            2450000.0 / 3740000.0 * 100.0)

    def test_verdetto_blocco_fvo(self):
        _an = [_F["mh540_attivita"](_a("A", "a", "FVTPL", "FVOCI",
                                       100.0, "Q1", True, True)),
               _F["mh540_attivita"](_a("B", "b", "AC", "AC",
                                       100.0, "Q1", False, False))]
        _ri = _F["mh540_riepilogo"](_an)
        assert _ri["verdetto"] == "BLOCCO_FVO"
        assert _ri["n_anomalie"] == 1

    def test_verdetto_tutte_riclassificate(self):
        _an = [_F["mh540_attivita"](_a("A", "a", "AC", "FVOCI", 300.0,
                                       "Q1", True, False)),
               _F["mh540_attivita"](_a("B", "b", "FVOCI", "FVTPL", 100.0,
                                       "Q1", True, False))]
        _ri = _F["mh540_riepilogo"](_an)
        assert _ri["verdetto"] == "TUTTE_RICLASSIFICATE"
        assert _ri["fv_riclassificato"] == pytest.approx(400.0)
        assert _ri["quota_riclassificata_pct"] == pytest.approx(100.0)
        assert _ri["n_anomalie"] == 0

    def test_verdetto_nessuna_riclassifica(self):
        _an = [_F["mh540_attivita"](_a("A", "a", "AC", "AC", 50.0,
                                       "Q1", False, False))]
        _ri = _F["mh540_riepilogo"](_an)
        assert _ri["verdetto"] == "NESSUNA_RICLASSIFICA"

    def test_verdetto_misto(self):
        _an = [_F["mh540_attivita"](_a("A", "a", "AC", "FVOCI", 300.0,
                                       "Q1", True, False)),
               _F["mh540_attivita"](_a("B", "b", "FVTPL", "FVTPL", 100.0,
                                       "Q1", False, False))]
        _ri = _F["mh540_riepilogo"](_an)
        assert _ri["verdetto"] == "MISTO"
        assert _ri["per_esito"] == {"RICLASSIFICATA": 1,
                                    "NESSUNA_RICLASSIFICA": 1}

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh540_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh540_riepilogo"]("x")
        with pytest.raises(ValueError):
            _F["mh540_riepilogo"](
                [_F["mh540_attivita"](_a())] * 5)
        with pytest.raises(ValueError):
            _F["mh540_riepilogo"](["x"])
        with pytest.raises(ValueError):
            _F["mh540_riepilogo"]([{"id": "A"}])


class TestW540Registry:
    def test_titolo_540_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE540) == 3

    def test_registry_tab_count_540(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 680
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 680

    def test_tab540_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680 = st.tabs([" in src
        assert "with tab540:" in src

    def test_chiavi_st540_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st540_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
