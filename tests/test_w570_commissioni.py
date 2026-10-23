"""Test tab570 "Proventi e oneri da commissioni (IFRS 7.17)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh570_num", "mh570_str", "mh570_categoria",
           "mh570_voce", "mh570_demo", "mh570_riepilogo")

TITLE570 = ("\U0001F4B8\U0001F4CA Proventi e oneri da commissioni "
            "(IFRS 7.17)")


def _v(pid="FEE-1", descrizione="voce", cat="BROKERAGE",
       pr=100_000.0, on=40_000.0, no=50_000_000.0):
    return _F["mh570_voce"](pid, descrizione, cat, pr, on, no)


class TestW570Validatori:
    def test_num_ok(self):
        assert _F["mh570_num"](2, "x") == 2.0
        assert _F["mh570_num"](-3.5, "x") == -3.5
        assert _F["mh570_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh570_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh570_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh570_str"](bad, "x")

    def test_categoria_ok(self):
        assert _F["mh570_categoria"]("brokerage", "x") == "BROKERAGE"
        assert _F["mh570_categoria"]("CLEARING", "x") == "CLEARING"
        assert _F["mh570_categoria"]("finanziamento", "x") == "FINANZIAMENTO"

    def test_categoria_ko(self):
        for bad in ("XYZ", "", None, "DERIVATI"):
            with pytest.raises(ValueError):
                _F["mh570_categoria"](bad, "x")


class TestW570Voce:
    def test_hand_computed(self):
        r = _v(pid="FEE-001", pr=45_000.0, on=380_000.0, no=250_000_000.0)
        assert r["id"] == "FEE-001"
        assert r["categoria"] == "BROKERAGE"
        assert r["proventi"] == pytest.approx(45_000.0)
        assert r["oneri"] == pytest.approx(380_000.0)
        assert r["nozionale"] == pytest.approx(250_000_000.0)
        assert r["margine"] == pytest.approx(-335_000.0)
        assert r["segno"] == "NEGATIVO"
        assert r["intensita_pct"] == pytest.approx(0.152)

    def test_segno_positivo(self):
        r = _v(pr=250_000.0, on=60_000.0)
        assert r["margine"] == pytest.approx(190_000.0)
        assert r["segno"] == "POSITIVO"

    def test_segno_neutro(self):
        r = _v(pr=10_000.0, on=10_000.0)
        assert r["margine"] == pytest.approx(0.0)
        assert r["segno"] == "NEUTRO"

    def test_intensita_none_senza_nozionale(self):
        r = _v(pr=250_000.0, on=60_000.0, no=0.0)
        assert r["intensita_pct"] is None
        assert r["nozionale"] == pytest.approx(0.0)

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(cat="XYZ")
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(descrizione="   ")
        with pytest.raises(ValueError):
            _v(pr=math.nan)


class TestW570Demo:
    def test_demo_shape(self):
        d = _F["mh570_demo"]()
        assert len(d) == 3
        assert all(set(r) >= {"proventi", "oneri", "nozionale", "margine",
                              "segno", "intensita_pct", "categoria"}
                   for r in d)

    def test_demo_verdetto(self):
        r = _F["mh570_riepilogo"](_F["mh570_demo"]())
        assert r["verdetto"] == "MARGINE_NEGATIVO"
        assert r["n_anomalie"] == 0
        assert r["margine_netto"] == pytest.approx(-265_000.0)
        # 45k + 0 + 250k proventi; 380k + 120k + 60k oneri
        assert r["proventi_totali"] == pytest.approx(295_000.0)
        assert r["oneri_totali"] == pytest.approx(560_000.0)

    def test_demo_intensita_media(self):
        r = _F["mh570_riepilogo"](_F["mh570_demo"]())
        # 560000 / 430000000 * 100 = 0,1302...% < soglia 2%
        assert r["intensita_media_pct"] == pytest.approx(0.130232, rel=1e-4)
        assert r["nozionale_totale"] == pytest.approx(430_000_000.0)


class TestW570Riepilogo:
    def test_nessuna_commissione(self):
        r = _F["mh570_riepilogo"]([_v(pr=0.0, on=0.0, no=0.0)])
        # la voce nulla e' un'anomalia, ma NESSUNA_* ha la precedenza
        # (convenzione tab566/567/568/569)
        assert r["verdetto"] == "NESSUNA_COMMISIONE"

    def test_id_duplicato(self):
        r = _F["mh570_riepilogo"]([_v(pid="FEE-1", pr=10.0),
                                   _v(pid="fee-1", pr=10.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert any("duplicato" in a.lower()
                   for o in r["analizzate"] for a in o["anomalie"])

    def test_proventi_negativi_anomalia(self):
        r = _F["mh570_riepilogo"]([_v(pr=-5_000.0, on=1_000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_oneri_negativi_anomalia(self):
        r = _F["mh570_riepilogo"]([_v(pr=50_000.0, on=-1_000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_voce_nulla_anomalia(self):
        r = _F["mh570_riepilogo"]([_v(pid="FEE-1", pr=0.0, on=0.0, no=0.0),
                                   _v(pid="FEE-2", pr=100_000.0,
                                      on=10_000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_nozionale_negativo_anomalia(self):
        r = _F["mh570_riepilogo"]([_v(pr=50_000.0, on=10_000.0, no=-1.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_intensita_elevata_boundary(self):
        # oneri/nozionale = 2,0% == soglia -> INTENSITA_ELEVATA (>=)
        r = _F["mh570_riepilogo"]([_v(pr=100_000.0, on=200_000.0,
                                      no=10_000_000.0)],
                                  soglia_intensita_pct=2.0)
        assert r["intensita_media_pct"] == pytest.approx(2.0)
        assert r["verdetto"] == "INTENSITA_ELEVATA"

    def test_intensita_sotto_soglia_margine_positivo(self):
        r = _F["mh570_riepilogo"]([_v(pr=300_000.0, on=100_000.0,
                                      no=50_000_000.0)],
                                  soglia_intensita_pct=2.0)
        assert r["intensita_media_pct"] == pytest.approx(0.2)
        assert r["verdetto"] == "COMMISSIONI_SOTTO_CONTROLLO"

    def test_senza_nozionale_margine_positivo(self):
        r = _F["mh570_riepilogo"]([_v(pr=250_000.0, on=60_000.0, no=0.0)])
        assert r["intensita_media_pct"] is None
        assert r["verdetto"] == "COMMISSIONI_SOTTO_CONTROLLO"

    def test_voci_vuote_ko(self):
        with pytest.raises(ValueError):
            _F["mh570_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (0.0, -100.0):
            with pytest.raises(ValueError):
                _F["mh570_riepilogo"](_F["mh570_demo"](),
                                      soglia_intensita_pct=bad)


class TestW570Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE570}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 661
        assert TITLE570 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661 = st.tabs([" in src
        assert "with tab570:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st570_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
