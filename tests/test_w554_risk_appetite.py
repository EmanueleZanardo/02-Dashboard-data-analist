"""Test tab554 'Risk appetite & limiti (IFRS 7.33-7.34)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh554_num", "mh554_str", "mh554_tipo", "mh554_voce",
           "mh554_demo", "mh554_riepilogo")

TITLE554 = "🛡️📊 Risk appetite & limiti (IFRS 7.33-7.34)"


def _v(vid="R-1", d="x", ti="RISCHIO_MERCATO", es=8000000.0, li=10000000.0,
       ap="appetito", mo="monitoraggio", co=True):
    return {"id": vid, "descrizione": d, "tipo": ti, "esposizione": es,
            "limite": li, "appetito": ap, "monitoraggio": mo,
            "coperture_attive": co}


class TestW554Validatori:
    def test_num_ok(self):
        assert _F["mh554_num"](2, "x") == 2.0
        assert _F["mh554_num"](0, "x") == 0.0
        assert _F["mh554_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh554_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh554_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh554_str"](bad, "x")

    def test_tipo_ok_ko(self):
        for ok in ("RISCHIO_MERCATO", "RISCHIO_CREDITO",
                   "RISCHIO_LIQUIDITA", "RISCHIO_OPERATIVO",
                   "RISCHIO_CONFORMITA"):
            assert _F["mh554_tipo"](ok) == ok
        for bad in ("MERCATO", "", None, 3, True):
            with pytest.raises(ValueError):
                _F["mh554_tipo"](bad)


class TestW554Voce:
    def test_voce_ok(self):
        o = _F["mh554_voce"](_v())
        assert o["utilizzo"] == pytest.approx(0.8)
        assert o["sforamento"] is False
        assert o["anomalie"] == []

    def test_utilizzo_none_senza_limite(self):
        o = _F["mh554_voce"](_v(es=100.0, li=0.0))
        assert o["utilizzo"] is None
        assert o["sforamento"] is False

    def test_sforamento(self):
        o = _F["mh554_voce"](_v(es=12000000.0, li=10000000.0))
        assert o["sforamento"] is True
        assert o["utilizzo"] == pytest.approx(1.2)

    def test_anomalia_senza_limite(self):
        o = _F["mh554_voce"](_v(es=500000.0, li=0.0))
        assert len(o["anomalie"]) == 1
        assert "limite" in o["anomalie"][0].lower()

    def test_anomalia_monitoraggio_mancante(self):
        o = _F["mh554_voce"](_v(mo=None))
        assert len(o["anomalie"]) == 1
        assert "monitoraggio" in o["anomalie"][0].lower()

    def test_anomalia_appetito_mancante(self):
        o = _F["mh554_voce"](_v(ap=None))
        assert len(o["anomalie"]) == 1
        assert "appetite" in o["anomalie"][0].lower()

    def test_voce_ko_struttura(self):
        with pytest.raises(ValueError):
            _F["mh554_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh554_voce"]({"id": "x"})
        with pytest.raises(ValueError):
            _F["mh554_voce"](_v(es=-1))
        with pytest.raises(ValueError):
            _F["mh554_voce"](_v(co="si"))
        with pytest.raises(ValueError):
            _F["mh554_voce"](_v(ti="RISCHIO_X"))


class TestW554Riepilogo:
    def test_demo_verdetto(self):
        r = _F["mh554_riepilogo"](_F["mh554_demo"]())
        assert r["verdetto"] == "LIMITI_SFORATI"
        assert r["n_sforamenti"] == 1
        assert r["esposizione_tot"] == pytest.approx(26800000.0)
        assert r["utilizzo_max"] == pytest.approx(1.24)
        assert r["n_anomalie"] == 0

    def test_verdetto_rispettato(self):
        r = _F["mh554_riepilogo"]([_v(es=5000000.0, li=10000000.0)])
        assert r["verdetto"] == "RISK_APPETITE_RISPETTATO"

    def test_verdetto_tesi(self):
        r = _F["mh554_riepilogo"]([_v(es=9200000.0, li=10000000.0)])
        assert r["verdetto"] == "LIMITI_TESI"

    def test_verdetto_monitorati(self):
        r = _F["mh554_riepilogo"]([_v(es=8000000.0, li=10000000.0)])
        assert r["verdetto"] == "LIMITI_MONITORATI"

    def test_verdetto_soglie_custom(self):
        r = _F["mh554_riepilogo"]([_v(es=8000000.0, li=10000000.0)],
                                  0.70, 0.60)
        assert r["verdetto"] == "LIMITI_TESI"

    def test_verdetto_nessun_rischio(self):
        r = _F["mh554_riepilogo"]([_v(es=0.0, li=10000000.0)])
        assert r["verdetto"] == "NESSUN_RISCHIO"

    def test_verdetto_anomalie(self):
        r = _F["mh554_riepilogo"]([_v(es=100000.0, li=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] >= 1

    def test_per_tipo(self):
        r = _F["mh554_riepilogo"](
            [_v(ti="RISCHIO_MERCATO"), _v(vid="R-2",
                                          ti="RISCHIO_CREDITO")])
        assert r["per_tipo"]["RISCHIO_MERCATO"]["n"] == 1
        assert r["per_tipo"]["RISCHIO_CREDITO"]["n"] == 1
        assert r["per_tipo"]["RISCHIO_MERCATO"]["esposizione"] == \
            pytest.approx(8000000.0)

    def test_riepilogo_ko(self):
        for bad in ([], "x", None):
            with pytest.raises(ValueError):
                _F["mh554_riepilogo"](bad)
        for st_, sv_ in ((0.0, 0.75), (1.5, 0.75), (-0.1, 0.75),
                         (0.75, 0.75), (0.60, 0.75), ("0.9", 0.75),
                         (True, 0.75), (math.nan, 0.75)):
            with pytest.raises(ValueError):
                _F["mh554_riepilogo"]([_v()], st_, sv_)


class TestW554Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_554_presente(self):
        assert self._src().count(TITLE554) == 3

    def test_counts_554(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 702
        assert TITLE554 in titoli
        assert "tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702 = st.tabs([" in src

    def test_chiavi_554_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st554_" in ln]
        # le f-string st554_id_{_i554} generano istanze a runtime: la base
        # e' fino al suffisso numerico; run/csv1/csv2 sono chiavi distinte
        basi = []
        for ln in righe:
            basi.append(re.search(r"st554_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 14
