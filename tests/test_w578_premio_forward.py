"""Test tab578 "Premio di rischio forward (ex-post)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh578_num", "mh578_str", "mh578_lato",
           "mh578_contratto", "mh578_demo", "mh578_riepilogo")

TITLE578 = "📊⚡ Premio di rischio forward (ex-post)"


def _c(cid="FWD-1", descrizione="contratto", lato="ACQUISTO",
       fw=95.0, spot=88.5, qty=350_400.0, periodo="Cal-25"):
    return _F["mh578_contratto"](cid, descrizione, lato, fw, spot,
                                 qty, periodo)


class TestW578Validatori:
    def test_num_ok(self):
        assert _F["mh578_num"](2, "x") == 2.0
        assert _F["mh578_num"](-3.5, "x") == -3.5
        assert _F["mh578_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh578_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh578_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh578_str"](bad, "x")

    def test_lato_ok(self):
        assert _F["mh578_lato"]("acquisto") == "ACQUISTO"
        assert _F["mh578_lato"]("VENDITA") == "VENDITA"

    def test_lato_ko(self):
        for bad in ("MKT", "", None, "acquisti"):
            with pytest.raises(ValueError):
                _F["mh578_lato"](bad)


class TestW578Contratto:
    def test_hand_computed(self):
        c = _c()
        # 95.0 - 88.5 = 6.5 EUR/MWh; 6.5 * 350400 = 2277600.0
        assert c["premio_mwh"] == pytest.approx(6.5)
        assert c["premio_totale"] == pytest.approx(2_277_600.0)
        assert c["premio_pct"] == pytest.approx(6.5 / 95.0 * 100.0)
        assert c["completa"] is True
        assert c["anomalie"] == []

    def test_spot_negativo_ok(self):
        c = _c(spot=-10.0)
        assert c["premio_mwh"] == pytest.approx(105.0)
        assert c["completa"] is True

    def test_premio_negativo(self):
        c = _c(fw=38.0, spot=41.5, qty=50_000.0)
        assert c["premio_mwh"] == pytest.approx(-3.5)
        assert c["premio_totale"] == pytest.approx(-175_000.0)

    def test_anomalia_quantita(self):
        c = _c(qty=0.0)
        assert c["completa"] is False
        assert any("Quantita'" in a for a in c["anomalie"])

    def test_anomalia_forward(self):
        c = _c(fw=-5.0)
        assert c["completa"] is False
        assert any("Prezzo forward" in a for a in c["anomalie"])

    def test_anomalia_periodo(self):
        c = _c(periodo="  ")
        assert c["completa"] is False
        assert any("Periodo" in a for a in c["anomalie"])

    def test_ko_lato_e_tipo(self):
        with pytest.raises(ValueError):
            _F["mh578_contratto"]("X", "d", "LONG", 95.0, 88.5,
                                  100.0, "Cal-25")
        with pytest.raises(ValueError):
            _F["mh578_contratto"]("X", "d", "ACQUISTO", math.nan,
                                  88.5, 100.0, "Cal-25")

    def test_demo(self):
        d = _F["mh578_demo"]()
        assert len(d) == 3
        assert [x["id"] for x in d] == ["FWD-401", "FWD-402",
                                       "FWD-403"]
        assert all(x["completa"] for x in d)


class TestW578Riepilogo:
    def test_vuoto(self):
        r = _F["mh578_riepilogo"]([])
        assert r["verdetto"] == "NESSUN_CONTRATTO"
        assert r["n_contratti"] == 0

    def test_demo_sfavorevole(self):
        r = _F["mh578_riepilogo"](_F["mh578_demo"]())
        assert r["verdetto"] == "PREMIO_SFAVOREVOLE"
        assert r["n_contratti"] == 3
        assert r["n_anomalie"] == 0
        # 2277600 - 175000 (acquisti) - 110400 (vendite) = 1992200.0
        assert r["costo_premio_netto"] == pytest.approx(1_992_200.0)
        assert r["premio_acquisti"] == pytest.approx(2_102_600.0)
        assert r["premio_vendite"] == pytest.approx(110_400.0)
        assert r["n_acquisti"] == 2
        assert r["n_vendite"] == 1
        # (2277600 + 110400 - 175000) / 422480
        assert r["quantita_totale"] == pytest.approx(422_480.0)
        assert r["premio_medio_ponderato"] == pytest.approx(
            2_213_000.0 / 422_480.0)

    def test_gestibile(self):
        r = _F["mh578_riepilogo"]([_c(fw=90.0, spot=88.5,
                                      qty=100.0)],
                                  soglia=1_000_000.0)
        assert r["verdetto"] == "PREMIO_GESTIBILE"
        assert r["costo_premio_netto"] == pytest.approx(150.0)

    def test_soglia_personalizzata(self):
        r = _F["mh578_riepilogo"]([_c(fw=90.0, spot=88.5,
                                      qty=100.0)],
                                  soglia=100.0)
        assert r["verdetto"] == "PREMIO_SFAVOREVOLE"

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh578_riepilogo"]([_c()], soglia=0.0)
        with pytest.raises(ValueError):
            _F["mh578_riepilogo"]([_c()], soglia="1")

    def test_duplicati_anomalia(self):
        r = _F["mh578_riepilogo"]([_c(cid="DUP"), _c(cid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"]
                   for x in r["analizzati"])

    def test_anomalie_hanno_priorita(self):
        bad = _c(qty=-1.0)
        r = _F["mh578_riepilogo"]([bad])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_vendita_favorevole_netto_negativo(self):
        # vendita sopra lo spot: premio positivo, netto negativo
        r = _F["mh578_riepilogo"]([_c(lato="VENDITA", fw=102.0,
                                      spot=97.0, qty=22_080.0)])
        assert r["costo_premio_netto"] == pytest.approx(-110_400.0)
        assert r["verdetto"] == "PREMIO_GESTIBILE"


class TestW578Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE578}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 817
        assert TITLE578 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817 = st.tabs([" in src
        assert "with tab578:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st578_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
