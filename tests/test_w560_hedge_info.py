"""Test tab560 'Informativa sull'hedge accounting (IFRS 7.24A-24F)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh560_num", "mh560_str", "mh560_ge0", "mh560_tipo",
           "mh560_rischio", "mh560_relazione", "mh560_demo",
           "mh560_riepilogo")

TITLE560 = "\U0001F9FE\U0001F4DD Informativa sull'hedge accounting (IFRS 7.24A-24F)"


def _r(rid="H-1", tp="CASH_FLOW", rs="GAS", st="Swap",
       no=1000000.0, vc=0.0, df=1000.0, di=-900.0, oc=0.0, rp=0.0):
    return _F["mh560_relazione"](rid, tp, rs, st, no, vc, df, di, oc, rp)


class TestW560Validatori:
    def test_num_ok(self):
        assert _F["mh560_num"](2, "x") == 2.0
        assert _F["mh560_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh560_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh560_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh560_str"](bad, "x")

    def test_ge0_ok_ko(self):
        assert _F["mh560_ge0"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh560_ge0"](-0.01, "x")

    def test_tipo_ok(self):
        assert _F["mh560_tipo"]("cash_flow") == "CASH_FLOW"
        assert _F["mh560_tipo"]("FAIR_VALUE") == "FAIR_VALUE"
        assert _F["mh560_tipo"]("net_investment") == "NET_INVESTMENT"

    def test_tipo_ko(self):
        for bad in (None, "", "HEDGE"):
            with pytest.raises(ValueError):
                _F["mh560_tipo"](bad)

    def test_rischio_ok_ko(self):
        assert _F["mh560_rischio"]("power") == "POWER"
        with pytest.raises(ValueError):
            _F["mh560_rischio"]("OIL")


class TestW560Relazione:
    def test_ok_hr001(self):
        r = _F["mh560_relazione"](
            "HR-001", "CASH_FLOW", "GAS", "Swap TTF Cal-27",
            42000000.0, 3200000.0, 1850000.0, -1790000.0,
            1790000.0, 220000.0)
        assert r["inefficacia"] == pytest.approx(60000.0)
        assert r["rapporto_inefficacia"] == pytest.approx(
            60000.0 / 1850000.0)
        assert r["esito"] == "INEFFICACIA_CONTENUTA"
        assert r["nozionale"] == 42000000.0

    def test_significativa(self):
        r = _r(df=1000.0, di=-500.0)
        assert r["inefficacia"] == pytest.approx(500.0)
        assert r["rapporto_inefficacia"] == pytest.approx(0.5)
        assert r["esito"] == "INEFFICACIA_SIGNIFICATIVA"

    def test_nessuna_variazione(self):
        r = _r(df=0.0, di=0.0)
        assert r["inefficacia"] == pytest.approx(0.0)
        assert r["rapporto_inefficacia"] == pytest.approx(0.0)
        assert r["esito"] == "NESSUNA_VARIAZIONE"

    def test_segni_opposti_si_compensano(self):
        r = _r(df=-960000.0, di=900000.0)
        assert r["inefficacia"] == pytest.approx(-60000.0)

    def test_ko(self):
        with pytest.raises(ValueError):
            _r(rid="  ")
        with pytest.raises(ValueError):
            _r(tp="BOH")
        with pytest.raises(ValueError):
            _r(rs="OIL")
        with pytest.raises(ValueError):
            _r(st="")
        with pytest.raises(ValueError):
            _r(no=-1.0)


class TestW560Riepilogo:
    def test_demo(self):
        d = _F["mh560_demo"]()
        assert len(d) == 3
        r = _F["mh560_riepilogo"](d)
        assert r["n_relazioni"] == 3
        assert r["n_anomalie"] == 0
        assert r["nozionale_totale"] == pytest.approx(85000000.0)
        assert r["inefficacia_totale"] == pytest.approx(-25000.0)
        assert r["inefficacia_ass_totale"] == pytest.approx(145000.0)
        assert r["quota_inefficacia"] == pytest.approx(
            145000.0 / 85000000.0)
        assert r["verdetto"] == "INFORMATIVA_ADEGUATA"
        assert r["per_tipo"] == {"CASH_FLOW": 2, "FAIR_VALUE": 1,
                                 "NET_INVESTMENT": 0}
        assert len(r["analizzate"]) == 3

    def test_id_duplicato(self):
        r = _F["mh560_riepilogo"]([_r("DUP"), _r("dup")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a.lower()
                   for a in r["analizzate"][1]["anomalie"])

    def test_nozionale_nullo(self):
        r = _F["mh560_riepilogo"]([_r(no=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nozionale" in a.lower()
                   for a in r["analizzate"][0]["anomalie"])

    def test_variazioni_nulle(self):
        r = _F["mh560_riepilogo"]([_r(df=0.0, di=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["analizzate"][0]["esito"] == "NESSUNA_VARIAZIONE"

    def test_stesso_segno(self):
        r = _F["mh560_riepilogo"]([_r(df=1000.0, di=500.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("non compensative" in a
                   for a in r["analizzate"][0]["anomalie"])

    def test_inefficacia_significativa(self):
        r = _F["mh560_riepilogo"]([_r(no=1000000.0, df=500000.0,
                                      di=0.0)])
        assert r["quota_inefficacia"] == pytest.approx(0.5)
        assert r["verdetto"] == "INEFFICACIA_SIGNIFICATIVA"

    def test_vuota(self):
        r = _F["mh560_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_RELAZIONE"
        assert r["n_relazioni"] == 0
        assert r["n_anomalie"] == 0


class TestW560Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_560_presente(self):
        assert self._src().count(TITLE560) == 3

    def test_counts_560(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 627
        assert TITLE560 in titoli
        assert "tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627 = st.tabs([" in src

    def test_chiavi_560_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st560_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st560_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
