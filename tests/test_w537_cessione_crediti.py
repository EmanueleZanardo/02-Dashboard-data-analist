"""Test tab537 '🏭📤 Cessione crediti (IFRS 9 3.2)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh537_num", "mh537_pct", "mh537_str", "mh537_bool",
           "mh537_cessione", "mh537_demo", "mh537_riepilogo")

TITLE537 = "🏭📤 Cessione crediti (IFRS 9 3.2)"


def _c(cid="C-1", d="x", vc=100000.0, pr=98000.0, q=50.0, cg=False,
       gm=0.0, si=False):
    return {"id": cid, "descrizione": d, "valore_contabile": vc,
            "prezzo_cessione": pr, "quota_rischi_trasferita_pct": q,
            "con_garanzia": cg, "garanzia_max_pct": gm,
            "servizio_incasso": si}


class TestW537Validatori:
    def test_num_ok(self):
        assert _F["mh537_num"](2, "x") == 2.0
        assert _F["mh537_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh537_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh537_pct"](0.0, "x") == 0.0
        assert _F["mh537_pct"](100.0, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "50", None):
            with pytest.raises(ValueError):
                _F["mh537_pct"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh537_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh537_bool"](True, "x") is True
        assert _F["mh537_bool"](False, "x") is False
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh537_bool"](bad, "x")


class TestW537Cessione:
    def test_cessione_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh537_cessione"]("x")

    def test_cessione_chiavi_mancanti(self):
        _d = _c()
        del _d["prezzo_cessione"]
        with pytest.raises(ValueError):
            _F["mh537_cessione"](_d)

    def test_cessione_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh537_cessione"](_c(cid="  "))

    def test_cessione_vc_ko(self):
        for bad in (0.0, -5.0, "1", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh537_cessione"](_c(vc=bad))

    def test_cessione_prezzo_ko(self):
        for bad in (0.0, -1.0, True):
            with pytest.raises(ValueError):
                _F["mh537_cessione"](_c(pr=bad))

    def test_cessione_quota_ko(self):
        for bad in (-0.1, 100.1, "90"):
            with pytest.raises(ValueError):
                _F["mh537_cessione"](_c(q=bad))

    def test_cessione_garanzia_ko(self):
        for bad in (-1.0, 101.0):
            with pytest.raises(ValueError):
                _F["mh537_cessione"](_c(gm=bad))
        with pytest.raises(ValueError):
            _F["mh537_cessione"](_c(cg=1))
        with pytest.raises(ValueError):
            _F["mh537_cessione"](_c(si="no"))

    def test_derecognition_soglia_90(self):
        _r = _F["mh537_cessione"](_c(q=90.0, vc=100000.0, pr=97000.0))
        assert _r["esito"] == "DERECOGNITION"
        assert _r["utile_perdita_ce"] == pytest.approx(-3000.0)
        assert _r["coinvolgimento_residuo"] == 0.0
        assert _r["passivita_associata"] == 0.0
        assert "3.2.4(a)" in _r["motivo"]

    def test_derecognition_utile(self):
        _r = _F["mh537_cessione"](_c(q=95.0, vc=100000.0, pr=101000.0))
        assert _r["utile_perdita_ce"] == pytest.approx(1000.0)
        assert "utile" in _r["nota_contabile"]

    def test_no_derecognition_soglia_10(self):
        _r = _F["mh537_cessione"](_c(q=10.0, vc=100000.0, pr=98000.0))
        assert _r["esito"] == "NO_DERECOGNITION"
        assert _r["utile_perdita_ce"] == 0.0
        assert _r["coinvolgimento_residuo"] == 100000.0
        assert _r["passivita_associata"] == 98000.0
        assert "3.2.4(b)" in _r["motivo"]

    def test_continuing_involvement_garanzia(self):
        _r = _F["mh537_cessione"](_c(q=60.0, vc=100000.0, pr=95000.0,
                                     cg=True, gm=20.0, si=True))
        assert _r["esito"] == "CONTINUING_INVOLVEMENT"
        assert _r["coinvolgimento_residuo"] == pytest.approx(20000.0)
        assert _r["passivita_associata"] == pytest.approx(20000.0)
        assert "garanzia" in _r["motivo"]
        assert "servicing" in _r["motivo"]
        assert "3.2.16" in _r["motivo"]

    def test_continuing_involvement_senza_garanzia(self):
        _r = _F["mh537_cessione"](_c(q=45.0, vc=100000.0, pr=95000.0))
        assert _r["esito"] == "CONTINUING_INVOLVEMENT"
        assert _r["coinvolgimento_residuo"] == pytest.approx(100000.0)
        assert "controllo residuo" in _r["motivo"]

    def test_limiti_interni(self):
        _r1 = _F["mh537_cessione"](_c(q=89.9))
        _r2 = _F["mh537_cessione"](_c(q=10.1))
        assert _r1["esito"] == "CONTINUING_INVOLVEMENT"
        assert _r2["esito"] == "CONTINUING_INVOLVEMENT"


class TestW537DemoRiepilogo:
    def test_demo_tre_casi(self):
        _demo = _F["mh537_demo"]()
        assert len(_demo) == 3
        _esiti = [_F["mh537_cessione"](_d)["esito"] for _d in _demo]
        assert _esiti == ["DERECOGNITION", "NO_DERECOGNITION",
                          "CONTINUING_INVOLVEMENT"]

    def test_demo_ids(self):
        _demo = _F["mh537_demo"]()
        assert [_d["id"] for _d in _demo] == ["CRED-EN-001", "CRED-EN-002",
                                             "CRED-GO-003"]

    def test_nota_contabile(self):
        _demo = _F["mh537_demo"]()
        _n1 = _F["mh537_cessione"](_demo[0])["nota_contabile"]
        _n2 = _F["mh537_cessione"](_demo[1])["nota_contabile"]
        _n3 = _F["mh537_cessione"](_demo[2])["nota_contabile"]
        assert "a CE" in _n1
        assert "passivita' finanziaria" in _n2
        assert "passivita' associata" in _n3

    def test_riepilogo_misto(self):
        _demo = _F["mh537_demo"]()
        _an = [_F["mh537_cessione"](_d) for _d in _demo]
        _r = _F["mh537_riepilogo"](_an)
        assert _r == {"n": 3, "n_derecognition": 1,
                      "n_no_derecognition": 1, "n_continuing": 1,
                      "verdetto": "MISTO"}

    def test_riepilogo_verdetti(self):
        _mk = lambda e: {"esito": e}
        assert _F["mh537_riepilogo"](
            [_mk("DERECOGNITION")])["verdetto"] == "TUTTI_STORNATI"
        assert _F["mh537_riepilogo"](
            [_mk("NO_DERECOGNITION")])["verdetto"] == "NESSUNO_STORNO"
        assert _F["mh537_riepilogo"](
            [_mk("CONTINUING_INVOLVEMENT")])["verdetto"] == "TUTTO_RESIDUO"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh537_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh537_riepilogo"]("x")
        with pytest.raises(ValueError):
            _F["mh537_riepilogo"]([{"esito": "ALTRO"}])


class TestW537Registry:
    def test_titolo_537_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE537) == 3

    def test_registry_tab_count_537(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 765
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 765

    def test_tab537_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765 = st.tabs([" in src
        assert "with tab537:" in src

    def test_chiavi_st537_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st537_[^\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
