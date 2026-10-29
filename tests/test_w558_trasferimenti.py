"""Test tab558 'Trasferimenti tra livelli fair value (IFRS 7.30)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh558_num", "mh558_str", "mh558_ge0", "mh558_direzione",
           "mh558_politica", "mh558_trasferimento", "mh558_demo",
           "mh558_riepilogo")

TITLE558 = "📊🔀 Trasferimenti tra livelli fair value (IFRS 7.30)"


def _mk(tid="T-1", classe="Forward", direzione="L2_VERSO_L1",
        importo=1000000.0, motivo="motivo", politica="DATA_EVENTO"):
    return _F["mh558_trasferimento"](tid, classe, direzione, importo,
                                     motivo, politica)


class TestW558Validatori:
    def test_num_ok(self):
        assert _F["mh558_num"](2, "x") == 2.0
        assert _F["mh558_num"](0, "x") == 0.0
        assert _F["mh558_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh558_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh558_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh558_str"](bad, "x")

    def test_direzione_ok(self):
        assert _F["mh558_direzione"]("l2_verso_l1") == "L2_VERSO_L1"
        assert _F["mh558_direzione"]("L1_VERSO_L2") == "L1_VERSO_L2"

    def test_direzione_ko(self):
        for bad in (None, "L1", "L2", "", "L1_VERSO_L3"):
            with pytest.raises(ValueError):
                _F["mh558_direzione"](bad)

    def test_politica_ok(self):
        assert _F["mh558_politica"]("data_evento") == "DATA_EVENTO"
        assert _F["mh558_politica"]("INIZIO_PERIODO") == "INIZIO_PERIODO"
        assert _F["mh558_politica"]("FINE_PERIODO") == "FINE_PERIODO"

    def test_politica_ko(self):
        for bad in (None, "", "META_PERIODO"):
            with pytest.raises(ValueError):
                _F["mh558_politica"](bad)


class TestW558Trasferimento:
    def test_ok(self):
        t = _mk("TRF-1", "Forward PSV", "L1_VERSO_L2", 5e6, "delisting",
                "FINE_PERIODO")
        assert t == {"id": "TRF-1", "classe": "Forward PSV",
                     "direzione": "L1_VERSO_L2", "importo_fv": 5000000.0,
                     "motivo": "delisting", "politica": "FINE_PERIODO"}

    def test_ko(self):
        with pytest.raises(ValueError):
            _mk(tid="  ")
        with pytest.raises(ValueError):
            _mk(classe="")
        with pytest.raises(ValueError):
            _mk(direzione="L3_VERSO_L1")
        with pytest.raises(ValueError):
            _mk(importo=-1)
        with pytest.raises(ValueError):
            _mk(motivo="   ")
        with pytest.raises(ValueError):
            _mk(politica="SEMPRE")


class TestW558Riepilogo:
    def test_demo(self):
        ts = _F["mh558_demo"]()
        assert len(ts) == 4
        r = _F["mh558_riepilogo"](ts)
        assert r["importo_totale"] == pytest.approx(9500000.0)
        assert r["n_trasferimenti"] == 4
        assert r["verso_l1"] == pytest.approx(6800000.0)
        assert r["verso_l2"] == pytest.approx(2700000.0)
        assert r["saldo_netto_verso_l1"] == pytest.approx(4100000.0)
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "TRASFERIMENTI_BILANCIATI"
        assert r["politiche_usate"] == ["DATA_EVENTO"]

    def test_verdetti_direzionali(self):
        r1 = _F["mh558_riepilogo"](
            [_mk("A", direzione="L2_VERSO_L1", importo=1e6)])
        assert r1["verdetto"] == "MIGLIORAMENTO_LIQUIDITA"
        assert r1["saldo_netto_verso_l1"] == pytest.approx(1e6)
        r2 = _F["mh558_riepilogo"](
            [_mk("A", direzione="L1_VERSO_L2", importo=1e6)])
        assert r2["verdetto"] == "DETERIORAMENTO_LIQUIDITA"
        assert r2["saldo_netto_verso_l1"] == pytest.approx(-1e6)

    def test_nessun_trasferimento(self):
        r = _F["mh558_riepilogo"]([_mk("A", importo=0.0)])
        assert r["verdetto"] == "NESSUN_TRASFERIMENTO"
        assert r["n_anomalie"] == 1
        per_id = {o["id"]: o for o in r["analizzati"]}
        assert per_id["A"]["anomalie"] == [
            "importo nullo (trasferimento senza importo)"]

    def test_id_duplicato(self):
        r = _F["mh558_riepilogo"]([_mk("DUP"), _mk("DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert "ID duplicato" in r["analizzati"][1]["anomalie"][0]

    def test_politica_non_uniforme(self):
        r = _F["mh558_riepilogo"](
            [_mk("A", politica="DATA_EVENTO"),
             _mk("B", politica="FINE_PERIODO")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert r["politiche_usate"] == ["DATA_EVENTO", "FINE_PERIODO"]

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh558_riepilogo"]([])


class TestW558Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_558_presente(self):
        assert self._src().count(TITLE558) == 3

    def test_counts_558(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 799
        assert TITLE558 in titoli
        assert "tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799 = st.tabs([" in src

    def test_chiavi_558_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st558_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st558_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
