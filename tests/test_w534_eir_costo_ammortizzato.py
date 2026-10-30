"""Test tab534 '📐📊 Tasso di interesse effettivo (IFRS 9 5.4.1)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh534_num", "mh534_pct", "mh534_str", "mh534_int1",
           "mh534_strumento", "mh534_eir_periodale", "mh534_piano",
           "mh534_riepilogo")

TITLE534 = "📐📊 Tasso di interesse effettivo (IFRS 9 5.4.1)"
TITLE533 = "📉⏳ ECL a 3 stadi (IFRS 9 5.5)"


def _s(cid="S-1", tipo="prestito", freq="mensile", imp=100000.0, fee=0.0,
       rata=10000.0, nom=0.0, per=12, d="x"):
    return {"id": cid, "tipo": tipo, "frequenza": freq,
            "importo_finanziato_eur": imp, "costi_transazione_eur": fee,
            "rata_periodica_eur": rata, "tasso_nominale_annuo_pct": nom,
            "n_periodi": per, "descrizione": d}


class TestW534Validatori:
    def test_num_ok(self):
        assert _F["mh534_num"](2, "x") == 2.0
        assert _F["mh534_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh534_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh534_pct"](0.0, "x") == 0.0
        assert _F["mh534_pct"](100.0, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "50", None):
            with pytest.raises(ValueError):
                _F["mh534_pct"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh534_str"](bad, "x")

    def test_int1_ok(self):
        assert _F["mh534_int1"](1, "x") == 1
        assert _F["mh534_int1"](24, "x") == 24

    def test_int1_ko(self):
        for bad in (0, -1, 1.5, True, "3", None):
            with pytest.raises(ValueError):
                _F["mh534_int1"](bad, "x")


class TestW534Strumento:
    def test_ok(self):
        e = _F["mh534_strumento"](_s(cid=" S-1 "))
        assert e["id"] == "S-1"
        assert e["importo_netto_eur"] == 100000.0
        assert e["periodi_annuo"] == 12

    def test_fee_e_periodi_annuo(self):
        e = _F["mh534_strumento"](_s(fee=4000.0, freq="trimestrale",
                                    imp=200000.0, rata=9000.0, per=24))
        assert e["importo_netto_eur"] == 204000.0
        assert e["periodi_annuo"] == 4

    def test_chiave_mancante(self):
        v = _s()
        del v["rata_periodica_eur"]
        with pytest.raises(ValueError):
            _F["mh534_strumento"](v)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh534_strumento"]("no")
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(tipo="future"))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(freq="settimanale"))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(imp=0.0))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(fee=-1.0))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(rata=0.0))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(nom=100.1))
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(per=0))

    def test_flussi_insufficienti(self):
        with pytest.raises(ValueError):
            _F["mh534_strumento"](_s(imp=100000.0, rata=1000.0, per=12))


class TestW534Eir:
    def test_zero_exact(self):
        r = _F["mh534_eir_periodale"](
            _s(imp=120000.0, rata=10000.0, per=12))
        assert r == 0.0

    def test_annuity_nominale(self):
        # rata = rendita al 6% annuo capitalizzato mensile
        i = 0.06 / 12
        rata = 100000.0 * i / (1.0 - (1.0 + i) ** -12)
        r = _F["mh534_eir_periodale"](
            _s(imp=100000.0, rata=rata, per=12, nom=6.0))
        assert r == pytest.approx(0.005, rel=1e-9)

    def test_demo1_eir(self):
        r = _F["mh534_eir_periodale"](
            _s(imp=200000.0, fee=4000.0, rata=9000.0, per=24,
               freq="trimestrale"))
        assert r == pytest.approx(0.00462412175737958, rel=1e-9)
        assert (1.0 + r) ** 4 - 1.0 == pytest.approx(
            0.018625178000063025, rel=1e-9)

    def test_demo2_eir(self):
        r = _F["mh534_eir_periodale"](
            _s(imp=60000.0, rata=10500.0, per=6))
        assert r == pytest.approx(0.014120733923192633, rel=1e-9)


class TestW534Piano:
    def test_chiusura_e_totali(self):
        p = _F["mh534_piano"](_s(imp=200000.0, fee=4000.0, rata=9000.0,
                                 per=24, freq="trimestrale", nom=1.5))
        assert p["chiusura_ok"] is True
        assert p["interessi_totali_eur"] == pytest.approx(
            12000.0, rel=1e-9)
        assert len(p["righe"]) == 24
        assert p["righe"][0]["saldo_iniziale_eur"] == 204000.0
        assert p["righe"][-1]["saldo_finale_eur"] == pytest.approx(
            0.0, abs=1e-4)
        assert p["eir_annuo_pct"] == pytest.approx(1.8625178000063025,
                                                   rel=1e-9)

    def test_esito_sopra(self):
        p = _F["mh534_piano"](_s(imp=200000.0, fee=4000.0, rata=9000.0,
                                 per=24, freq="trimestrale", nom=1.5))
        assert p["esito"] == "SOPRA_NOMINALE"
        assert p["spread_vs_nominale_pct"] == pytest.approx(
            0.3625178000063025, rel=1e-9)

    def test_esito_allineato_zero(self):
        p = _F["mh534_piano"](_s(imp=120000.0, rata=10000.0, per=12,
                                 nom=0.0))
        assert p["eir_annuo_pct"] == 0.0
        assert p["esito"] == "ALLINEATO"
        assert p["interessi_totali_eur"] == pytest.approx(0.0, abs=1e-9)


class TestW534Riepilogo:
    def test_verdetto_misto(self):
        rows = [
            _s(cid="FIN-PPA-001", freq="trimestrale", imp=200000.0,
               fee=4000.0, rata=9000.0, nom=1.5, per=24,
               d="prestito FV"),
            _s(cid="CRED-EL-002", tipo="credito_commerciale",
               imp=60000.0, rata=10500.0, nom=0.0, per=6, d="credito"),
            _s(cid="VEND-EL-003", tipo="credito_commerciale",
               imp=120000.0, rata=10000.0, nom=0.0, per=12, d="vendor"),
        ]
        out = _F["mh534_riepilogo"](rows)
        esiti = [r["esito"] for r in out["righe"]]
        assert esiti == ["SOPRA_NOMINALE", "SOPRA_NOMINALE", "ALLINEATO"]
        t = out["totali"]
        assert t["verdetto"] == "MISTO"
        assert t["n_strumenti"] == 3
        assert t["importo_netto_totale_eur"] == 384000.0
        assert t["interessi_totali_eur"] == pytest.approx(
            12000.0 + 3000.0, rel=1e-9)
        assert (t["n_sopra"], t["n_allineati"], t["n_sotto"]) == (2, 1, 0)
        assert t["eir_medio_annuo_pct"] == pytest.approx(
            (1.8625178000063025 * 204000.0
             + 18.324845111908484 * 60000.0) / 384000.0, rel=1e-9)

    def test_tutti_sopra(self):
        rows = [_s(cid="a", imp=200000.0, fee=4000.0, rata=9000.0,
                   per=24, freq="trimestrale", nom=1.5),
                _s(cid="b", imp=60000.0, rata=10500.0, per=6, nom=0.0)]
        t = _F["mh534_riepilogo"](rows)["totali"]
        assert t["verdetto"] == "TUTTI_SOPRA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh534_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh534_riepilogo"]("no")
        with pytest.raises(ValueError):
            _F["mh534_riepilogo"]([_s(cid="dup"), _s(cid="dup")])


class TestW534Registry:
    def test_titolo_534_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE534) == 3

    def test_registry_tab_count_534(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 823
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 823

    def test_tab534_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823 = st.tabs([" in src
        assert "with tab534:" in src

    def test_chiavi_st534_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st534_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
