"""Test tab516 '⏳ Costo della copertura (time value, IFRS 9)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh516_num", "mh516_str", "mh516_opzione",
           "mh516_costo", "mh516_riepilogo")

TITLE516 = "⏳ Costo della copertura (time value, IFRS 9)"
TITLE515 = "🛑 Cessazione della copertura (hedge discontinuation)"


def _o(rid="OP-2026-001", fv=12500.0, intr=8000.0, tv=4500.0,
       tipo="periodo", nper=6, real=False):
    return {"id": rid, "fair_value": fv, "intrinsic": intr,
            "time_value": tv, "tipo": tipo, "n_periodi": nper,
            "transazione_realizzata": real}


class TestW516Validatori:
    def test_num_ok(self):
        assert _F["mh516_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh516_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh516_str"]("  OP-1 ", "x") == "OP-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh516_str"](bad, "x")


class TestW516Opzione:
    def test_ok(self):
        r = _F["mh516_opzione"](_o())
        assert r["id"] == "OP-2026-001"
        assert r["tipo"] == "periodo"
        assert r["n_periodi"] == 6
        assert r["scostamento"] == pytest.approx(0.0)
        assert r["scostamento_ok"] is True

    def test_scostamento_flag(self):
        r = _F["mh516_opzione"](_o(fv=12510.0))
        assert r["scostamento"] == pytest.approx(10.0)
        assert r["scostamento_ok"] is False

    def test_tipo_ko(self):
        with pytest.raises(ValueError):
            _F["mh516_opzione"](_o(tipo="futuro"))

    def test_chiave_mancante_ko(self):
        d = _o()
        del d["time_value"]
        with pytest.raises(ValueError):
            _F["mh516_opzione"](d)

    def test_n_periodi_ko(self):
        for bad in (0, -3, 1.5, "6", True, None):
            with pytest.raises(ValueError):
                _F["mh516_opzione"](_o(nper=bad))

    def test_real_non_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh516_opzione"](_o(real="si"))


class TestW516Costo:
    def test_periodo_piano(self):
        a = _F["mh516_costo"]([_o()])
        o = a["righe"][0]
        assert o["verdetto"] == "AMMORTAMENTO_SISTEMATICO"
        assert o["quota_periodo"] == pytest.approx(750.0)
        assert len(o["piano"]) == 6
        assert o["piano"][0] == {"periodo": 1, "quota": pytest.approx(750.0),
                                 "residuo": pytest.approx(3750.0)}
        assert o["piano"][-1]["residuo"] == pytest.approx(0.0)
        assert o["ammortizzato"] == pytest.approx(4500.0)
        assert o["differito"] == pytest.approx(0.0)
        assert o["rilasciato"] == pytest.approx(0.0)

    def test_transazione_differita(self):
        a = _F["mh516_costo"](
            [_o(rid="B", tipo="transazione", nper=1, real=False)])
        o = a["righe"][0]
        assert o["verdetto"] == "DIFFERITO_OCI"
        assert o["quota_periodo"] is None
        assert o["piano"] == []
        assert o["differito"] == pytest.approx(4500.0)

    def test_transazione_rilasciata(self):
        a = _F["mh516_costo"](
            [_o(rid="B", tipo="transazione", nper=1, real=True)])
        o = a["righe"][0]
        assert o["verdetto"] == "RILASCIO_A_PNL"
        assert o["rilasciato"] == pytest.approx(4500.0)
        assert o["differito"] == pytest.approx(0.0)

    def test_totali_demo(self):
        a = _F["mh516_costo"]([
            _o("OP-2026-001", 12500.0, 8000.0, 4500.0, "periodo", 6, False),
            _o("OP-2026-002", 6200.0, 5000.0, 1200.0,
               "transazione", 1, False)])
        tt = a["totali"]
        assert tt["n_opzioni"] == 2
        assert tt["costo_totale"] == pytest.approx(5700.0)
        assert tt["ammortizzato_totale"] == pytest.approx(4500.0)
        assert tt["differito_totale"] == pytest.approx(1200.0)
        assert tt["rilasciato_totale"] == pytest.approx(0.0)
        assert tt["n_scostamenti"] == 0
        assert tt["verdetto_complessivo"] == "MISTO"

    def test_complessivo_tutto_differito(self):
        a = _F["mh516_costo"](
            [_o("A", tipo="transazione", nper=1, real=False)])
        assert a["totali"]["verdetto_complessivo"] == "TUTTO_DIFFERITO"

    def test_complessivo_tutto_rilasciato(self):
        a = _F["mh516_costo"](
            [_o("A", tipo="transazione", nper=1, real=True)])
        assert a["totali"]["verdetto_complessivo"] == "TUTTO_RILASCIATO"

    def test_complessivo_tutto_ammortamento(self):
        a = _F["mh516_costo"]([_o("A"), _o("B")])
        assert a["totali"]["verdetto_complessivo"] == \
            "AMMORTAMENTO_SISTEMATICO"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh516_costo"]([])
        with pytest.raises(ValueError):
            _F["mh516_costo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh516_costo"]([_o(rid="A"), _o(rid="A")])
        with pytest.raises(ValueError):
            _F["mh516_costo"]([_o(tv=float("nan"))])

    def test_riepilogo_wrapper(self):
        a = _F["mh516_riepilogo"]([_o()])
        assert a["totali"]["n_opzioni"] == 1
        assert a["righe"][0]["verdetto"] == "AMMORTAMENTO_SISTEMATICO"


def test_registry_tab516():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 820
    assert TITLE516 in titoli
    assert src.count(TITLE516) == 3
    assert ", tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820 = st.tabs([" in src
    assert "    with tab516:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab516" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab516" in withs
    assert len(withs) == len(dvars) == 820
    # ordine: tab516 dopo tab515
    _decl516 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl516.index(f'"{TITLE515}"') < _decl516.index(f'"{TITLE516}"')
    assert titoli[dvars.index("tab516")] == TITLE516


def test_chiavi_st516_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st516_[^"]+)"', src) + re.findall(
        r'key=f"(st516_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
