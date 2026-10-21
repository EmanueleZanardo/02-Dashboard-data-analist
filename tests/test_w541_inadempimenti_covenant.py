"""Test tab541 '⚠️💰 Inadempimenti e violazioni covenant (IFRS 7.18-19)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh541_num", "mh541_str", "mh541_bool", "mh541_int0",
           "mh541_voce", "mh541_demo", "mh541_riepilogo")

TITLE541 = "⚠️💰 Inadempimenti e violazioni covenant (IFRS 7.18-19)"


def _v(vid="V-1", d="x", vc=100000.0, df=False, gg=0, vcov=False,
       rim=False, wai=False):
    return {"id": vid, "descrizione": d, "valore_contabile": vc,
            "in_default": df, "giorni_inadempimento": gg,
            "violazione_covenant": vcov, "covenant_rimossa": rim,
            "waiver_ottenuto": wai}


class TestW541Validatori:
    def test_num_ok(self):
        assert _F["mh541_num"](2, "x") == 2.0
        assert _F["mh541_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh541_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh541_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh541_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh541_bool"](True, "x") is True
        assert _F["mh541_bool"](False, "x") is False
        for bad in (1, 0, "sì", None, 1.0):
            with pytest.raises(ValueError):
                _F["mh541_bool"](bad, "x")

    def test_int0_ok_ko(self):
        assert _F["mh541_int0"](0, "x") == 0
        assert _F["mh541_int0"](45, "x") == 45
        for bad in (-1, 1.5, True, "3", None):
            with pytest.raises(ValueError):
                _F["mh541_int0"](bad, "x")


class TestW541Voce:
    def test_no_inadempienza(self):
        o = _F["mh541_voce"](_v())
        assert o["esito"] == "NO_INADEMPIENZA"
        assert o["anomalie"] == []

    def test_inadempienza_in_corso(self):
        o = _F["mh541_voce"](_v(df=True, gg=45))
        assert o["esito"] == "INADEMPIENZA_IN_CORSO"
        assert "7.18" in o["nota"]
        assert o["anomalie"] == []

    def test_giorni_senza_flag(self):
        o = _F["mh541_voce"](_v(gg=10))
        assert o["esito"] == "INADEMPIENZA_IN_CORSO"
        assert len(o["anomalie"]) == 1

    def test_default_senza_giorni(self):
        o = _F["mh541_voce"](_v(df=True))
        assert o["esito"] == "INADEMPIENZA_IN_CORSO"
        assert len(o["anomalie"]) == 1

    def test_violazione_rimediata(self):
        o = _F["mh541_voce"](_v(vcov=True, rim=True))
        assert o["esito"] == "VIOLAZIONE_RIMEDIATA"
        assert "7.19" in o["nota"]

    def test_violazione_con_waiver(self):
        o = _F["mh541_voce"](_v(vcov=True, wai=True))
        assert o["esito"] == "VIOLAZIONE_RIMEDIATA"

    def test_violazione_non_rimediata(self):
        o = _F["mh541_voce"](_v(vcov=True))
        assert o["esito"] == "VIOLAZIONE_NON_RIMEDIATA"
        assert "1.74" in o["nota"]

    def test_default_vince_su_violazione(self):
        o = _F["mh541_voce"](_v(df=True, gg=5, vcov=True))
        assert o["esito"] == "INADEMPIENZA_IN_CORSO"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh541_voce"]("x")
        with pytest.raises(ValueError):
            _F["mh541_voce"]({"id": "A"})
        for bad in (_v(vc=0.0), _v(vc=-5), _v(vc=math.nan),
                    _v(vc=True), _v(df="si"), _v(gg=-1),
                    _v(gg=1.5), _v(vid="  "), _v(d=None)):
            with pytest.raises(ValueError):
                _F["mh541_voce"](bad)


class TestW541Riepilogo:
    def test_demo_verdetto_inadempienze(self):
        _an = [_F["mh541_voce"](p) for p in _F["mh541_demo"]()]
        assert len(_an) == 3
        assert [_o["esito"] for _o in _an] == [
            "VIOLAZIONE_RIMEDIATA", "INADEMPIENZA_IN_CORSO",
            "NO_INADEMPIENZA"]
        _ri = _F["mh541_riepilogo"](_an)
        assert _ri["verdetto"] == "INADEMPIENZE_IN_CORSO"
        assert _ri["n_anomalie"] == 0
        assert _ri["vc_totale"] == pytest.approx(15300000.0)
        assert _ri["n_inadempienze"] == 1
        assert _ri["n_violazioni_non_rimediate"] == 0
        assert _ri["esposizione_riclassifica_corrente"] == pytest.approx(
            0.0)

    def test_verdetto_violazioni_da_rimedio(self):
        _an = [_F["mh541_voce"](_v("A", "a", 100.0, vcov=True)),
               _F["mh541_voce"](_v("B", "b", 50.0))]
        _ri = _F["mh541_riepilogo"](_an)
        assert _ri["verdetto"] == "VIOLAZIONI_DA_RIMEDIO"
        assert _ri["esposizione_riclassifica_corrente"] == pytest.approx(
            100.0)

    def test_verdetto_tutte_rimediate(self):
        _an = [_F["mh541_voce"](_v("A", "a", 100.0, vcov=True, rim=True)),
               _F["mh541_voce"](_v("B", "b", 50.0))]
        _ri = _F["mh541_riepilogo"](_an)
        assert _ri["verdetto"] == "TUTTE_RIMEDIATE"

    def test_verdetto_nessuna_criticita(self):
        _an = [_F["mh541_voce"](_v("A", "a", 100.0))]
        _ri = _F["mh541_riepilogo"](_an)
        assert _ri["verdetto"] == "NESSUNA_CRITICITA"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh541_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh541_riepilogo"]("x")
        with pytest.raises(ValueError):
            _F["mh541_riepilogo"]([_F["mh541_voce"](_v())] * 5)
        with pytest.raises(ValueError):
            _F["mh541_riepilogo"](["x"])
        with pytest.raises(ValueError):
            _F["mh541_riepilogo"]([{"id": "A"}])


class TestW541Registry:
    def test_titolo_541_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE541) == 3

    def test_registry_tab_count_541(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 605
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 605

    def test_tab541_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605 = st.tabs([" in src
        assert "with tab541:" in src

    def test_chiavi_st541_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st541_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
