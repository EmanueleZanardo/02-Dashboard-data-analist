"""Test tab565 "Fair value: metodi e assunzioni (IFRS 7.27)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh565_num", "mh565_ge0", "mh565_str", "mh565_livello",
           "mh565_tecnica", "mh565_posizione", "mh565_demo",
           "mh565_riepilogo")

TITLE565 = ("\U0001F4CA\U0001F52C Fair value: metodi e assunzioni "
            "(IFRS 7.27)")


def _v(pid="P-1", descrizione="pos", livello="LIVELLO_1",
       tecnica="QUOTAZIONE_MERCATO_ATTIVO", io="q", ino="", fv=100.0):
    return _F["mh565_posizione"](pid, descrizione, livello, tecnica,
                                 io, ino, fv)


class TestW565Validatori:
    def test_num_ok(self):
        assert _F["mh565_num"](2, "x") == 2.0
        assert _F["mh565_num"](-3.5, "x") == -3.5
        assert _F["mh565_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh565_num"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh565_ge0"](0, "x") == 0.0
        assert _F["mh565_ge0"](7, "x") == 7.0

    def test_ge0_ko(self):
        for bad in (-0.01, -100.0, math.nan):
            with pytest.raises(ValueError):
                _F["mh565_ge0"](bad, "x")

    def test_str_ok(self):
        assert _F["mh565_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh565_str"](bad, "x")

    def test_livello_ok(self):
        for t in ("LIVELLO_1", "livello_2", " Livello_3 "):
            assert _F["mh565_livello"](t) == t.strip().upper()

    def test_livello_ko(self):
        for bad in ("LIVELLO_4", "", None, 2):
            with pytest.raises(ValueError):
                _F["mh565_livello"](bad)

    def test_tecnica_ok(self):
        for t in ("QUOTAZIONE_MERCATO_ATTIVO",
                  "market_approach_comparables",
                  " INCOME_APPROACH_DCF ", "MODELLO_OPZIONE",
                  "cost_approach", "non_dichiarata"):
            assert _F["mh565_tecnica"](t) == t.strip().upper()

    def test_tecnica_ko(self):
        for bad in ("DCF", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh565_tecnica"](bad)


class TestW565Posizione:
    def test_hand_computed(self):
        p = _F["mh565_posizione"]("POS-001", "Derivato power", "LIVELLO_3",
                                  "MODELLO_OPZIONE", "curva forward",
                                  "volatilita' implicita", 2_100_000.0)
        assert p["id"] == "POS-001"
        assert p["livello"] == "LIVELLO_3"
        assert p["tecnica"] == "MODELLO_OPZIONE"
        assert p["input_non_osservabili"] == "volatilita' implicita"
        assert p["fair_value"] == 2_100_000.0

    def test_io_ino_non_str(self):
        p = _v(io=None, ino=5)
        assert p["input_osservabili"] == ""
        assert p["input_non_osservabili"] == ""

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(descrizione="  ")
        with pytest.raises(ValueError):
            _v(livello="LIVELLO_0")
        with pytest.raises(ValueError):
            _v(tecnica="MARKET")
        with pytest.raises(ValueError):
            _v(fv=-1.0)
        with pytest.raises(ValueError):
            _v(fv=math.nan)


class TestW565Demo:
    def test_demo_shape(self):
        d = _F["mh565_demo"]()
        assert len(d) == 3
        assert [p["id"] for p in d] == ["POS-001", "POS-002", "POS-003"]
        assert [p["livello"] for p in d] == ["LIVELLO_3", "LIVELLO_2",
                                                "LIVELLO_1"]

    def test_demo_complete(self):
        r = _F["mh565_riepilogo"](_F["mh565_demo"]())
        assert r["verdetto"] == "DISCLOSURE_ADEGUATA"
        assert r["n_anomalie"] == 0
        assert r["copertura"] == pytest.approx(1.0)


class TestW565Riepilogo:
    def test_verdetto_demo(self):
        r = _F["mh565_riepilogo"](_F["mh565_demo"]())
        assert r["verdetto"] == "DISCLOSURE_ADEGUATA"
        assert r["n_posizioni"] == 3
        assert r["n_livello_3"] == 1
        assert r["n_complete"] == 3
        assert r["fair_value_totale"] == pytest.approx(8_700_000.0)
        assert r["copertura"] == pytest.approx(1.0)
        assert all(p["completa"] for p in r["analizzate"])

    def test_copertura_parziale_con_anomalia(self):
        # una posizione su tre incompleta -> copertura 66.67% e anomalia:
        # il verdetto e' ANOMALIE_DA_VERIFICARE (le anomalie prevalgono)
        pos = [_v(pid="A", tecnica="NON_DICHIARATA", livello="LIVELLO_2"),
               _v(pid="B"), _v(pid="C")]
        r = _F["mh565_riepilogo"](pos)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["copertura"] == pytest.approx(2.0 / 3.0)
        assert r["n_complete"] == 2
        assert r["n_anomalie"] == 1

    def test_nessuna_posizione(self):
        r = _F["mh565_riepilogo"]([_v(fv=0.0)])
        assert r["verdetto"] == "NESSUNA_POSIZIONE"

    def test_anomalia_tecnica_mancante_l2(self):
        r = _F["mh565_riepilogo"](
            [_v(pid="X", livello="LIVELLO_2", tecnica="NON_DICHIARATA")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("tecnica di valutazione non dichiarata" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_ino_mancanti_l3(self):
        r = _F["mh565_riepilogo"](
            [_v(pid="X", livello="LIVELLO_3", tecnica="MODELLO_OPZIONE",
                io="curva", ino="")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("input non osservabili non dichiarati" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_io_mancanti_l2(self):
        r = _F["mh565_riepilogo"](
            [_v(pid="X", livello="LIVELLO_2", tecnica="INCOME_APPROACH_DCF",
                io="", ino="")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("input osservabili non dichiarati" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_tecnica_l1(self):
        # livello 1 con tecnica diversa dalla quotazione
        r = _F["mh565_riepilogo"](
            [_v(pid="X", livello="LIVELLO_1", tecnica="MODELLO_OPZIONE")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("livello 1 senza quotazione" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_ino_su_livello_2(self):
        r = _F["mh565_riepilogo"](
            [_v(pid="X", livello="LIVELLO_2", tecnica="INCOME_APPROACH_DCF",
                io="curva", ino="stima interna")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("classificazione da rivedere" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_id_duplicato(self):
        r = _F["mh565_riepilogo"]([_v(pid="X"), _v(pid="x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh565_riepilogo"]([])

    def test_anomalie_senza_posizioni_valide(self):
        # tutte le posizioni con anomalia -> copertura 0%
        pos = [_v(pid="A", livello="LIVELLO_2", tecnica="NON_DICHIARATA"),
               _v(pid="B", livello="LIVELLO_1", tecnica="MODELLO_OPZIONE")]
        r = _F["mh565_riepilogo"](pos)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["copertura"] == pytest.approx(0.0)
        assert r["n_complete"] == 0


class TestW565Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE565}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 683
        assert TITLE565 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683 = st.tabs([" in src
        assert "with tab565:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st565_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
