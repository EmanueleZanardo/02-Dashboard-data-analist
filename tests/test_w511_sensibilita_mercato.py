"""Test tab511 '📉 Sensibilità al rischio di mercato (IFRS 7.40)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh511_num", "mh511_str", "mh511_relazione", "mh511_shocks",
           "mh511_sensibilita", "mh511_analisi", "mh511_riepilogo")

TITLE511 = "📉 Sensibilità al rischio di mercato (IFRS 7.40)"
TITLE510 = "📋 Informativa IFRS 7 (coperture)"


def _rel(**kw):
    d = {"id": "HR-2026-001", "prezzo": 90.0, "dv01_strumento": 100000.0,
         "dv01_coperto": 120000.0}
    d.update(kw)
    return d


class TestW511Validatori:
    def test_num_ok(self):
        assert _F["mh511_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh511_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh511_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh511_str"](bad, "x")


class TestW511Relazione:
    def test_ok(self):
        r = _F["mh511_relazione"](_rel())
        assert r["id"] == "HR-2026-001" and r["prezzo"] == 90.0

    def test_chiave_mancante_ko(self):
        d = _rel()
        del d["dv01_coperto"]
        with pytest.raises(ValueError):
            _F["mh511_relazione"](d)

    def test_prezzo_ko(self):
        for bad in (0.0, -5.0, "90"):
            with pytest.raises(ValueError):
                _F["mh511_relazione"](_rel(prezzo=bad))

    def test_dv01_non_numerica_ko(self):
        with pytest.raises(ValueError):
            _F["mh511_relazione"](_rel(dv01_strumento="x"))


class TestW511Shocks:
    def test_ok(self):
        assert _F["mh511_shocks"]("-25,-10,-5,5,10,25") == \
            [-0.25, -0.1, -0.05, 0.05, 0.1, 0.25]

    def test_punto_e_virgola_e_spazi(self):
        assert _F["mh511_shocks"](" 10 ; -5 ") == [-0.05, 0.1]

    def test_duplicati_rimossi(self):
        assert _F["mh511_shocks"]("10,10,-10") == [-0.1, 0.1]

    def test_ko(self):
        for bad in ("", "   ", "abc", "10,xyz", "0", "0,10", "150",
                    "-101", "nan", "inf"):
            with pytest.raises(ValueError):
                _F["mh511_shocks"](bad)


class TestW511Sensibilita:
    def test_hedge_sotto_coperto_inefficacia_zero(self):
        # |ΔI| < |ΔH|: efficace = ΔI, inefficacia = 0
        r = _F["mh511_sensibilita"](_rel(), 0.10)
        assert r["move"] == pytest.approx(9.0)
        assert r["delta_I"] == pytest.approx(900000.0)
        assert r["delta_H"] == pytest.approx(1080000.0)
        assert r["effetto_pnl"] == pytest.approx(0.0)
        assert r["effetto_oci"] == pytest.approx(900000.0)

    def test_over_hedge_inefficacia(self):
        # |ΔI| > |ΔH|: inefficacia = ΔI - segno(ΔI)*|ΔH|
        r = _F["mh511_sensibilita"](
            _rel(dv01_strumento=150000.0, dv01_coperto=120000.0), 0.25)
        assert r["move"] == pytest.approx(22.5)
        assert r["effetto_pnl"] == pytest.approx(675000.0)
        assert r["effetto_oci"] == pytest.approx(2700000.0)

    def test_shock_negativo_segno(self):
        r = _F["mh511_sensibilita"](
            _rel(dv01_strumento=150000.0, dv01_coperto=120000.0), -0.25)
        assert r["effetto_pnl"] == pytest.approx(-675000.0)
        assert r["effetto_oci"] == pytest.approx(-2700000.0)

    def test_dv01_zero(self):
        r = _F["mh511_sensibilita"](
            _rel(dv01_strumento=0.0, dv01_coperto=0.0), 0.10)
        assert r["effetto_pnl"] == 0.0 and r["effetto_oci"] == 0.0

    def test_shock_degenere_ko(self):
        for bad in (0.0, 1.5, -2.0):
            with pytest.raises(ValueError):
                _F["mh511_sensibilita"](_rel(), bad)


class TestW511Analisi:
    def _rels(self):
        return [_rel(id="A"), _rel(id="B", dv01_strumento=150000.0,
                                   dv01_coperto=120000.0)]

    def test_righe_e_scenari(self):
        a = _F["mh511_analisi"](self._rels(), [-0.1, 0.1], 100000.0)
        assert len(a["righe"]) == 4
        assert len(a["scenari"]) == 2
        assert {s["shock_pct"] for s in a["scenari"]} == {-10.0, 10.0}

    def test_verdetto_stabile(self):
        a = _F["mh511_analisi"]([_rel(id="A")], [-0.25, 0.25], 1e9)
        assert a["riepilogo"]["verdetto"] == "STABILE"
        assert all(s["verdetto"] == "ENTRO_BUDGET" for s in a["scenari"])

    def test_verdetto_sensibile_e_peggiore(self):
        a = _F["mh511_analisi"](self._rels(), [-0.25, 0.25], 100000.0)
        rep = a["riepilogo"]
        assert rep["verdetto"] == "SENSIBILE"
        assert rep["scenario_peggiore_pct"] in (-25.0, 25.0)
        assert rep["max_pnl_abs"] == pytest.approx(675000.0)
        # bordo: max |ineff| == budget -> ENTRO
        a2 = _F["mh511_analisi"](self._rels(), [0.25], 675000.0)
        assert a2["scenari"][0]["verdetto"] == "ENTRO_BUDGET"
        # epsilon: appena sopra il bordo -> FUORI
        a3 = _F["mh511_analisi"](self._rels(), [0.25], 674999.99)
        assert a3["scenari"][0]["verdetto"] == "FUORI_BUDGET"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh511_analisi"]([], [0.1], 100.0)
        dup = [_rel(id="A"), _rel(id="A")]
        with pytest.raises(ValueError):
            _F["mh511_analisi"](dup, [0.1], 100.0)
        with pytest.raises(ValueError):
            _F["mh511_analisi"]([_rel(id="A")], [], 100.0)
        with pytest.raises(ValueError):
            _F["mh511_analisi"]([_rel(id="A")], [0.1], -1.0)

    def test_riepilogo_wrapper(self):
        a = _F["mh511_riepilogo"]([_rel(id="A")], [0.1], 1e9)
        assert a["riepilogo"]["verdetto"] == "STABILE"
        assert a["riepilogo"]["n_relazioni"] == 1


def test_registry_tab511():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 783
    assert TITLE511 in titoli
    assert src.count(TITLE511) == 3
    assert ", tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783 = st.tabs([" in src
    assert "    with tab511:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab511" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab511" in withs
    assert len(withs) == len(dvars) == 783
    # ordine: tab511 dopo tab510
    _decl511 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl511.index(f'"{TITLE510}"') < _decl511.index(f'"{TITLE511}"')
    assert titoli[dvars.index("tab511")] == TITLE511


def test_chiavi_st511_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st511_[^"]+)"', src) + re.findall(
        r'key=f"(st511_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
