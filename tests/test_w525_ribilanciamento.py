"""Test tab525 '⚖️🔄 Ribilanciamento (IFRS 9 6.5.5)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh525_num", "mh525_str", "mh525_relazione", "mh525_misura",
           "mh525_riepilogo")

TITLE525 = "⚖️🔄 Ribilanciamento (IFRS 9 6.5.5)"
TITLE524 = "🧪📐 Derivato ipotetico (IFRS 9 B6.5.5)"


def _r(rid="RIB-2026-001", qi=10000.0, qs=8000.0, hrt=0.80, hrd=0.80,
       ineff=0.0, d="Swap TTF Q1"):
    return {"id": rid, "qta_item_mwh": qi, "qta_strumento_mwh": qs,
            "hr_target": hrt, "hr_designato": hrd,
            "inefficacia_accumulata": ineff, "descrizione": d}


class TestW525Validatori:
    def test_num_ok(self):
        assert _F["mh525_num"](2, "x") == 2.0
        assert _F["mh525_num"](-1.5, "x") == -1.5
        assert _F["mh525_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh525_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh525_str"]("  RIB-1 ", "x") == "RIB-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh525_str"](bad, "x")


class TestW525Relazione:
    def test_ok(self):
        r = _F["mh525_relazione"](_r())
        assert r["id"] == "RIB-2026-001"
        assert r["qta_item_mwh"] == pytest.approx(10000.0)
        assert r["qta_strumento_mwh"] == pytest.approx(8000.0)
        assert r["hr_target"] == pytest.approx(0.80)
        assert r["hr_designato"] == pytest.approx(0.80)
        assert r["inefficacia_accumulata"] == pytest.approx(0.0)
        assert r["descrizione"] == "Swap TTF Q1"
        assert r["hr_effettivo"] == pytest.approx(0.80)
        assert r["qta_strumento_target"] == pytest.approx(8000.0)
        assert r["delta_qta"] == pytest.approx(0.0)

    def test_default_ineff_desc(self):
        d = _r()
        del d["inefficacia_accumulata"]
        del d["descrizione"]
        r = _F["mh525_relazione"](d)
        assert r["inefficacia_accumulata"] == pytest.approx(0.0)
        assert r["descrizione"] == ""

    def test_qi_ko(self):
        for bad in (0, -100, True, "1000", float("nan")):
            with pytest.raises(ValueError):
                _F["mh525_relazione"](_r(qi=bad))

    def test_qs_ko(self):
        for bad in (-1.0, True, "8000", None):
            with pytest.raises(ValueError):
                _F["mh525_relazione"](_r(qs=bad))

    def test_hrt_ko(self):
        for bad in (0, -0.5, 2.01, True, "0.8", float("inf")):
            with pytest.raises(ValueError):
                _F["mh525_relazione"](_r(hrt=bad))

    def test_hrd_ko(self):
        for bad in (-0.1, True, "0.8"):
            with pytest.raises(ValueError):
                _F["mh525_relazione"](_r(hrd=bad))

    def test_chiave_mancante(self):
        d = _r()
        del d["hr_target"]
        with pytest.raises(ValueError):
            _F["mh525_relazione"](d)


class TestW525Misura:
    def test_allineato(self):
        m = _F["mh525_misura"](_r())
        assert m["esito"] == "ALLINEATO"
        assert m["delta_qta_mwh"] == pytest.approx(0.0)
        assert m["hr_effettivo"] == pytest.approx(0.80)

    def test_ribilancia_acquisto(self):
        m = _F["mh525_misura"](_r(rid="RIB-2026-002", qs=5000.0,
                                  ineff=45000.0))
        assert m["esito"] == "RIBILANCIA_ACQUISTO"
        assert m["delta_qta_mwh"] == pytest.approx(3000.0)
        assert m["qta_strumento_target"] == pytest.approx(8000.0)
        assert m["squilibrio_vs_designato"] == pytest.approx(-0.375)
        assert m["inefficacia_a_pnl"] == pytest.approx(45000.0)

    def test_ribilancia_vendita(self):
        m = _F["mh525_misura"](_r(rid="RIB-2026-003", qi=5000.0,
                                  qs=5000.0, hrt=0.80, hrd=0.80))
        assert m["esito"] == "RIBILANCIA_VENDITA"
        assert m["delta_qta_mwh"] == pytest.approx(-1000.0)
        assert m["hr_effettivo"] == pytest.approx(1.0)
        assert m["squilibrio_vs_designato"] == pytest.approx(0.25)

    def test_epsilon_allineato(self):
        # drift sotto 1e-9: ancora ALLINEATO
        m = _F["mh525_misura"](_r(qs=8000.0 + 1e-12))
        assert m["esito"] == "ALLINEATO"

    def test_hrd_zero_squilibrio_none(self):
        m = _F["mh525_misura"](_r(hrd=0.0, qs=5000.0))
        assert m["esito"] == "RIBILANCIA_ACQUISTO"
        assert m["squilibrio_vs_designato"] is None

    def test_qs_zero(self):
        m = _F["mh525_misura"](_r(qs=0.0))
        assert m["esito"] == "RIBILANCIA_ACQUISTO"
        assert m["delta_qta_mwh"] == pytest.approx(8000.0)


class TestW525Riepilogo:
    def _demo(self):
        return [_r(rid="A", qs=8000.0),
                _r(rid="B", qi=10000.0, qs=5000.0, hrt=0.80,
                   hrd=0.80, ineff=45000.0, d="sottodimensionato"),
                _r(rid="C", qi=5000.0, qs=5000.0, hrt=0.80,
                   hrd=0.80, d="sovradimensionato")]

    def test_misto(self):
        a = _F["mh525_riepilogo"](self._demo())
        t = a["totali"]
        assert t["n_relazioni"] == 3
        assert t["n_allineati"] == 1
        assert t["n_da_ribilanciare"] == 2
        assert t["delta_acquisto_MWh"] == pytest.approx(3000.0)
        assert t["delta_vendita_MWh"] == pytest.approx(1000.0)
        assert t["inefficacia_totale_a_pnl"] == pytest.approx(45000.0)
        assert t["verdetto_complessivo"] == "MISTO"
        assert [x["esito"] for x in a["righe"]] == [
            "ALLINEATO", "RIBILANCIA_ACQUISTO", "RIBILANCIA_VENDITA"]

    def test_tutti_allineati(self):
        a = _F["mh525_riepilogo"]([_r(rid="A1"), _r(rid="A2")])
        assert a["totali"]["verdetto_complessivo"] == "TUTTI_ALLINEATI"
        assert a["totali"]["n_allineati"] == 2
        assert a["totali"]["delta_acquisto_MWh"] == pytest.approx(0.0)
        assert a["totali"]["delta_vendita_MWh"] == pytest.approx(0.0)

    def test_nessuno_allineato(self):
        a = _F["mh525_riepilogo"]([_r(rid="B1", qs=5000.0),
                                   _r(rid="B2", qs=12000.0)])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "NESSUNO_ALLINEATO"
        assert t["n_allineati"] == 0
        assert t["delta_acquisto_MWh"] == pytest.approx(3000.0)
        assert t["delta_vendita_MWh"] == pytest.approx(4000.0)

    def test_wrapper_parita_misura(self):
        a = _F["mh525_riepilogo"]([_r()])
        v = _F["mh525_misura"](_r())
        assert a["righe"][0]["delta_qta_mwh"] == pytest.approx(
            v["delta_qta_mwh"])
        assert a["righe"][0]["esito"] == v["esito"]
        assert a["righe"][0]["hr_effettivo"] == pytest.approx(
            v["hr_effettivo"])

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh525_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh525_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh525_riepilogo"]([_r(rid="A"), _r(rid="A")])


def test_registry_tab525():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 758
    assert TITLE525 in titoli
    assert TITLE524 in titoli
    assert src.count(TITLE525) == 3
    assert ", tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758 = st.tabs([" in src
    # chiavi widget st525_* univoche (12 pattern attesi)
    keys = re.findall(r'key=f?"(st525_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 11
