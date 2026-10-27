"""Test tab514 '📅 Piano di recycling futuro (proiezione release OCI→P&L)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh514_num", "mh514_str", "mh514_periodo",
           "mh514_relazione", "mh514_piano", "mh514_riepilogo")

TITLE514 = "📅 Piano di recycling futuro (proiezione release OCI→P&L)"
TITLE513 = "🧪 Test retrospettivo di efficacia (look-back)"


def _p(periodo="2026-Q1", imp=-3000.0):
    return {"periodo": periodo, "impatto_pnl": imp}


def _r(rid="HR-2026-002", ris=12000.0, periodi=None):
    return {"id": rid, "riserva_iniziale": ris,
            "periodi": periodi if periodi is not None
            else [_p("2026-Q1", -3000.0), _p("2026-Q2", -3000.0),
                  _p("2026-Q3", -3000.0), _p("2026-Q4", -3000.0)]}


class TestW514Validatori:
    def test_num_ok(self):
        assert _F["mh514_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh514_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh514_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh514_str"](bad, "x")


class TestW514Periodo:
    def test_ok(self):
        r = _F["mh514_periodo"](_p())
        assert r["periodo"] == "2026-Q1"
        assert r["impatto_pnl"] == -3000.0

    def test_chiave_mancante_ko(self):
        d = _p()
        del d["impatto_pnl"]
        with pytest.raises(ValueError):
            _F["mh514_periodo"](d)

    def test_non_dict_ko(self):
        with pytest.raises(ValueError):
            _F["mh514_periodo"]("2026-Q1")


class TestW514Relazione:
    def test_ok(self):
        r = _F["mh514_relazione"](_r())
        assert r["id"] == "HR-2026-002"
        assert len(r["periodi"]) == 4

    def test_chiave_mancante_ko(self):
        d = _r()
        del d["riserva_iniziale"]
        with pytest.raises(ValueError):
            _F["mh514_relazione"](d)

    def test_periodi_duplicati_ko(self):
        with pytest.raises(ValueError):
            _F["mh514_relazione"](
                _r(periodi=[_p("2026-Q1"), _p("2026-Q1")]))

    def test_periodi_vuoti_ko(self):
        with pytest.raises(ValueError):
            _F["mh514_relazione"](_r(periodi=[]))


class TestW514Piano:
    def test_completo(self):
        a = _F["mh514_piano"]([_r()])
        o = a["righe"][0]
        assert o["verdetto"] == "COMPLETO"
        assert o["riciclato_totale"] == pytest.approx(12000.0)
        assert o["residuo"] == pytest.approx(0.0, abs=0.01)
        assert o["copertura"] == pytest.approx(1.0)
        det = o["dettaglio"]
        assert [d["riciclaggio"] for d in det] == [3000.0] * 4
        assert det[-1]["riserva_residua"] == pytest.approx(0.0, abs=0.01)

    def test_residuo(self):
        a = _F["mh514_piano"](
            [_r("HR-2026-003", 8000.0,
                [_p("2026-Q1", -2000.0), _p("2026-Q2", -2000.0)])])
        o = a["righe"][0]
        assert o["verdetto"] == "RESIDUO"
        assert o["riciclato_totale"] == pytest.approx(4000.0)
        assert o["residuo"] == pytest.approx(4000.0)
        assert o["copertura"] == pytest.approx(0.5)

    def test_cap_al_residuo(self):
        # impatto maggiore della riserva: ricicla solo il residuo
        a = _F["mh514_piano"]([_r("A", 1000.0, [_p("P1", -5000.0)])])
        o = a["righe"][0]
        assert o["dettaglio"][0]["riciclaggio"] == pytest.approx(1000.0)
        assert o["verdetto"] == "COMPLETO"

    def test_segno_discorde_nessun_riciclaggio(self):
        # impatto che aumenterebbe la riserva: nessun recycling
        a = _F["mh514_piano"]([_r("A", 1000.0, [_p("P1", 5000.0)])])
        o = a["righe"][0]
        assert o["dettaglio"][0]["riciclaggio"] == 0.0
        assert o["verdetto"] == "RESIDUO"
        assert o["residuo"] == pytest.approx(1000.0)

    def test_riserva_negativa(self):
        a = _F["mh514_piano"](
            [_r("A", -6000.0, [_p("P1", 2000.0), _p("P2", 4000.0)])])
        o = a["righe"][0]
        assert [d["riciclaggio"] for d in o["dettaglio"]] == [-2000.0, -4000.0]
        assert o["verdetto"] == "COMPLETO"
        assert o["copertura"] == pytest.approx(1.0)

    def test_totali(self):
        a = _F["mh514_piano"](
            [_r("A", 12000.0,
                [_p("P1", -3000.0), _p("P2", -3000.0),
                 _p("P3", -3000.0), _p("P4", -3000.0)]),
             _r("B", 8000.0, [_p("P1", -2000.0), _p("P2", -2000.0)])])
        tt = a["totali"]
        assert tt["n_relazioni"] == 2
        assert tt["n_complete"] == 1
        assert tt["riserva_iniziale"] == pytest.approx(20000.0)
        assert tt["riciclato_totale"] == pytest.approx(16000.0)
        assert tt["residuo_totale"] == pytest.approx(4000.0)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh514_piano"]([])
        with pytest.raises(ValueError):
            _F["mh514_piano"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh514_piano"]([_r("A"), _r("A")])
        with pytest.raises(ValueError):
            _F["mh514_piano"]([_r(periodi=[_p(imp=float("nan"))])])

    def test_riepilogo_wrapper(self):
        a = _F["mh514_riepilogo"]([_r()])
        assert a["totali"]["n_relazioni"] == 1
        assert a["righe"][0]["verdetto"] == "COMPLETO"


def test_registry_tab514():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 750
    assert TITLE514 in titoli
    assert src.count(TITLE514) == 3
    assert ", tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750 = st.tabs([" in src
    assert "    with tab514:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab514" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab514" in withs
    assert len(withs) == len(dvars) == 750
    # ordine: tab514 dopo tab513
    _decl514 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl514.index(f'"{TITLE513}"') < _decl514.index(f'"{TITLE514}"')
    assert titoli[dvars.index("tab514")] == TITLE514


def test_chiavi_st514_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st514_[^"]+)"', src) + re.findall(
        r'key=f"(st514_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
