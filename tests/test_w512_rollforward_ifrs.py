"""Test tab512 '📒 Rollforward riserva cash-flow hedge (OCI)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh512_num", "mh512_str", "mh512_riga",
           "mh512_rollforward", "mh512_riepilogo")

TITLE512 = "📒 Rollforward riserva cash-flow hedge (OCI)"
TITLE511 = "📉 Sensibilità al rischio di mercato (IFRS 7.40)"


def _riga(**kw):
    d = {"id": "HR-2026-001", "saldo_iniziale": 85000.0,
         "quota_efficace": 12500.0, "recycling": 5000.0,
         "altri_movimenti": 0.0, "imposte": 1875.0,
         "saldo_finale_contabile": 90625.0}
    d.update(kw)
    return d


def _demo():
    return [_riga(),
            _riga(id="HR-2026-002", saldo_iniziale=40000.0,
                  quota_efficace=-3200.0, recycling=2000.0,
                  altri_movimenti=500.0, imposte=720.0,
                  saldo_finale_contabile=34580.0),
            _riga(id="HR-2026-003", saldo_iniziale=0.0,
                  quota_efficace=8000.0, recycling=0.0,
                  altri_movimenti=0.0, imposte=1920.0,
                  saldo_finale_contabile=6580.0)]


class TestW512Validatori:
    def test_num_ok(self):
        assert _F["mh512_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh512_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh512_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh512_str"](bad, "x")


class TestW512Riga:
    def test_ok(self):
        r = _F["mh512_riga"](_riga())
        assert r["id"] == "HR-2026-001"
        assert r["saldo_iniziale"] == 85000.0
        assert r["quota_efficace"] == 12500.0

    def test_segno_libero(self):
        # quota efficace e altri movimenti possono essere negativi
        r = _F["mh512_riga"](_riga(quota_efficace=-3200.0,
                                   altri_movimenti=-150.0))
        assert r["quota_efficace"] == -3200.0
        assert r["altri_movimenti"] == -150.0

    def test_chiave_mancante_ko(self):
        d = _riga()
        del d["recycling"]
        with pytest.raises(ValueError):
            _F["mh512_riga"](d)

    def test_non_numerica_ko(self):
        with pytest.raises(ValueError):
            _F["mh512_riga"](_riga(imposte="x"))

    def test_id_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh512_riga"](_riga(id="   "))

    def test_non_dict_ko(self):
        with pytest.raises(ValueError):
            _F["mh512_riga"](["HR-2026-001"])


class TestW512Rollforward:
    def test_riga_quadrata(self):
        # 85000 + 12500 - 5000 + 0 - 1875 = 90625 -> scostamento 0
        a = _F["mh512_rollforward"]([_riga()])
        o = a["righe"][0]
        assert o["saldo_finale_calcolato"] == 90625.0
        assert o["scostamento"] == 0.0
        assert o["verdetto"] == "QUADRATO"
        assert a["totali"]["verdetto"] == "QUADRATO"
        assert a["totali"]["n_sbilanciate"] == 0

    def test_riga_sbilanciata(self):
        # contabile 90625 + 500 -> scostamento +500.0
        a = _F["mh512_rollforward"](
            [_riga(saldo_finale_contabile=91125.0)])
        o = a["righe"][0]
        assert o["saldo_finale_calcolato"] == 90625.0
        assert o["scostamento"] == pytest.approx(500.0)
        assert o["verdetto"] == "SBILANCIATO"
        assert a["totali"]["verdetto"] == "SBILANCIATO"
        assert a["totali"]["n_sbilanciate"] == 1

    def test_demo_totali(self):
        a = _F["mh512_rollforward"](_demo())
        tt = a["totali"]
        assert len(a["righe"]) == 3
        assert [o["verdetto"] for o in a["righe"]] == \
            ["QUADRATO", "QUADRATO", "SBILANCIATO"]
        # riga 3: 0 + 8000 - 0 + 0 - 1920 = 6080; contabile 6580 -> +500
        assert a["righe"][2]["saldo_finale_calcolato"] == 6080.0
        assert a["righe"][2]["scostamento"] == pytest.approx(500.0)
        assert tt["saldo_iniziale"] == pytest.approx(125000.0)
        assert tt["quota_efficace"] == pytest.approx(17300.0)
        assert tt["recycling"] == pytest.approx(7000.0)
        assert tt["altri_movimenti"] == pytest.approx(500.0)
        assert tt["imposte"] == pytest.approx(4515.0)
        assert tt["saldo_finale_calcolato"] == pytest.approx(131285.0)
        assert tt["saldo_finale_contabile"] == pytest.approx(131785.0)
        # scostamento totale = 6580 - 6080 della sola riga 3
        assert tt["scostamento"] == pytest.approx(500.0)
        assert tt["n_sbilanciate"] == 1
        assert tt["verdetto"] == "SBILANCIATO"

    def test_tolleranza_bordo(self):
        # |scost| <= 0.005 € -> QUADRATO; oltre -> SBILANCIATO
        base = dict(saldo_iniziale=100.0, quota_efficace=0.0,
                    recycling=0.0, altri_movimenti=0.0, imposte=0.0)
        a = _F["mh512_rollforward"](
            [_riga(saldo_finale_contabile=100.005, **base)])
        assert a["righe"][0]["verdetto"] == "QUADRATO"
        b = _F["mh512_rollforward"](
            [_riga(saldo_finale_contabile=100.006, **base)])
        assert b["righe"][0]["verdetto"] == "SBILANCIATO"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh512_rollforward"]([])
        with pytest.raises(ValueError):
            _F["mh512_rollforward"]("non una lista")
        dup = [_riga(id="A"), _riga(id="A")]
        with pytest.raises(ValueError):
            _F["mh512_rollforward"](dup)
        with pytest.raises(ValueError):
            _F["mh512_rollforward"](
                [_riga(saldo_iniziale=float("nan"))])

    def test_riepilogo_wrapper(self):
        a = _F["mh512_riepilogo"]([_riga()])
        assert a["totali"]["verdetto"] == "QUADRATO"
        assert a["totali"]["n_relazioni"] == 1


def test_registry_tab512():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 736
    assert TITLE512 in titoli
    assert src.count(TITLE512) == 3
    assert ", tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736 = st.tabs([" in src
    assert "    with tab512:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab512" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab512" in withs
    assert len(withs) == len(dvars) == 736
    # ordine: tab512 dopo tab511
    _decl512 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl512.index(f'"{TITLE511}"') < _decl512.index(f'"{TITLE512}"')
    assert titoli[dvars.index("tab512")] == TITLE512


def test_chiavi_st512_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st512_[^"]+)"', src) + re.findall(
        r'key=f"(st512_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
