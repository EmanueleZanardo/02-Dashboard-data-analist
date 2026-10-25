"""Test tab547 'Crediti scaduti non deteriorati (IFRS 7.37)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh547_num", "mh547_str", "mh547_classe", "mh547_bucket",
           "mh547_riga", "mh547_demo", "mh547_riepilogo")

TITLE547 = "⏰📉 Crediti scaduti non deteriorati (IFRS 7.37)"


def _r(rid="R-1", d="x", cl="CREDITI_COMMERCIALI", imp=1000.0, gg=0.0):
    return {"id": rid, "descrizione": d, "classe": cl, "importo": imp,
            "giorni": gg}


class TestW547Validatori:
    def test_num_ok(self):
        assert _F["mh547_num"](2, "x") == 2.0
        assert _F["mh547_num"](0, "x") == 0.0
        assert _F["mh547_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh547_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh547_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh547_str"](bad, "x")

    def test_classe_ok_ko(self):
        for ok in ("CREDITI_COMMERCIALI", "CREDITI_PPA",
                   "MARGINI_TRADING", "ALTRE_ATTIVITA"):
            assert _F["mh547_classe"](ok, "x") == ok
        for bad in ("CREDITI", "crediti_ppa", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh547_classe"](bad, "x")


class TestW547Bucket:
    def test_bucket_boundary(self):
        casi = [(0, "NON_SCADUTO"), (1, "SCADUTO_1_30"),
                (30, "SCADUTO_1_30"), (31, "SCADUTO_31_60"),
                (60, "SCADUTO_31_60"), (61, "SCADUTO_61_90"),
                (90, "SCADUTO_61_90"), (91, "SCADUTO_OLTRE_90"),
                (400, "SCADUTO_OLTRE_90")]
        for gg, atteso in casi:
            assert _F["mh547_bucket"](gg) == atteso

    def test_bucket_ko(self):
        for bad in (-1, "x", None, True, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh547_bucket"](bad)


class TestW547Riga:
    def test_bucket_calcolo(self):
        o = _F["mh547_riga"](_r(gg=45.0))
        assert o["bucket"] == "SCADUTO_31_60"
        assert o["anomalie"] == []

    def test_non_scaduto_ok(self):
        o = _F["mh547_riga"](_r(gg=0.0))
        assert o["bucket"] == "NON_SCADUTO"
        assert o["anomalie"] == []

    def test_anomalia_oltre_90(self):
        o = _F["mh547_riga"](_r(gg=120.0))
        assert o["bucket"] == "SCADUTO_OLTRE_90"
        assert any("oltre 90 gg" in a for a in o["anomalie"])

    def test_anomalia_oltre_365(self):
        o = _F["mh547_riga"](_r(gg=400.0))
        assert any("365 gg" in a for a in o["anomalie"])
        assert not any("oltre 90 gg" in a for a in o["anomalie"])

    def test_anomalia_margine_scaduto(self):
        o = _F["mh547_riga"](_r(cl="MARGINI_TRADING", gg=5.0))
        assert any("margine di trading" in a for a in o["anomalie"])

    def test_margine_non_scaduto_ok(self):
        o = _F["mh547_riga"](_r(cl="MARGINI_TRADING", gg=0.0))
        assert o["anomalie"] == []

    def test_riga_ko(self):
        with pytest.raises(ValueError):
            _F["mh547_riga"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh547_riga"](_r(imp=-1.0))
        with pytest.raises(ValueError):
            _F["mh547_riga"](_r(gg=-5.0))
        with pytest.raises(ValueError):
            _F["mh547_riga"](_r(gg="x"))
        with pytest.raises(ValueError):
            _F["mh547_riga"](_r(cl="CREDITI"))
        with pytest.raises(ValueError):
            _F["mh547_riga"](_r(rid=""))


class TestW547Demo:
    def test_demo_verdetto(self):
        demo = _F["mh547_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["PPA-IT-001", "COMM-DE-002",
                                          "RATEI-UK-003"]
        ri = _F["mh547_riepilogo"](demo)
        assert ri["totale"] == pytest.approx(10100000.0)
        assert ri["scaduto_tot"] == pytest.approx(1600000.0)
        assert ri["quota_scaduta"] == pytest.approx(1600000.0 / 10100000.0)
        assert ri["verdetto"] == "SCADUTO_TESO"
        assert ri["n_anomalie"] == 0
        assert ri["per_bucket"]["NON_SCADUTO"]["importo"] == pytest.approx(
            8500000.0)
        assert ri["per_bucket"]["SCADUTO_31_60"]["importo"] == pytest.approx(
            1200000.0)
        assert ri["per_bucket"]["SCADUTO_1_30"]["importo"] == pytest.approx(
            400000.0)


class TestW547Riepilogo:
    def test_verdetto_critico(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=1000.0, gg=0.0),
                                    _r(rid="B", imp=500.0, gg=45.0)])
        assert ri["quota_scaduta"] == pytest.approx(1.0 / 3.0)
        assert ri["verdetto"] == "SCADUTO_CRITICO"

    def test_verdetto_critico_boundary(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=750.0, gg=0.0),
                                    _r(rid="B", imp=250.0, gg=45.0)])
        assert ri["verdetto"] == "SCADUTO_TESO"
        ri2 = _F["mh547_riepilogo"]([_r(rid="A", imp=749.99, gg=0.0),
                                     _r(rid="B", imp=250.01, gg=45.0)])
        assert ri2["verdetto"] == "SCADUTO_CRITICO"

    def test_verdetto_teso_boundary(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=900.0, gg=0.0),
                                    _r(rid="B", imp=100.0, gg=45.0)])
        assert ri["verdetto"] == "PORTAFOGLIO_SANO"
        ri2 = _F["mh547_riepilogo"]([_r(rid="A", imp=899.99, gg=0.0),
                                     _r(rid="B", imp=100.01, gg=45.0)])
        assert ri2["verdetto"] == "SCADUTO_TESO"

    def test_verdetto_sano(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=1000.0, gg=0.0)])
        assert ri["verdetto"] == "PORTAFOGLIO_SANO"
        assert ri["quota_scaduta"] == pytest.approx(0.0)

    def test_nessun_credito(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=0.0, gg=0.0)])
        assert ri["verdetto"] == "NESSUN_CREDITO"

    def test_anomalie_da_verificare(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", imp=100.0, gg=120.0)])
        assert ri["n_anomalie"] >= 1
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_per_classe(self):
        ri = _F["mh547_riepilogo"]([_r(rid="A", cl="CREDITI_PPA",
                                       imp=800.0, gg=0.0),
                                    _r(rid="B", cl="CREDITI_PPA",
                                       imp=200.0, gg=10.0)])
        assert set(ri["per_classe"]) == {"CREDITI_PPA"}
        assert ri["per_classe"]["CREDITI_PPA"]["importo"] == pytest.approx(
            1000.0)

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh547_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh547_riepilogo"]("non-lista")


class TestW547Registry:
    def test_titolo_547_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE547) == 3

    def test_registry_tab_count_547(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 700
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 700

    def test_chain_estesa(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700 = st.tabs([" in src
