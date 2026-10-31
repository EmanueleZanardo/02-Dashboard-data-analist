"""Test tab555 'Fair value: movimenti livello 3 (IFRS 7.28)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh555_num", "mh555_num_signed", "mh555_str", "mh555_voce",
           "mh555_demo", "mh555_riepilogo")

TITLE555 = "📐⚖️ Fair value: movimenti livello 3 (IFRS 7.28)"


def _v(vid="L3-1", d="x", ap=1000000.0, pl=100000.0, oc=50000.0,
       ac=200000.0, rg=150000.0, ti=0.0, to=0.0):
    return {"id": vid, "descrizione": d, "apertura": ap,
            "utili_perdite_pl": pl, "utili_perdite_oci": oc,
            "acquisti_emissioni": ac, "regolamenti": rg,
            "trasferimenti_in": ti, "trasferimenti_out": to}


class TestW555Validatori:
    def test_num_ok(self):
        assert _F["mh555_num"](2, "x") == 2.0
        assert _F["mh555_num"](0, "x") == 0.0
        assert _F["mh555_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh555_num"](bad, "x")

    def test_num_signed_ok(self):
        assert _F["mh555_num_signed"](-5, "x") == -5.0
        assert _F["mh555_num_signed"](0, "x") == 0.0
        assert _F["mh555_num_signed"](3.25, "x") == 3.25

    def test_num_signed_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh555_num_signed"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh555_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh555_str"](bad, "x")

    def test_voce_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh555_voce"](["no"])


class TestW555Voce:
    def test_chiusura_e_variazione(self):
        o = _F["mh555_voce"](_v())
        # 1M + 100k + 50k + 200k - 150k = 1.2M
        assert o["chiusura"] == pytest.approx(1200000.0)
        assert o["variazione_netta"] == pytest.approx(200000.0)
        assert o["variazione_pct"] == pytest.approx(0.2)
        assert o["anomalie"] == []

    def test_variazione_none_apertura_zero(self):
        o = _F["mh555_voce"](_v(ap=0.0, pl=0.0, oc=0.0, ac=500.0, rg=100.0))
        assert o["chiusura"] == pytest.approx(400.0)
        assert o["variazione_pct"] is None
        assert o["anomalie"] == []

    def test_regolamenti_oltre_detenuto(self):
        o = _F["mh555_voce"](_v(ap=100.0, ac=0.0, ti=0.0, rg=150.0))
        assert len(o["anomalie"]) == 1
        assert "regolamenti" in o["anomalie"][0].lower()

    def test_trasferimenti_out_oltre_detenuto(self):
        o = _F["mh555_voce"](_v(ap=100.0, pl=0.0, oc=0.0, ac=0.0,
                                rg=0.0, ti=0.0, to=120.0))
        # to=120 oltre il detenuto=100 -> anche chiusura negativa: 2 anomalie
        assert len(o["anomalie"]) == 2
        assert any("trasferimenti" in a.lower() for a in o["anomalie"])

    def test_chiusura_negativa(self):
        o = _F["mh555_voce"](_v(ap=100.0, pl=-300.0, oc=0.0, ac=0.0,
                                rg=0.0, ti=0.0, to=0.0))
        assert o["chiusura"] == pytest.approx(-200.0)
        assert any("negativa" in a.lower() for a in o["anomalie"])

    def test_voce_ferma(self):
        o = _F["mh555_voce"](_v(ap=100.0, pl=0.0, oc=0.0, ac=0.0,
                                rg=0.0, ti=0.0, to=0.0))
        assert any("ferma" in a.lower() for a in o["anomalie"])

    def test_pl_negativo_ok(self):
        o = _F["mh555_voce"](_v(pl=-400000.0))
        # 1M - 400k + 50k + 200k - 150k = 700k
        assert o["chiusura"] == pytest.approx(700000.0)
        assert o["anomalie"] == []


class TestW555Riepilogo:
    def test_demo_riepilogo(self):
        demo = _F["mh555_demo"]()
        assert len(demo) == 3
        r = _F["mh555_riepilogo"](demo)
        # apertura 4.3M; chiusure 2.75M + 1.01M + 0.8M = 4.56M
        assert r["apertura_tot"] == pytest.approx(4300000.0)
        assert r["chiusura_tot"] == pytest.approx(4560000.0)
        assert r["variazione_netta_tot"] == pytest.approx(260000.0)
        assert r["variazione_pct_tot"] == pytest.approx(260000.0 / 4300000.0)
        assert r["n_anomalie"] == 0
        # +6.05% < soglia 10% -> STABILE
        assert r["verdetto"] == "LIVELLO3_STABILE"

    def test_verdetto_crescita(self):
        r = _F["mh555_riepilogo"]([_v(ap=1000.0, pl=300.0, oc=0.0,
                                      ac=0.0, rg=0.0)])
        assert r["verdetto"] == "LIVELLO3_IN_CRESCITA"

    def test_verdetto_riduzione(self):
        r = _F["mh555_riepilogo"]([_v(ap=1000.0, pl=-250.0, oc=0.0,
                                      ac=0.0, rg=0.0)])
        assert r["verdetto"] == "LIVELLO3_IN_RIDUZIONE"

    def test_verdetto_anomalie(self):
        r = _F["mh555_riepilogo"]([_v(ap=100.0, pl=0.0, oc=0.0, ac=0.0,
                                      rg=500.0, ti=0.0, to=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] >= 1

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh555_riepilogo"]([])

    def test_soglie_degeneri(self):
        for bad in (0.0, -0.1, 1.5, math.nan, True, "0.1"):
            with pytest.raises(ValueError):
                _F["mh555_riepilogo"]([_v()], soglia_crescita=bad)
            with pytest.raises(ValueError):
                _F["mh555_riepilogo"]([_v()], soglia_riduzione=bad)

    def test_soglie_personalizzate(self):
        r = _F["mh555_riepilogo"]([_v(ap=1000.0, pl=60.0, oc=0.0,
                                      ac=0.0, rg=0.0)],
                                 soglia_crescita=0.05,
                                 soglia_riduzione=0.05)
        assert r["verdetto"] == "LIVELLO3_IN_CRESCITA"


class TestW555Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_555_presente(self):
        assert self._src().count(TITLE555) == 3

    def test_counts_555(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 834
        assert TITLE555 in titoli
        assert "tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830, tab831, tab832, tab833, tab834 = st.tabs([" in src

    def test_chiavi_555_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st555_" in ln]
        # le f-string st555_id_{_i555} generano istanze a runtime: la base
        # e' fino al suffisso numerico; run/csv1/csv2 sono chiavi distinte
        basi = []
        for ln in righe:
            basi.append(re.search(r"st555_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 14
