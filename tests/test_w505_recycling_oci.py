"""Test tab505 '♻️ Recycling OCI: rilascio della riserva a P&L': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh505_num", "mh505_str", "mh505_ge0", "mh505_voce",
           "mh505_rilascio", "mh505_riepilogo")

TITLE505 = "♻️ Recycling OCI: rilascio della riserva a P&L"
TITLE504 = "📊📓 Diario dell'inefficacia: OCI vs P&L per periodo"


def _demo():
    return [_F["mh505_voce"](n, q) for n, q in
            [("Fornitura Gen-Feb", 40000.0),
             ("Fornitura Mar", 50000.0),
             ("Fornitura Apr", 50000.0),
             ("Conguaglio Q2", 0.0)]]


class TestW505Validatori:
    def test_num_ok(self):
        assert _F["mh505_num"](3, "x") == 3.0
        assert _F["mh505_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh505_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh505_str"]("  Gen-Feb  ", "x") == "Gen-Feb"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh505_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh505_ge0"](0, "x") == 0.0
        assert _F["mh505_ge0"](12.5, "x") == 12.5

    def test_ge0_ko(self):
        for bad in (-0.1, "-3", None, float("nan")):
            with pytest.raises(ValueError):
                _F["mh505_ge0"](bad, "x")

    def test_voce_ok(self):
        v = _F["mh505_voce"](" A ", 100.0)
        assert v == {"nome": "A", "quota": 100.0}

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh505_voce"]("", 100.0)
        with pytest.raises(ValueError):
            _F["mh505_voce"]("A", -1.0)
        with pytest.raises(ValueError):
            _F["mh505_voce"]("A", float("inf"))


class TestW505Rilascio:
    def test_demo_fifo(self):
        righe = _F["mh505_rilascio"](_demo(), 150000.0, 0.0)
        assert [r["rilasciato"] for r in righe] == \
            [40000.0, 50000.0, 50000.0, 0.0]
        assert [r["residuo_dopo"] for r in righe] == \
            [110000.0, 60000.0, 10000.0, 10000.0]
        assert [r["verdetto"] for r in righe] == \
            ["RILASCIATA", "RILASCIATA", "RILASCIATA", "NESSUN_RILASCIO"]

    def test_parziale_e_non_rilasciata(self):
        voci = [_F["mh505_voce"]("A", 60000.0),
                _F["mh505_voce"]("B", 60000.0),
                _F["mh505_voce"]("C", 10000.0)]
        righe = _F["mh505_rilascio"](voci, 100000.0, 0.0)
        assert righe[0]["rilasciato"] == 60000.0
        assert righe[0]["verdetto"] == "RILASCIATA"
        assert righe[1]["rilasciato"] == 40000.0
        assert righe[1]["verdetto"] == "RILASCIATA_PARZIALE"
        assert righe[2]["rilasciato"] == 0.0
        assert righe[2]["verdetto"] == "NON_RILASCIATA"
        assert righe[2]["residuo_dopo"] == 0.0

    def test_identita_contabile(self):
        # somma rilasciati + residuo finale = |riserva|
        riserva = 150000.0
        righe = _F["mh505_rilascio"](_demo(), riserva, 0.0)
        assert sum(abs(r["rilasciato"]) for r in righe) + \
            abs(righe[-1]["residuo_dopo"]) == pytest.approx(riserva)

    def test_riserva_negativa_segno(self):
        voci = [_F["mh505_voce"]("A", 30000.0)]
        righe = _F["mh505_rilascio"](voci, -50000.0, 0.0)
        assert righe[0]["rilasciato"] == -30000.0
        assert righe[0]["residuo_dopo"] == -20000.0
        assert righe[0]["verdetto"] == "RILASCIATA"

    def test_riserva_vuota(self):
        righe = _F["mh505_rilascio"](_demo(), 0.0, 0.0)
        assert all(r["rilasciato"] == 0.0 for r in righe)
        assert righe[0]["verdetto"] == "NON_RILASCIATA"
        assert righe[3]["verdetto"] == "NESSUN_RILASCIO"
        assert _F["mh505_riepilogo"](_demo(), 0.0, 0.0)["verdetto_complessivo"] == "RISERVA_VUOTA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh505_rilascio"]([], 1000.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh505_rilascio"](_demo(), float("nan"), 0.0)
        with pytest.raises(ValueError):
            _F["mh505_rilascio"](_demo(), 1000.0, -1.0)


class TestW505Riepilogo:
    def test_demo(self):
        s = _F["mh505_riepilogo"](_demo(), 150000.0, 0.0)
        assert s["n_voci"] == 4
        assert s["conteggi"] == {"RILASCIATA": 3, "RILASCIATA_PARZIALE": 0,
                                 "NON_RILASCIATA": 0, "NESSUN_RILASCIO": 1}
        assert s["verdetto_complessivo"] == "RILASCIO_PARZIALE"
        assert s["riserva_iniziale_eur"] == 150000.0
        assert s["rilasciato_eur"] == 140000.0
        assert s["residuo_eur"] == pytest.approx(10000.0)
        assert s["ratio_rilasciata"] == pytest.approx(140000.0 / 150000.0)
        assert s["voci_con_rilascio"] == 3
        assert len(s["righe"]) == 4

    def test_completo(self):
        voci = [_F["mh505_voce"]("A", 40000.0),
                _F["mh505_voce"]("B", 60000.0)]
        s = _F["mh505_riepilogo"](voci, 100000.0, 0.0)
        assert s["verdetto_complessivo"] == "RILASCIO_COMPLETO"
        assert s["residuo_eur"] == 0.0
        assert s["ratio_rilasciata"] == 1.0

    def test_materialita_chiude(self):
        # residuo 10'000 <= tolleranza 10'000 -> COMPLETO
        s = _F["mh505_riepilogo"](_demo(), 150000.0, 10000.0)
        assert s["verdetto_complessivo"] == "RILASCIO_COMPLETO"

    def test_riserva_vuota(self):
        s = _F["mh505_riepilogo"](_demo(), 0.0, 0.0)
        assert s["verdetto_complessivo"] == "RISERVA_VUOTA"
        assert s["ratio_rilasciata"] == 0.0

    def test_nessun_rilascio(self):
        voci = [_F["mh505_voce"]("A", 0.0), _F["mh505_voce"]("B", 0.0)]
        s = _F["mh505_riepilogo"](voci, 50000.0, 0.0)
        assert s["verdetto_complessivo"] == "NESSUN_RILASCIO"
        assert s["rilasciato_eur"] == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh505_riepilogo"]([], 1000.0, 0.0)


def test_registry_tab505():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 655
    assert TITLE505 in titoli
    assert src.count(TITLE505) == 3
    assert "tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655 = st.tabs([" in src
    assert "    with tab505:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab505" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab505" in withs
    assert len(withs) == len(dvars) == 655
    # ordine: tab505 dopo tab504
    _decl505 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl505.index(f'"{TITLE504}"') < _decl505.index(f'"{TITLE505}"')
    assert titoli[dvars.index("tab505")] == TITLE505


def test_chiavi_st505_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st505_[^"]+)"', src) + re.findall(
        r'key=f"(st505_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
