"""Test tab566 "Sensibilita' fair value livello 3 (IFRS 7.27(h))": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh566_num", "mh566_str", "mh566_livello",
           "mh566_posizione", "mh566_demo", "mh566_riepilogo")

TITLE566 = ("\U0001F4CA\U0001F3AF Sensibilita' fair value livello 3 "
            "(IFRS 7.27(h))")


def _v(pid="P-L3-1", descrizione="pos", livello="LIVELLO_3", fv=100.0,
       inome="volatilita'", ibase=1.0, shock=10.0):
    return _F["mh566_posizione"](pid, descrizione, livello, fv, inome,
                                 ibase, shock)


class TestW566Validatori:
    def test_num_ok(self):
        assert _F["mh566_num"](2, "x") == 2.0
        assert _F["mh566_num"](-3.5, "x") == -3.5
        assert _F["mh566_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh566_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh566_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh566_str"](bad, "x")

    def test_livello_ok(self):
        for t in ("LIVELLO_1", "livello_2", " Livello_3 "):
            assert _F["mh566_livello"](t) == t.strip().upper()

    def test_livello_ko(self):
        for bad in ("LIVELLO_4", "", None, 2):
            with pytest.raises(ValueError):
                _F["mh566_livello"](bad)


class TestW566Posizione:
    def test_hand_computed(self):
        p = _F["mh566_posizione"]("POS-L3-001", "Spark spread",
                                  "LIVELLO_3", 4_800_000.0,
                                  "volatilita'", 0.42, 15.0)
        assert p["id"] == "POS-L3-001"
        assert p["livello"] == "LIVELLO_3"
        assert p["fv_shock_su"] == pytest.approx(5_520_000.0)
        assert p["fv_shock_giu"] == pytest.approx(4_080_000.0)
        assert p["var_max_pct"] == pytest.approx(15.0)

    def test_shock_non_positivo_non_calcolabile(self):
        p = _v(shock=0.0)
        assert p["fv_shock_su"] is None
        assert p["fv_shock_giu"] is None
        assert p["var_max_pct"] is None

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(descrizione="  ")
        with pytest.raises(ValueError):
            _v(livello="LIVELLO_0")
        with pytest.raises(ValueError):
            _v(fv=math.nan)
        with pytest.raises(ValueError):
            _v(ibase="x")
        with pytest.raises(ValueError):
            _v(shock=None)


class TestW566Demo:
    def test_demo_shape(self):
        d = _F["mh566_demo"]()
        assert len(d) == 3
        assert [p["id"] for p in d] == ["POS-L3-001", "POS-L3-002",
                                       "POS-L3-003"]
        assert [p["livello"] for p in d] == ["LIVELLO_3"] * 3

    def test_demo_shocks(self):
        d = _F["mh566_demo"]()
        assert [p["var_max_pct"] for p in d] == [15.0, 10.0, 20.0]


class TestW566Riepilogo:
    def test_verdetto_demo(self):
        r = _F["mh566_riepilogo"](_F["mh566_demo"]())
        assert r["verdetto"] == "SENSIBILITA_ELEVATA"
        assert r["n_posizioni"] == 3
        assert r["fair_value_totale"] == pytest.approx(19_200_000.0)
        assert r["sensibilita_max_pct"] == pytest.approx(20.0)
        assert r["n_sopra_soglia"] == 3
        assert r["n_anomalie"] == 0
        assert all(p["sopra_soglia"] for p in r["analizzate"])

    def test_sensibilita_contenuta_soglia_alta(self):
        r = _F["mh566_riepilogo"](_F["mh566_demo"](), soglia_pct=25.0)
        assert r["verdetto"] == "SENSIBILITA_CONTENUTA"
        assert r["n_sopra_soglia"] == 0

    def test_anomalia_fv_nullo(self):
        r = _F["mh566_riepilogo"]([_v(pid="A"),
                                   _v(pid="Z", fv=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nullo o negativo" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_fv_negativo(self):
        r = _F["mh566_riepilogo"]([_v(pid="A"),
                                   _v(pid="Z", fv=-5.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nullo o negativo" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_shock_non_positivo(self):
        r = _F["mh566_riepilogo"]([_v(pid="Z", shock=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("shock non positivo" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_livello_non_3(self):
        r = _F["mh566_riepilogo"](
            [_v(pid="Z", livello="LIVELLO_2", inome="")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("non di livello 3" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])
        # su livello 2 l'input mancante non genera anche l'anomalia
        # "input non osservabile non dichiarato"
        assert not any("non osservabile non dichiarato" in a.lower()
                       for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_input_mancante_livello_3(self):
        r = _F["mh566_riepilogo"]([_v(pid="Z", inome="  ")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("input non osservabile non dichiarato" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_id_duplicato(self):
        r = _F["mh566_riepilogo"]([_v(pid="X"), _v(pid="x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalie_prevalgono_su_elevata(self):
        # sensibilita' elevata MA con anomalia -> ANOMALIE_DA_VERIFICARE
        r = _F["mh566_riepilogo"]([_v(pid="A", shock=20.0),
                                   _v(pid="A", shock=25.0)])
        assert r["sensibilita_max_pct"] == pytest.approx(25.0)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_nessuna_posizione(self):
        r = _F["mh566_riepilogo"]([_v(pid="Z", fv=0.0, shock=0.0)])
        assert r["verdetto"] == "NESSUNA_POSIZIONE"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh566_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (-1.0, 101.0, math.nan):
            with pytest.raises(ValueError):
                _F["mh566_riepilogo"]([_v()], soglia_pct=bad)


class TestW566Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE566}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 673
        assert TITLE566 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673 = st.tabs([" in src
        assert "with tab566:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st566_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
