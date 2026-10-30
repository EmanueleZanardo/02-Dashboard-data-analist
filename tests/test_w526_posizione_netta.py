"""Test tab526 '⚖️🧺 Posizione netta (IFRS 9 6.6)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh526_num", "mh526_str", "mh526_item", "mh526_gruppo",
           "mh526_riepilogo")

TITLE526 = "⚖️🧺 Posizione netta (IFRS 9 6.6)"
TITLE525 = "⚖️🔄 Ribilanciamento (IFRS 9 6.5.5)"


def _it(iid="GEN-CCGT", qta=10000.0, prz=85.0, dfv=20000.0, d="x"):
    return {"id": iid, "qta_mwh": qta, "prezzo_eur_mwh": prz,
            "delta_fv": dfv, "descrizione": d}


def _g(gid="GRP-1", items=None, dreal=0.0, sog=0.20):
    return {"id": gid,
            "items": items if items is not None else
            [_it(), _it("LOAD", -6000.0, 92.0, -12000.0)],
            "delta_fv_strumento": dreal, "soglia_proporz": sog,
            "descrizione": "g"}


class TestW526Validatori:
    def test_num_ok(self):
        assert _F["mh526_num"](2, "x") == 2.0
        assert _F["mh526_num"](-1.5, "x") == -1.5
        assert _F["mh526_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh526_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh526_str"]("  GRP-1 ", "x") == "GRP-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh526_str"](bad, "x")


class TestW526Item:
    def test_ok(self):
        r = _F["mh526_item"](_it())
        assert r["id"] == "GEN-CCGT"
        assert r["qta_mwh"] == pytest.approx(10000.0)
        assert r["valore_eur"] == pytest.approx(850000.0)
        assert r["delta_unitario"] == pytest.approx(2.0)

    def test_default_descrizione(self):
        i = _it()
        del i["descrizione"]
        assert _F["mh526_item"](i)["descrizione"] == ""

    def test_qta_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(qta=0.0))

    def test_prezzo_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(prz=-1.0))

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh526_item"]("non un dict")
        i = _it()
        del i["delta_fv"]
        with pytest.raises(ValueError):
            _F["mh526_item"](i)
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(iid="  "))
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(qta=float("nan")))
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(qta=True))
        with pytest.raises(ValueError):
            _F["mh526_item"](_it(d=7))


class TestW526Gruppo:
    def test_designabile_lorda(self):
        r = _F["mh526_gruppo"](_g())
        assert r["esito"] == "DESIGNABILE_LORDA"
        assert "6.6.2" in r["motivo"]
        assert r["qta_netta_mwh"] == pytest.approx(4000.0)
        assert r["qta_lorda_mwh"] == pytest.approx(16000.0)
        assert r["delta_fv_gruppo"] == pytest.approx(8000.0)

    def test_designabile_netta(self):
        r = _F["mh526_gruppo"](_g(items=[_it("A", 5000.0, 80.0, 10000.0),
                                         _it("B", 3000.0, 80.0, 6000.0)]))
        assert r["esito"] == "DESIGNABILE_NETTA"
        assert r["qta_netta_mwh"] == pytest.approx(8000.0)
        assert r["qta_lorda_mwh"] == pytest.approx(8000.0)

    def test_non_designabile_netta_nulla(self):
        r = _F["mh526_gruppo"](_g(items=[_it("A", 5000.0, 78.0, 12500.0),
                                         _it("B", -5000.0, 78.0, -12500.0)]))
        assert r["esito"] == "NON_DESIGNABILE"
        assert "6.6.1(e)" in r["motivo"]
        assert r["qta_netta_mwh"] == pytest.approx(0.0)

    def test_proporzionale(self):
        r = _F["mh526_gruppo"](_g())  # du 2.0 e 2.0
        assert r["proporzionalita"] == "PROPORZIONALE"
        assert r["item_devianti"] == []

    def test_non_proporzionale(self):
        r = _F["mh526_gruppo"](_g(items=[_it("A", 5000.0, 78.0, 12500.0),
                                         _it("B", -5000.0, 78.0, -5000.0)]))
        assert r["proporzionalita"] == "NON_PROPORZIONALE"
        assert set(r["item_devianti"]) == {"A", "B"}

    def test_proporzionale_tutti_fermi(self):
        r = _F["mh526_gruppo"](_g(items=[_it("A", 5000.0, 78.0, 0.0),
                                         _it("B", 3000.0, 78.0, 0.0)]))
        assert r["proporzionalita"] == "PROPORZIONALE"

    def test_inefficacia_e_quota(self):
        r = _F["mh526_gruppo"](_g(dreal=-8200.0))
        assert r["inefficacia"] == pytest.approx(-200.0)
        assert r["quota_efficace"] == pytest.approx(-8000.0)

    def test_soglia_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh526_gruppo"](_g(sog=0.0))
        with pytest.raises(ValueError):
            _F["mh526_gruppo"](_g(sog=1.5))

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh526_gruppo"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh526_gruppo"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh526_gruppo"]({"id": "X", "items": [_it()]})
        with pytest.raises(ValueError):
            _F["mh526_gruppo"](_g(items=[_it("A"), _it("A")]))
        with pytest.raises(ValueError):
            _F["mh526_gruppo"](_g(gid="  "))
        with pytest.raises(ValueError):
            _F["mh526_gruppo"](_g(dreal=float("inf")))


class TestW526Riepilogo:
    def _due(self):
        return [_g("GRP-1", items=[_it("A", 5000.0, 80.0, 10000.0),
                                   _it("B", 3000.0, 80.0, 6000.0)]),
                _g("GRP-2", items=[_it("C", 5000.0, 78.0, 12500.0),
                                   _it("D", -5000.0, 78.0, -12500.0)])]

    def test_misto(self):
        r = _F["mh526_riepilogo"](self._due())
        t = r["totali"]
        assert t["n_gruppi"] == 2
        assert t["n_designabili"] == 1
        assert t["n_non_designabili"] == 1
        assert t["verdetto_complessivo"] == "MISTO"
        assert t["qta_netta_totale_mwh"] == pytest.approx(8000.0)
        assert t["qta_lorda_totale_mwh"] == pytest.approx(18000.0)

    def test_tutti_designabili(self):
        r = _F["mh526_riepilogo"]([self._due()[0]])
        assert r["totali"]["verdetto_complessivo"] == "TUTTI_DESIGNABILI"

    def test_nessuno_designabile(self):
        r = _F["mh526_riepilogo"]([self._due()[1]])
        assert r["totali"]["verdetto_complessivo"] == "NESSUNO_DESIGNABILE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh526_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh526_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh526_riepilogo"]([_g("A"), _g("A")])


def test_registry_tab526():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 810
    assert TITLE526 in titoli
    assert TITLE525 in titoli
    assert src.count(TITLE526) == 3
    assert ", tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810 = st.tabs([" in src
    # chiavi widget st526_* univoche (13 pattern attesi)
    keys = re.findall(r'key=f?"(st526_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 13
