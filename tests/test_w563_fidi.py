"""Test tab563 'Limiti di credito controparte (fido)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh563_num", "mh563_ge0", "mh563_str", "mh563_rating",
           "mh563_controparte", "mh563_demo", "mh563_riepilogo")

TITLE563 = ("\U0001F3E6\U0001F4CF Limiti di credito controparte (fido)")


def _v(cid="F-1", nome="CP", rating="BBB", fido=10_000_000.0,
       mtm=1_000_000.0, pfe=500_000.0, garanzie=0.0):
    return _F["mh563_controparte"](cid, nome, rating, fido, mtm, pfe,
                                   garanzie)


class TestW563Validatori:
    def test_num_ok_signed(self):
        # il MtM e' con segno: num accetta anche negativi
        assert _F["mh563_num"](2, "x") == 2.0
        assert _F["mh563_num"](-3.5, "x") == -3.5
        assert _F["mh563_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh563_num"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh563_ge0"](0, "x") == 0.0
        assert _F["mh563_ge0"](7, "x") == 7.0

    def test_ge0_ko(self):
        for bad in (-0.01, -100.0, math.nan):
            with pytest.raises(ValueError):
                _F["mh563_ge0"](bad, "x")

    def test_str_ok(self):
        assert _F["mh563_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh563_str"](bad, "x")

    def test_rating_ok(self):
        for r in ("AAA", "AA", "A", "BBB", "BB", "B", "CCC", "D", "NR",
                  "bbb", " nr "):
            assert _F["mh563_rating"](r) == r.strip().upper()

    def test_rating_ko(self):
        for bad in ("XYZ", "", "AA+", None, 5):
            with pytest.raises(ValueError):
                _F["mh563_rating"](bad)


class TestW563Controparte:
    def test_hand_computed(self):
        c = _F["mh563_controparte"]("FID-001", "Trader TTF", "BBB",
                                   50_000_000.0, 30_000_000.0,
                                   12_000_000.0, 5_000_000.0)
        assert c["esposizione_lorda"] == 42_000_000.0
        assert c["esposizione_netta"] == 37_000_000.0
        assert c["utilizzo"] == pytest.approx(0.74)
        assert c["headroom"] == 13_000_000.0
        assert c["status"] == "OK"

    def test_mtm_negativo_non_e_esposizione(self):
        c = _v(mtm=-5_000_000.0, pfe=2_000_000.0, garanzie=0.0)
        assert c["esposizione_lorda"] == 2_000_000.0
        assert c["esposizione_netta"] == 2_000_000.0
        assert c["status"] == "OK"

    def test_garanzie_azzerano(self):
        c = _v(mtm=1_000_000.0, pfe=500_000.0, garanzie=2_000_000.0)
        assert c["esposizione_netta"] == 0.0
        assert c["utilizzo"] == 0.0
        assert c["status"] == "OK"

    def test_soglie_status(self):
        assert _v(fido=100.0, mtm=75.0, pfe=0.0)["status"] == "ATTENZIONE"
        assert _v(fido=100.0, mtm=74.99, pfe=0.0)["status"] == "OK"
        assert _v(fido=100.0, mtm=90.0, pfe=0.0)["status"] == "CRITICO"
        assert _v(fido=100.0, mtm=100.0, pfe=0.0)["status"] == "CRITICO"
        assert _v(fido=100.0, mtm=100.01, pfe=0.0)["status"] == "SUPERATO"

    def test_fido_non_positivo(self):
        for bad in (0.0, -10.0):
            with pytest.raises(ValueError):
                _v(fido=bad)

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(cid="")
        with pytest.raises(ValueError):
            _v(nome="  ")
        with pytest.raises(ValueError):
            _v(rating="ZZZ")
        with pytest.raises(ValueError):
            _v(pfe=-1.0)
        with pytest.raises(ValueError):
            _v(garanzie=-1.0)
        with pytest.raises(ValueError):
            _v(mtm=math.nan)


class TestW563Demo:
    def test_demo_shape(self):
        d = _F["mh563_demo"]()
        assert len(d) == 3
        assert [c["id"] for c in d] == ["FID-001", "FID-002", "FID-003"]
        assert [c["rating"] for c in d] == ["BBB", "A", "BB"]

    def test_demo_totals(self):
        d = _F["mh563_demo"]()
        assert sum(c["esposizione_netta"] for c in d) == 114_000_000.0
        assert sum(c["fido"] for c in d) == 140_000_000.0
        assert [c["status"] for c in d] == ["OK", "ATTENZIONE", "SUPERATO"]


class TestW563Riepilogo:
    def test_verdetto_demo(self):
        r = _F["mh563_riepilogo"](_F["mh563_demo"]())
        assert r["verdetto"] == "FIDO_SUPERATO"
        assert r["fido_totale"] == 140_000_000.0
        assert r["esposizione_netta_totale"] == 114_000_000.0
        assert r["utilizzo_medio"] == pytest.approx(114.0 / 140.0)
        assert r["n_superati"] == 1
        assert r["n_critici"] == 0
        assert r["n_anomalie"] == 0

    def test_nessuna_esposizione(self):
        r = _F["mh563_riepilogo"]([_v(mtm=0.0, pfe=0.0, garanzie=0.0)])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"

    def test_anomalia_id_duplicato(self):
        r = _F["mh563_riepilogo"]([_v(cid="X"), _v(cid="x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] >= 1
        assert any("duplicato" in a.lower()
                   for c in r["analizzate"] for a in c["anomalie"])

    def test_anomalia_garanzie_eccedenti(self):
        # netta azzerata dalle garanzie: verdetto NESSUNA_ESPOSIZIONE
        # (precedenza come in mh562_*), ma l'anomalia resta registrata
        r = _F["mh563_riepilogo"]([_v(mtm=1.0, pfe=0.0, garanzie=5.0)])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"
        assert r["n_anomalie"] >= 1
        assert any("garanzie eccedenti" in a.lower()
                   for c in r["analizzate"] for a in c["anomalie"])

    def test_anomalia_lorda_nulla(self):
        r = _F["mh563_riepilogo"]([_v(mtm=-3.0, pfe=0.0, garanzie=0.0)])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE" or r["n_anomalie"] >= 1

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh563_riepilogo"]([])

    def test_verdetto_critico(self):
        r = _F["mh563_riepilogo"]([_v(fido=100.0, mtm=95.0, pfe=0.0)])
        assert r["verdetto"] == "FIDO_CRITICO"

    def test_verdetto_sotto_controllo(self):
        r = _F["mh563_riepilogo"]([_v(fido=100.0, mtm=50.0, pfe=0.0)])
        assert r["verdetto"] == "FIDI_SOTTO_CONTROLLO"


class TestW563Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE563}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 766
        assert TITLE563 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766 = st.tabs([" in src
        assert "with tab563:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st563_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
