"""Test tab533 '📉⏳ ECL a 3 stadi (IFRS 9 5.5)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh533_num", "mh533_pct", "mh533_str", "mh533_bool",
           "mh533_int0", "mh533_esposizione", "mh533_stadio",
           "mh533_ecl", "mh533_riepilogo")

TITLE533 = "📉⏳ ECL a 3 stadi (IFRS 9 5.5)"
TITLE532 = "🧾💸 SPPI test (IFRS 9 4.1.2(b))"


def _e(cid="E-1", tipo="prestito", ead=1000000.0, pd12=1.0, pdlt=5.0,
       lgd=45.0, eir=5.0, vita=3.0, gg=0, dg=0, wl=False, sem=False,
       d="x"):
    return {"id": cid, "tipo": tipo, "ead_eur": ead, "pd_12m_pct": pd12,
            "pd_lifetime_pct": pdlt, "lgd_pct": lgd, "eir_pct": eir,
            "vita_residua_anni": vita, "giorni_scaduto": gg,
            "downgrade_notch": dg, "watchlist": wl,
            "approccio_semplificato": sem, "descrizione": d}


class TestW533Validatori:
    def test_num_ok(self):
        assert _F["mh533_num"](2, "x") == 2.0
        assert _F["mh533_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh533_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh533_pct"](0.0, "x") == 0.0
        assert _F["mh533_pct"](100.0, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "50", None):
            with pytest.raises(ValueError):
                _F["mh533_pct"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh533_str"](bad, "x")

    def test_bool_ko(self):
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh533_bool"](bad, "x")

    def test_int0_ok(self):
        assert _F["mh533_int0"](0, "x") == 0
        assert _F["mh533_int0"](90, "x") == 90

    def test_int0_ko(self):
        for bad in (-1, 1.5, True, "3", None):
            with pytest.raises(ValueError):
                _F["mh533_int0"](bad, "x")


class TestW533Esposizione:
    def test_ok(self):
        e = _F["mh533_esposizione"](_e(cid=" E-1 "))
        assert e["id"] == "E-1"
        assert e["ead_eur"] == 1000000.0
        assert e["giorni_scaduto"] == 0

    def test_chiave_mancante(self):
        v = _e()
        del v["lgd_pct"]
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](v)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh533_esposizione"]("no")
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(tipo="future"))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(ead=-5.0))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(pd12=101.0))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(pd12=5.0, pdlt=4.9))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(eir=100.0))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(vita=0.0))
        with pytest.raises(ValueError):
            _F["mh533_esposizione"](_e(gg=-1))

    def test_pdlt_uguale_pd12_ok(self):
        e = _F["mh533_esposizione"](_e(pd12=3.0, pdlt=3.0))
        assert e["pd_lifetime_pct"] == 3.0


class TestW533Stadio:
    def test_stage1(self):
        st, te, _ = _F["mh533_stadio"](_e())
        assert (st, te) == ("STAGE_1", "ECL_12_MESI")

    def test_stage2_scaduto(self):
        st, te, _ = _F["mh533_stadio"](_e(gg=31))
        assert (st, te) == ("STAGE_2", "ECL_LIFETIME")

    def test_stage1_boundary_30gg(self):
        st, _, _ = _F["mh533_stadio"](_e(gg=30))
        assert st == "STAGE_1"

    def test_stage2_downgrade(self):
        st, _, _ = _F["mh533_stadio"](_e(dg=2))
        assert st == "STAGE_2"

    def test_stage1_downgrade_1(self):
        st, _, _ = _F["mh533_stadio"](_e(dg=1))
        assert st == "STAGE_1"

    def test_stage2_watchlist(self):
        st, _, _ = _F["mh533_stadio"](_e(wl=True))
        assert st == "STAGE_2"

    def test_stage3_boundary_90gg(self):
        st, _, _ = _F["mh533_stadio"](_e(gg=90))
        assert st == "STAGE_3"
        st2, _, _ = _F["mh533_stadio"](_e(gg=89))
        assert st2 == "STAGE_2"

    def test_stage2_semplificato(self):
        st, te, _ = _F["mh533_stadio"](_e(sem=True))
        assert (st, te) == ("STAGE_2", "ECL_LIFETIME")


class TestW533Ecl:
    def test_stage1_math(self):
        r = _F["mh533_ecl"](_e(pd12=2.0, pdlt=10.0, lgd=50.0,
                               eir=5.0, vita=3.0))
        assert r["ecl_eur"] == pytest.approx(9523.809523809523,
                                             rel=1e-9)
        assert r["stadio"] == "STAGE_1"
        assert r["coverage_pct"] == pytest.approx(0.9523809523809523,
                                                  rel=1e-9)

    def test_lifetime_math(self):
        r = _F["mh533_ecl"](_e(pd12=2.0, pdlt=10.0, lgd=50.0,
                               eir=5.0, vita=3.0, gg=45))
        assert r["stadio"] == "STAGE_2"
        assert r["ecl_eur"] == pytest.approx(43191.8799265738, rel=1e-9)

    def test_ecl_eir_zero(self):
        r = _F["mh533_ecl"](_e(pd12=2.0, pdlt=2.0, lgd=50.0, eir=0.0))
        assert r["ecl_eur"] == pytest.approx(10000.0, rel=1e-12)

    def test_ead_zero(self):
        r = _F["mh533_ecl"](_e(ead=0.0))
        assert r["ecl_eur"] == 0.0
        assert r["coverage_pct"] == 0.0

    def test_lgd_zero(self):
        r = _F["mh533_ecl"](_e(lgd=0.0))
        assert r["ecl_eur"] == 0.0


class TestW533Riepilogo:
    def test_verdetti(self):
        assert _F["mh533_riepilogo"]([_e(cid="a")])["totali"][
            "verdetto"] == "TUTTO_STAGE_1"
        assert _F["mh533_riepilogo"]([_e(cid="a"), _e(cid="b", gg=40)]
                                     )["totali"]["verdetto"] == "SICR_PRESENTE"
        assert _F["mh533_riepilogo"]([_e(cid="a"), _e(cid="b", gg=40),
                                      _e(cid="c", gg=120)]
                                     )["totali"]["verdetto"] == \
            "CREDIT_IMPAIRED"

    def test_totali(self):
        t = _F["mh533_riepilogo"]([_e(cid="a", ead=1000.0),
                                   _e(cid="b", ead=2000.0, gg=45)]
                                  )["totali"]
        assert t["n_esposizioni"] == 2
        assert (t["n_stage_1"], t["n_stage_2"], t["n_stage_3"]) == (1, 1, 0)
        assert t["ead_totale_eur"] == 3000.0
        assert t["ecl_totale_eur"] == pytest.approx(
            t["ecl_stage_1_eur"] + t["ecl_stage_2_eur"], rel=1e-12)
        assert t["coverage_media_pct"] == pytest.approx(
            t["ecl_totale_eur"] / 3000.0 * 100.0, rel=1e-12)

    def test_demo_defaults(self):
        rows = [
            _e(cid="PPA-SOL-001", tipo="receivable_ppa", ead=500000.0,
               pd12=0.8, pdlt=4.5, lgd=40.0, eir=3.5, vita=5.0),
            _e(cid="TRD-GAS-002", tipo="credito_commerciale",
               ead=1200000.0, pd12=2.0, pdlt=12.0, lgd=55.0, eir=4.0,
               vita=2.0, gg=45, dg=1),
            _e(cid="RET-EL-003", tipo="credito_commerciale", ead=300000.0,
               pd12=5.0, pdlt=35.0, lgd=70.0, eir=5.0, vita=1.0,
               gg=120, dg=3, wl=True),
        ]
        out = _F["mh533_riepilogo"](rows)
        stadi = [r["stadio"] for r in out["righe"]]
        assert stadi == ["STAGE_1", "STAGE_2", "STAGE_3"]
        assert out["totali"]["verdetto"] == "CREDIT_IMPAIRED"
        assert out["righe"][0]["ecl_eur"] == pytest.approx(
            1545.8937198067633, rel=1e-9)
        assert out["righe"][1]["ecl_eur"] == pytest.approx(
            73224.85207100591, rel=1e-9)
        assert out["righe"][2]["ecl_eur"] == pytest.approx(70000.0,
                                                           rel=1e-12)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh533_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh533_riepilogo"]("no")
        with pytest.raises(ValueError):
            _F["mh533_riepilogo"]([_e(cid="dup"), _e(cid="dup")])


class TestW533Registry:
    def test_titolo_533_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE533) == 3

    def test_registry_tab_count_533(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 770
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 770

    def test_tab533_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770 = st.tabs([" in src
        assert "with tab533:" in src

    def test_chiavi_st533_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st533_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
