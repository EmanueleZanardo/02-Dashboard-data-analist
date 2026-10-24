"""Test tab498 '📓 Blotter delle coperture: registro operazioni': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh498_num", "mh498_num_ge0", "mh498_num_pos", "mh498_mese",
           "mh498_data", "mh498_lato", "mh498_spread_bps", "mh498_fee",
           "mh498_tol", "mh498_operazione", "mh498_costo_spread",
           "mh498_costo_operazione", "mh498_netting", "mh498_verdetto",
           "mh498_riepilogo")

TITLE498 = "📓 Blotter delle coperture: registro operazioni"
TITLE497 = "🔓🛡️ Rilascio della copertura: quando alleggerire l'hedge?"


def _op(data, comm, scad, lato, vol, pz, bps, fee):
    return _F["mh498_operazione"](data, comm, scad, lato, vol, pz, bps, fee)


# Demo: due righe sulla stessa linea (buy + sell parziale) e una su altra linea
OP_BUY = _op("2026-10-12", "TTF gas", "2027-01", "ACQUISTO", 60000.0, 88.40, 2.0, 250.0)
OP_SELL = _op("2026-10-13", "TTF gas", "2027-01", "VENDITA", 20000.0, 89.10, 2.0, 120.0)
OP_PWR = _op("2026-10-13", "Power baseload DE", "2027-03", "ACQUISTO", 49938.26, 116.20, 3.0, 400.0)
RIGHE = _F["mh498_netting"]([OP_BUY, OP_SELL, OP_PWR])


class TestW498Validatori:
    def test_num_ok(self):
        assert _F["mh498_num"](3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh498_num"](bad, "x")

    def test_num_pos_ko(self):
        for bad in (0.0, -1.0):
            with pytest.raises(ValueError):
                _F["mh498_num_pos"](bad, "x")

    def test_mese_ok(self):
        assert _F["mh498_mese"]("2027-01", "x") == "2027-01"

    def test_mese_ko(self):
        for bad in ("2027-13", "27-01", 202701, "2027/01"):
            with pytest.raises(ValueError):
                _F["mh498_mese"](bad, "x")

    def test_data_ok(self):
        assert _F["mh498_data"]("2026-10-12", "x") == "2026-10-12"

    def test_data_ko(self):
        for bad in ("2026-13-01", "12/10/2026", "2026-02-30"):
            with pytest.raises(ValueError):
                _F["mh498_data"](bad, "x")

    def test_lato(self):
        assert _F["mh498_lato"]("acquisto", "x") == 1.0
        assert _F["mh498_lato"]("VENDITA", "x") == -1.0
        with pytest.raises(ValueError):
            _F["mh498_lato"]("BUY", "x")

    def test_spread_fee(self):
        assert _F["mh498_spread_bps"](0.0, "x") == 0.0
        for bad in (-1.0, 501.0):
            with pytest.raises(ValueError):
                _F["mh498_spread_bps"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh498_fee"](-5.0, "x")
        with pytest.raises(ValueError):
            _F["mh498_tol"](0.51, "x")


class TestW498Operazione:
    def test_operazione_ok(self):
        assert OP_BUY["lato"] == 1.0
        assert OP_SELL["lato"] == -1.0
        assert OP_BUY["data"] == "2026-10-12"
        assert OP_BUY["scadenza"] == "2027-01"

    def test_operazione_ko(self):
        with pytest.raises(ValueError):
            _op("2026-10-12", "TTF gas", "2027-01", "ACQUISTO", 0.0, 88.40, 2.0, 0.0)
        with pytest.raises(ValueError):
            _op("2026-10-12", "TTF gas", "2027-01", "ACQUISTO", 100.0, -5.0, 2.0, 0.0)
        with pytest.raises(ValueError):
            _op("2026-10-12", "", "2027-01", "ACQUISTO", 100.0, 88.40, 2.0, 0.0)


class TestW498Costi:
    def test_costo_spread(self):
        assert _F["mh498_costo_spread"](1_000_000.0, 5.0) == pytest.approx(500.0)
        assert _F["mh498_costo_spread"](1_000_000.0, 0.0) == 0.0

    def test_costo_operazione(self):
        c = _F["mh498_costo_operazione"](OP_BUY)
        noz = 60000.0 * 88.40
        assert c["nozionale_eur"] == pytest.approx(noz)
        assert c["costo_spread"] == pytest.approx(noz * 2.0 / 10000.0)
        assert c["commissioni"] == 250.0
        assert c["costo_totale"] == pytest.approx(noz * 2.0 / 10000.0 + 250.0)


class TestW498Netting:
    def test_netting_linee(self):
        gas = next(r for r in RIGHE if r["commodity"] == "TTF gas")
        assert (gas["commodity"], gas["scadenza"]) == ("TTF gas", "2027-01")
        assert gas["n_ops"] == 2
        assert gas["acquisti_mwh"] == pytest.approx(60000.0)
        assert gas["vendite_mwh"] == pytest.approx(20000.0)
        assert gas["netto_mwh"] == pytest.approx(40000.0)
        # prezzo medio ponderato sui volumi firmati
        assert gas["prezzo_medio_eur_mwh"] == pytest.approx(88.05)
        assert gas["nozionale_eur"] == pytest.approx(60000.0 * 88.40 + 20000.0 * 89.10)
        assert gas["costo_spread"] == pytest.approx(
            (60000.0 * 88.40 + 20000.0 * 89.10) * 2.0 / 10000.0)
        assert gas["commissioni"] == pytest.approx(370.0)
        assert gas["costo_totale"] == pytest.approx(gas["costo_spread"] + 370.0)

    def test_netting_seconda_linea(self):
        pwr = next(r for r in RIGHE if r["commodity"] == "Power baseload DE")
        assert pwr["netto_mwh"] == pytest.approx(49938.26)
        assert pwr["prezzo_medio_eur_mwh"] == pytest.approx(116.20)

    def test_netting_ordinato(self):
        assert len(RIGHE) == 2
        chiavi = [(r["commodity"], r["scadenza"]) for r in RIGHE]
        assert chiavi == sorted(chiavi)

    def test_netting_netto_zero_prezzo_none(self):
        b = _op("2026-10-12", "TTF gas", "2027-01", "ACQUISTO", 100.0, 90.0, 2.0, 0.0)
        s = _op("2026-10-12", "TTF gas", "2027-01", "VENDITA", 100.0, 90.0, 2.0, 0.0)
        righe = _F["mh498_netting"]([b, s])
        assert righe[0]["netto_mwh"] == pytest.approx(0.0)
        assert righe[0]["prezzo_medio_eur_mwh"] is None
        assert righe[0]["nozionale_eur"] == pytest.approx(18000.0)

    def test_netting_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh498_netting"]([])


class TestW498Riepilogo:
    def _rie(self, budget, tol=0.05):
        op = _op("2026-10-12", "TTF gas", "2027-01", "ACQUISTO",
                 100000.0, 100.0, 5.0, 100.0)
        return _F["mh498_riepilogo"]([op], budget, tol)

    def test_verdetti(self):
        assert self._rie(10000.0)["verdetto"] == "SOTTO_BUDGET"
        assert self._rie(5000.0)["verdetto"] == "IN_LINEA"
        assert self._rie(4000.0)["verdetto"] == "SOPRA_BUDGET"
        # costo = 5100 esatto
        r = self._rie(10000.0)
        assert r["costo_totale"] == pytest.approx(5100.0)
        assert r["varianza_eur"] == pytest.approx(-4900.0)
        assert r["varianza_pct"] == pytest.approx(-0.49)
        assert r["n_operazioni"] == 1
        assert r["mwh_netti"] == pytest.approx(100000.0)

    def test_verdetto_bordo(self):
        # costo == budget*(1-tol) -> SOTTO_BUDGET
        assert _F["mh498_verdetto"](5100.0, 5100.0 / 0.95, 0.05) == "SOTTO_BUDGET"
        # costo == budget*(1+tol) -> IN_LINEA
        assert _F["mh498_verdetto"](5100.0, 5100.0 / 1.05, 0.05) == "IN_LINEA"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh498_riepilogo"]([OP_BUY], 0.0, 0.05)
        with pytest.raises(ValueError):
            _F["mh498_riepilogo"]([], 10000.0, 0.05)


def test_registry_tab498():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 690
    assert TITLE498 in titoli
    assert src.count(TITLE498) == 3
    assert "tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690 = st.tabs([" in src
    assert "    with tab498:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab498" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab498" in withs
    assert len(withs) == len(dvars) == 690
    # ordine: tab498 dopo tab497
    _decl498 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl498.index(f'"{TITLE497}"') < _decl498.index(f'"{TITLE498}"')
    assert titoli[dvars.index("tab498")] == TITLE498


def test_chiavi_st498_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st498_[^"]+)"', src) + re.findall(
        r'key=f"(st498_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10
