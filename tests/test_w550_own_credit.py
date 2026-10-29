"""Test tab550 'Rischio di credito proprio su passivita' FVTPL (IFRS 7.9-7.10)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh550_num", "mh550_signed", "mh550_str", "mh550_metodo",
           "mh550_quota", "mh550_voce", "mh550_demo", "mh550_riepilogo")

TITLE550 = "🏛️💳 Rischio di credito proprio su passività FVTPL (IFRS 7.9-7.10)"


def _v(vid="V-1", d="x", vc=1000000.0, sc=1000000.0, vp=0.0, vcum=0.0,
       mt="SPREAD_CDS_PROPRIO", qo=1.0):
    return {"id": vid, "descrizione": d, "valore_contabile": vc,
            "importo_scadenza": sc, "var_credito_periodo": vp,
            "var_credito_cumulata": vcum, "metodo": mt, "quota_oci": qo}


class TestW550Validatori:
    def test_num_ok(self):
        assert _F["mh550_num"](2, "x") == 2.0
        assert _F["mh550_num"](0, "x") == 0.0
        assert _F["mh550_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh550_num"](bad, "x")

    def test_signed_ok_ko(self):
        assert _F["mh550_signed"](-3.5, "x") == -3.5
        assert _F["mh550_signed"](0, "x") == 0.0
        assert _F["mh550_signed"](100, "x") == 100.0
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh550_signed"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh550_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh550_str"](bad, "x")

    def test_metodo_ok_ko(self):
        for ok in ("SPREAD_CDS_PROPRIO", "CURVA_BOND_PROPRIA",
                   "MODELLO_INTERNO"):
            assert _F["mh550_metodo"](ok, "x") == ok
        for bad in ("CDS", "spread_cds_proprio", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh550_metodo"](bad, "x")

    def test_quota_ok_ko(self):
        assert _F["mh550_quota"](0, "x") == 0.0
        assert _F["mh550_quota"](1, "x") == 1.0
        assert _F["mh550_quota"](0.35, "x") == 0.35
        for bad in (-0.01, 1.01, 2, math.nan, math.inf, True, "0.5",
                    None):
            with pytest.raises(ValueError):
                _F["mh550_quota"](bad, "x")


class TestW550Voce:
    def test_voce_ok(self):
        o = _F["mh550_voce"](_v())
        assert o["id"] == "V-1"
        assert o["valore_contabile"] == 1000000.0
        assert o["importo_scadenza"] == 1000000.0
        assert o["diff_scadenza"] == 0.0
        assert o["var_credito_periodo"] == 0.0
        assert o["var_credito_cumulata"] == 0.0
        assert o["quota_oci"] == 1.0
        assert o["var_oci"] == 0.0
        assert o["var_pnl"] == 0.0
        assert o["anomalie"] == []

    def test_voce_derivati(self):
        o = _F["mh550_voce"](_v(vc=48000000.0, sc=50000000.0, vp=-1200000.0,
                               vcum=-4500000.0, qo=1.0))
        assert o["diff_scadenza"] == -2000000.0
        assert o["var_oci"] == -4500000.0
        assert o["var_pnl"] == 0.0
        assert o["anomalie"] == []

    def test_anomalia_scadenza_mancante(self):
        o = _F["mh550_voce"](_v(vc=1000.0, sc=0.0))
        assert len(o["anomalie"]) == 1
        assert "7.9(b)" in o["anomalie"][0]

    def test_anomalia_vc_nullo(self):
        o = _F["mh550_voce"](_v(vc=0.0, sc=1000.0))
        assert len(o["anomalie"]) == 1
        assert "rilevazione iniziale" in o["anomalie"][0]

    def test_anomalia_tutto_pnl(self):
        o = _F["mh550_voce"](_v(vcum=-5000.0, qo=0.0))
        assert len(o["anomalie"]) == 1
        assert "5.7.7" in o["anomalie"][0]

    def test_anomalia_mista(self):
        o = _F["mh550_voce"](_v(vcum=-5000.0, qo=0.5))
        assert len(o["anomalie"]) == 1
        assert "mista" in o["anomalie"][0]
        assert o["var_oci"] == -2500.0
        assert o["var_pnl"] == -2500.0

    def test_anomalia_periodo_senza_cumulata(self):
        o = _F["mh550_voce"](_v(vp=1000.0, vcum=0.0))
        assert len(o["anomalie"]) == 1
        assert "7.9(a)" in o["anomalie"][0]

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh550_voce"](["non", "dict"])
        with pytest.raises(ValueError):
            _F["mh550_voce"]({})
        _bad = _v()
        _bad["quota_oci"] = 1.5
        with pytest.raises(ValueError):
            _F["mh550_voce"](_bad)
        _bad = _v()
        _bad["metodo"] = "XXX"
        with pytest.raises(ValueError):
            _F["mh550_voce"](_bad)
        _bad = _v()
        _bad["valore_contabile"] = "1000"
        with pytest.raises(ValueError):
            _F["mh550_voce"](_bad)


class TestW550Demo:
    def test_demo_struttura(self):
        d = _F["mh550_demo"]()
        assert len(d) == 3
        assert [v["id"] for v in d] == ["BOND-IT-001", "STRD-DE-002",
                                       "EMTN-UK-003"]
        for v in d:
            _F["mh550_voce"](v)

    def test_demo_riepilogo(self):
        ri = _F["mh550_riepilogo"](_F["mh550_demo"]())
        assert ri["n_voci"] == 3
        assert ri["vc_tot"] == 85000000.0
        assert ri["scadenza_tot"] == 87000000.0
        assert ri["diff_scadenza_tot"] == -2000000.0
        assert ri["var_cum_tot"] == -4700000.0
        assert ri["var_oci_tot"] == -4700000.0
        assert ri["var_pnl_tot"] == 0.0
        assert ri["quota_rel"] == pytest.approx(4700000.0 / 85000000.0)
        assert ri["n_anomalie"] == 0
        assert ri["verdetto"] == "OWN_CREDIT_RILEVANTE"
        assert ri["per_metodo"]["SPREAD_CDS_PROPRIO"]["vc"] == 48000000.0
        assert ri["per_metodo"]["CURVA_BOND_PROPRIA"]["var_cum"] == 900000.0


class TestW550Riepilogo:
    def test_verdetto_regolare(self):
        ri = _F["mh550_riepilogo"]([_v(vc=1000000.0, vcum=-20000.0)])
        assert ri["verdetto"] == "PRESENTAZIONE_REGOLARE"
        assert ri["quota_rel"] == pytest.approx(0.02)

    def test_verdetto_anomalie(self):
        ri = _F["mh550_riepilogo"]([_v(vc=1000000.0, vcum=-20000.0,
                                       qo=0.0)])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert ri["n_anomalie"] == 1
        assert ri["var_pnl_tot"] == -20000.0
        assert ri["var_oci_tot"] == 0.0

    def test_verdetto_nessuna(self):
        ri = _F["mh550_riepilogo"]([_v(vc=0.0, sc=0.0)])
        assert ri["verdetto"] == "NESSUNA_PASSIVITA"
        assert ri["quota_rel"] == 0.0

    def test_soglia_boundary(self):
        ri = _F["mh550_riepilogo"]([_v(vc=1000.0, vcum=-100.0)], 0.1)
        assert ri["quota_rel"] == 0.1
        assert ri["verdetto"] == "PRESENTAZIONE_REGOLARE"

    def test_soglia_custom(self):
        demo = _F["mh550_demo"]()
        ri = _F["mh550_riepilogo"](demo, 0.02)
        assert ri["verdetto"] == "OWN_CREDIT_RILEVANTE"
        ri = _F["mh550_riepilogo"](demo, 0.10)
        assert ri["verdetto"] == "PRESENTAZIONE_REGOLARE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh550_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh550_riepilogo"]("non lista")
        for bad in (0, 1, -0.1, 1.5, math.nan, math.inf, True, "x",
                    None):
            with pytest.raises(ValueError):
                _F["mh550_riepilogo"]([_v()], bad)


class TestW550Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_titolo_550_presente(self):
        assert self._src().count(TITLE550) == 3

    def test_counts_550(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 787
        assert TITLE550 in titoli

    def test_ui_indentata(self):
        assert "    with tab550:" in self._src()

    def test_dvar_line(self):
        assert "tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787 = st.tabs([" in self._src()

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st550_" in ln]
        # le f-string st550_id_{_i550} generano istanze a runtime: la base
        # e' fino al suffisso numerico; csv1/csv2 sono chiavi distinte
        basi = [re.search(r"st550_[a-z]+\d*", ln).group(0)
                for ln in righe]
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
