"""Test tab517 '🧩 Componenti di rischio designati (IFRS 9)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh517_num", "mh517_pct", "mh517_str", "mh517_componente",
           "mh517_valutazione", "mh517_riepilogo")

TITLE517 = "🧩 Componenti di rischio designati (IFRS 9)"
TITLE516 = "⏳ Costo della copertura (time value, IFRS 9)"


def _c(rid="RC-2026-001", elem="PPA baseload 2027", comp="TTF",
       met="contratto_esplicito", quota=80.0, mis=True, imp=65.0):
    return {"id": rid, "elemento": elem, "componente": comp, "metodo": met,
            "quota_designata": quota, "misurabile": mis,
            "impatto_componente": imp}


class TestW517Validatori:
    def test_num_ok(self):
        assert _F["mh517_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh517_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh517_pct"](0.5, "x") == 0.5
        assert _F["mh517_pct"](100.0, "x") == 100.0
        assert _F["mh517_pct"](0.0, "x", zero_ok=True) == 0.0

    def test_pct_ko(self):
        for bad in (0.0, -1.0, 100.1, "50", True):
            with pytest.raises(ValueError):
                _F["mh517_pct"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh517_pct"](-1.0, "x", zero_ok=True)
        with pytest.raises(ValueError):
            _F["mh517_pct"](100.1, "x", zero_ok=True)

    def test_str_ok(self):
        assert _F["mh517_str"]("  RC-1 ", "x") == "RC-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh517_str"](bad, "x")


class TestW517Componente:
    def test_ok(self):
        r = _F["mh517_componente"](_c())
        assert r["id"] == "RC-2026-001"
        assert r["componente"] == "TTF"
        assert r["identificabile"] is True
        assert r["verdetto"] == "DESIGNABILE"
        assert r["motivo"] == ""

    def test_soglia_identificabile(self):
        r = _F["mh517_componente"](_c(imp=10.0))
        assert r["identificabile"] is True
        assert r["verdetto"] == "DESIGNABILE"
        r2 = _F["mh517_componente"](_c(imp=9.99))
        assert r2["identificabile"] is False
        assert r2["verdetto"] == "NON_DESIGNABILE"
        assert "10%" in r2["motivo"]

    def test_non_misurabile(self):
        r = _F["mh517_componente"](_c(mis=False))
        assert r["verdetto"] == "NON_DESIGNABILE"
        assert "misurabile" in r["motivo"]

    def test_doppio_motivo(self):
        r = _F["mh517_componente"](_c(mis=False, imp=8.0))
        assert r["verdetto"] == "NON_DESIGNABILE"
        assert "; " in r["motivo"]

    def test_componente_ko(self):
        with pytest.raises(ValueError):
            _F["mh517_componente"](_c(comp="PETROLIO"))

    def test_metodo_ko(self):
        with pytest.raises(ValueError):
            _F["mh517_componente"](_c(met="a occhio"))

    def test_chiave_mancante_ko(self):
        d = _c()
        del d["quota_designata"]
        with pytest.raises(ValueError):
            _F["mh517_componente"](d)

    def test_quota_ko(self):
        for bad in (0.0, -5.0, 100.1, "80", True, None):
            with pytest.raises(ValueError):
                _F["mh517_componente"](_c(quota=bad))

    def test_impatto_ko(self):
        for bad in (-0.1, 100.1, "65", True, None):
            with pytest.raises(ValueError):
                _F["mh517_componente"](_c(imp=bad))

    def test_mis_non_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh517_componente"](_c(mis="si"))


class TestW517Valutazione:
    def test_demo_misto(self):
        a = _F["mh517_valutazione"](
            [_c(), _c(rid="RC-2026-002", elem="Vendita spark spread Q1",
                      comp="EUA_CO2", met="inferenza_statistica",
                      quota=50.0, mis=False, imp=8.0)])
        tt = a["totali"]
        assert tt["n_componenti"] == 2
        assert tt["n_designabili"] == 1
        assert tt["quota_designata_media"] == pytest.approx(65.0)
        assert tt["impatto_medio"] == pytest.approx(36.5)
        assert tt["verdetto_complessivo"] == "MISTO"
        assert a["righe"][0]["verdetto"] == "DESIGNABILE"
        assert a["righe"][1]["verdetto"] == "NON_DESIGNABILE"

    def test_complessivo_tutte_designabili(self):
        a = _F["mh517_valutazione"]([_c(), _c(rid="B")])
        assert a["totali"]["verdetto_complessivo"] == "TUTTE_DESIGNABILI"

    def test_complessivo_nessuna(self):
        a = _F["mh517_valutazione"]([_c(rid="A", mis=False)])
        assert a["totali"]["verdetto_complessivo"] == "NESSUNA_DESIGNABILE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh517_valutazione"]([])
        with pytest.raises(ValueError):
            _F["mh517_valutazione"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh517_valutazione"]([_c(rid="A"), _c(rid="A")])

    def test_riepilogo_wrapper(self):
        a = _F["mh517_riepilogo"]([_c()])
        assert a["totali"]["n_componenti"] == 1
        assert a["righe"][0]["verdetto"] == "DESIGNABILE"


def test_registry_tab517():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 757
    assert TITLE517 in titoli
    assert src.count(TITLE517) == 3
    assert ", tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757 = st.tabs([" in src
    assert "    with tab517:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab517" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab517" in withs
    assert len(withs) == len(dvars) == 757
    # ordine: tab517 dopo tab516
    _decl517 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl517.index(f'"{TITLE516}"') < _decl517.index(f'"{TITLE517}"')
    assert titoli[dvars.index("tab517")] == TITLE517


def test_chiavi_st517_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    keys = re.findall(r'key="(st517_[^"]+)"', src) + re.findall(
        r'key=f"(st517_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
