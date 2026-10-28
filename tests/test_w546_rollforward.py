"""Test tab546 'Rollforward fondo svalutazione crediti (IFRS 7.16)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh546_num", "mh546_signed", "mh546_str", "mh546_stadio",
           "mh546_riga", "mh546_demo", "mh546_riepilogo")

TITLE546 = "📒➡️ Rollforward fondo svalutazione crediti (IFRS 7.16)"


def _r(rid="R-1", d="x", st="STADIO_1", ap=1000.0, acc=0.0, uti=0.0,
       ril=0.0, alt=0.0):
    return {"id": rid, "descrizione": d, "stadio": st, "apertura": ap,
            "accantonamento": acc, "utilizzi": uti, "rilasci": ril,
            "altri": alt}


class TestW546Validatori:
    def test_num_ok(self):
        assert _F["mh546_num"](2, "x") == 2.0
        assert _F["mh546_num"](0, "x") == 0.0
        assert _F["mh546_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh546_num"](bad, "x")

    def test_signed_ok(self):
        assert _F["mh546_signed"](-5.0, "x") == -5.0
        assert _F["mh546_signed"](0, "x") == 0.0
        assert _F["mh546_signed"](2.5, "x") == 2.5

    def test_signed_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh546_signed"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh546_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh546_str"](bad, "x")

    def test_stadio_ok_ko(self):
        for ok in ("STADIO_1", "STADIO_2", "STADIO_3"):
            assert _F["mh546_stadio"](ok, "x") == ok
        for bad in ("STADIO_4", "stadio_1", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh546_stadio"](bad, "x")


class TestW546Riga:
    def test_chiusura_calcolo(self):
        o = _F["mh546_riga"](_r(ap=2500000.0, acc=900000.0, ril=250000.0))
        assert o["chiusura"] == pytest.approx(3150000.0)
        assert o["variazione_netta"] == pytest.approx(650000.0)
        assert o["anomalie"] == []

    def test_chiusura_con_altri_negativi(self):
        o = _F["mh546_riga"](_r(st="STADIO_2", ap=4000000.0, acc=1400000.0,
                                uti=300000.0, ril=100000.0, alt=-50000.0))
        assert o["chiusura"] == pytest.approx(4950000.0)
        assert o["variazione_netta"] == pytest.approx(950000.0)
        assert o["anomalie"] == []

    def test_anomalia_chiusura_negativa(self):
        o = _F["mh546_riga"](_r(ap=100.0, uti=500.0))
        assert o["chiusura"] == pytest.approx(-400.0)
        assert any("chiusura negativa" in a for a in o["anomalie"])

    def test_anomalia_writeoff_oltre_disponibile(self):
        o = _F["mh546_riga"](_r(ap=1000.0, acc=200.0, uti=1500.0))
        assert any("write-off" in a for a in o["anomalie"])

    def test_anomalia_writeoff_boundary_ok(self):
        o = _F["mh546_riga"](_r(ap=1000.0, acc=200.0, uti=1200.0))
        assert o["chiusura"] == pytest.approx(0.0)
        assert not any("write-off" in a for a in o["anomalie"])

    def test_anomalia_rilasci_oltre_disponibile(self):
        o = _F["mh546_riga"](_r(ap=1000.0, acc=200.0, ril=1500.0))
        assert any("rilasci" in a for a in o["anomalie"])

    def test_anomalia_stadio3_azzerato_senza_writeoff(self):
        o = _F["mh546_riga"](_r(st="STADIO_3", ap=500.0, ril=500.0))
        assert o["chiusura"] == pytest.approx(0.0)
        assert any("azzerato senza write-off" in a for a in o["anomalie"])

    def test_anomalia_stadio2_senza_accantonamento(self):
        o = _F["mh546_riga"](_r(st="STADIO_2", ap=1000.0))
        assert any("zero accantonamenti" in a for a in o["anomalie"])

    def test_stadio1_senza_accantonamento_ok(self):
        o = _F["mh546_riga"](_r(st="STADIO_1", ap=1000.0))
        assert o["anomalie"] == []

    def test_riga_ko(self):
        with pytest.raises(ValueError):
            _F["mh546_riga"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh546_riga"](_r(ap=-1.0))
        with pytest.raises(ValueError):
            _F["mh546_riga"](_r(acc=-5.0))
        with pytest.raises(ValueError):
            _F["mh546_riga"](_r(alt="x"))
        with pytest.raises(ValueError):
            _F["mh546_riga"](_r(st="STADIO_4"))
        with pytest.raises(ValueError):
            _F["mh546_riga"](_r(rid=""))


class TestW546Demo:
    def test_demo_verdetto(self):
        demo = _F["mh546_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["ECL-S1-001", "ECL-S2-002",
                                          "ECL-S3-003"]
        ri = _F["mh546_riepilogo"](demo)
        assert ri["apertura_tot"] == pytest.approx(15000000.0)
        assert ri["chiusura_tot"] == pytest.approx(15300000.0)
        assert ri["variazione_netta_tot"] == pytest.approx(300000.0)
        assert ri["accantonamento_tot"] == pytest.approx(4500000.0)
        assert ri["utilizzi_tot"] == pytest.approx(3800000.0)
        assert ri["verdetto"] == "ROLLFORWARD_STABILE"
        assert ri["n_anomalie"] == 0
        assert set(ri["per_stadio"]) == {"STADIO_1", "STADIO_2", "STADIO_3"}
        assert ri["per_stadio"]["STADIO_3"]["chiusura"] == pytest.approx(
            7200000.0)


class TestW546Riepilogo:
    def test_verdetto_deterioramento(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, acc=300.0)])
        assert ri["chiusura_tot"] == pytest.approx(1300.0)
        assert ri["verdetto"] == "FONDO_IN_DETERIORAMENTO"

    def test_verdetto_deterioramento_boundary(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, acc=150.0)])
        assert ri["verdetto"] == "ROLLFORWARD_STABILE"
        ri2 = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, acc=150.01)])
        assert ri2["verdetto"] == "FONDO_IN_DETERIORAMENTO"

    def test_verdetto_miglioramento(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, ril=200.0)])
        assert ri["verdetto"] == "FONDO_IN_MIGLIORAMENTO"

    def test_verdetto_miglioramento_boundary(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, ril=150.0)])
        assert ri["verdetto"] == "ROLLFORWARD_STABILE"
        ri2 = _F["mh546_riepilogo"]([_r(rid="A", ap=1000.0, ril=150.01)])
        assert ri2["verdetto"] == "FONDO_IN_MIGLIORAMENTO"

    def test_nessun_fondo(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=0.0)])
        assert ri["verdetto"] == "NESSUN_FONDO"

    def test_anomalie_da_verificare(self):
        ri = _F["mh546_riepilogo"]([_r(rid="A", ap=100.0, uti=500.0)])
        assert ri["n_anomalie"] >= 1
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh546_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh546_riepilogo"]("non-lista")


class TestW546Registry:
    def test_titolo_546_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE546) == 3

    def test_registry_tab_count_546(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 776
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 776

    def test_chain_estesa(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776 = st.tabs([" in src
