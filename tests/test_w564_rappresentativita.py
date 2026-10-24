"""Test tab564 "Rappresentativita' analisi di sensibilita' (IFRS 7.41-7.42)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh564_num", "mh564_ge0", "mh564_str", "mh564_tipo",
           "mh564_fattore", "mh564_demo", "mh564_riepilogo")

TITLE564 = ("\U0001F4CA\u2696\uFE0F Rappresentativita' analisi di "
            "sensibilita' (IFRS 7.41-7.42)")


def _v(fid="R-1", nome="RF", tipo="COMMODITY", fine=100.0, media=100.0,
       motivo=""):
    return _F["mh564_fattore"](fid, nome, tipo, fine, media, motivo)


class TestW564Validatori:
    def test_num_ok(self):
        assert _F["mh564_num"](2, "x") == 2.0
        assert _F["mh564_num"](-3.5, "x") == -3.5
        assert _F["mh564_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh564_num"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh564_ge0"](0, "x") == 0.0
        assert _F["mh564_ge0"](7, "x") == 7.0

    def test_ge0_ko(self):
        for bad in (-0.01, -100.0, math.nan):
            with pytest.raises(ValueError):
                _F["mh564_ge0"](bad, "x")

    def test_str_ok(self):
        assert _F["mh564_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh564_str"](bad, "x")

    def test_tipo_ok(self):
        for t in ("COMMODITY", "TASSI", "FX", "AZIONI", "ALTRO",
                  "tassi", " fx "):
            assert _F["mh564_tipo"](t) == t.strip().upper()

    def test_tipo_ko(self):
        for bad in ("GAS", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh564_tipo"](bad)


class TestW564Fattore:
    def test_hand_computed(self):
        f = _F["mh564_fattore"]("RIS-001", "Prezzi commodity power/gas",
                                "COMMODITY", 38_200_000.0, 35_000_000.0)
        assert f["deviazione"] == pytest.approx(3.2 / 35.0)
        assert f["motivo"] == ""

    def test_media_nulla_dev_none(self):
        f = _v(media=0.0)
        assert f["deviazione"] is None

    def test_motivo_strip(self):
        f = _v(motivo="  roll q4  ")
        assert f["motivo"] == "roll q4"

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(fid="")
        with pytest.raises(ValueError):
            _v(nome="  ")
        with pytest.raises(ValueError):
            _v(tipo="GAS")
        with pytest.raises(ValueError):
            _v(fine=-1.0)
        with pytest.raises(ValueError):
            _v(media=-1.0)
        with pytest.raises(ValueError):
            _v(fine=math.nan)


class TestW564Demo:
    def test_demo_shape(self):
        d = _F["mh564_demo"]()
        assert len(d) == 3
        assert [f["id"] for f in d] == ["RIS-001", "RIS-002", "RIS-003"]
        assert [f["tipo"] for f in d] == ["COMMODITY", "TASSI", "FX"]

    def test_demo_deviazioni(self):
        d = _F["mh564_demo"]()
        assert d[0]["deviazione"] == pytest.approx(0.0914285714)
        assert d[1]["deviazione"] == pytest.approx(0.5625)
        assert d[2]["deviazione"] == pytest.approx(0.2 / 5.3)
        assert d[1]["motivo"] != ""  # motivo 7.41 fornito per il non
                                     # rappresentativo


class TestW564Riepilogo:
    def test_verdetto_demo(self):
        r = _F["mh564_riepilogo"](_F["mh564_demo"]())
        assert r["verdetto"] == "SENSIBILITA_NON_RAPPRESENTATIVA"
        assert r["n_fattori"] == 3
        assert r["n_non_rappresentativi"] == 1
        assert r["n_anomalie"] == 0
        assert r["esposizione_fine_totale"] == pytest.approx(55_800_000.0)
        # (9.142857% + 56.25% + 3.773585%) / 3 = 23.0555%
        assert r["deviazione_media"] == pytest.approx(
            (0.0914285714 + 0.5625 + 0.2 / 5.3) / 3.0)
        assert r["analizzati"][1]["non_rappresentativo"] is True
        assert r["analizzati"][0]["non_rappresentativo"] is False
        assert r["analizzati"][2]["non_rappresentativo"] is False

    def test_soglia_personalizzata(self):
        # soglia 60%: il fattore tassi (56.25%) diventa rappresentativo
        r = _F["mh564_riepilogo"](_F["mh564_demo"](), soglia_pct=60.0)
        assert r["verdetto"] == "SENSIBILITA_RAPPRESENTATIVA"
        assert r["n_non_rappresentativi"] == 0

    def test_nessun_rischio(self):
        r = _F["mh564_riepilogo"]([_v(fine=0.0, media=100.0)])
        assert r["verdetto"] == "NESSUN_RISCHIO"

    def test_anomalia_motivo_mancante(self):
        r = _F["mh564_riepilogo"]([_v(fine=150.0, media=100.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] >= 1
        assert any("motivo mancante" in a.lower()
                   for f in r["analizzati"] for a in f["anomalie"])

    def test_anomalia_media_nulla(self):
        r = _F["mh564_riepilogo"]([_v(fine=100.0, media=0.0)])
        assert r["n_anomalie"] >= 1
        assert any("media nulla" in a.lower()
                   for f in r["analizzati"] for a in f["anomalie"])

    def test_anomalia_id_duplicato(self):
        r = _F["mh564_riepilogo"]([_v(fid="X"), _v(fid="x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a.lower()
                   for f in r["analizzati"] for a in f["anomalie"])

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh564_riepilogo"]([])

    def test_soglia_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh564_riepilogo"]([_v()], soglia_pct=101.0)

    def test_boundary_soglia(self):
        # deviazione esattamente 20% -> NON_RAPPRESENTATIVA (>=)
        r = _F["mh564_riepilogo"]([_v(fine=120.0, media=100.0,
                                      motivo="m")])
        assert r["n_non_rappresentativi"] == 1


class TestW564Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE564}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 691
        assert TITLE564 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691 = st.tabs([" in src
        assert "with tab564:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st564_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
