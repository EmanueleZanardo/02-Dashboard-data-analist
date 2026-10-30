"""Test tab584 "Convertitore unita' di misura energia e prezzi": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh584_num", "mh584_str", "mh584_categoria",
           "mh584_unita_energia", "mh584_unita_prezzo", "mh584_pcs",
           "mh584_fx", "mh584_conversione", "mh584_demo",
           "mh584_riepilogo")

TITLE584 = "🔄📐 Convertitore unità di misura energia e prezzi"


def _c(sid="C-1", descrizione="voce", categoria="ENERGIA", valore=1.0,
       da="MWH", a="KWH", **kw):
    return _F["mh584_conversione"](sid, descrizione, categoria, valore,
                                   da, a, **kw)


class TestW584Validatori:
    def test_num_ok(self):
        assert _F["mh584_num"](2, "x") == 2.0
        assert _F["mh584_num"](-3.5, "x") == -3.5
        assert _F["mh584_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh584_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh584_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh584_str"](bad, "x")

    def test_categoria_ok(self):
        assert _F["mh584_categoria"]("energia") == "ENERGIA"
        assert _F["mh584_categoria"]("PREZZO") == "PREZZO"

    def test_categoria_ko(self):
        for bad in ("GAS", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh584_categoria"](bad)

    def test_unita_energia_ok(self):
        for u in ("MWH", "KWH", "GWH", "MMBTU", "THERM", "SM3", "TOE",
                  "GJ", "GCAL", "mmbtu"):
            assert _F["mh584_unita_energia"](u) == u.upper()

    def test_unita_energia_ko(self):
        for bad in ("EUR_MWH", "KG", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh584_unita_energia"](bad)

    def test_unita_prezzo_ok(self):
        for u in ("EUR_MWH", "CEUR_KWH", "EUR_SM3", "USD_MMBTU",
                  "P_THERM", "EUR_GJ", "p_therm"):
            assert _F["mh584_unita_prezzo"](u) == u.upper()

    def test_unita_prezzo_ko(self):
        for bad in ("MWH", "EUR_KWH", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh584_unita_prezzo"](bad)

    def test_pcs_ok(self):
        assert _F["mh584_pcs"](10.55) == 10.55

    def test_pcs_ko(self):
        for bad in (0.0, -1.0, "x", None, True):
            with pytest.raises(ValueError):
                _F["mh584_pcs"](bad)

    def test_fx_ko(self):
        for bad in (0.0, -1.5, "x", None):
            with pytest.raises(ValueError):
                _F["mh584_fx"](bad, "cambio_eurusd")


class TestW584Conversioni:
    def test_energia_hand_mmbtu_mwh(self):
        c = _c(da="MMBTU", a="MWH", valore=2500.0)
        assert c["convertito"] == pytest.approx(2500.0 * 0.2930710701722222)
        assert c["fattore"] == pytest.approx(0.2930710701722222)
        assert c["completa"] and not c["anomalie"]

    def test_energia_inversa_mwh_mmbtu(self):
        c = _c(da="MWH", a="MMBTU", valore=1.0)
        assert c["convertito"] == pytest.approx(3.412141633127945)
        assert c["fattore"] == pytest.approx(3.412141633127945)

    def test_energia_sm3_pcs(self):
        c = _c(da="SM3", a="MWH", valore=1000.0, pcs=10.55)
        assert c["convertito"] == pytest.approx(10.55)
        c2 = _c(da="SM3", a="MWH", valore=1000.0, pcs=11.0)
        assert c2["convertito"] == pytest.approx(11.0)

    def test_energia_unita_varie(self):
        assert _c(da="KWH", a="MWH", valore=1000.0)["convertito"] == \
            pytest.approx(1.0)
        assert _c(da="GWH", a="MWH", valore=2.0)["convertito"] == \
            pytest.approx(2000.0)
        assert _c(da="TOE", a="MWH", valore=1.0)["convertito"] == \
            pytest.approx(11.63)
        assert _c(da="GJ", a="MWH", valore=3.6)["convertito"] == \
            pytest.approx(1.0)
        assert _c(da="GCAL", a="MWH", valore=1.0)["convertito"] == \
            pytest.approx(1.163)
        assert _c(da="THERM", a="KWH", valore=10.0)["convertito"] == \
            pytest.approx(293.0710701722222)

    def test_prezzo_hand_eur_sm3(self):
        c = _c(categoria="PREZZO", valore=1.25, da="EUR_SM3",
               a="EUR_MWH")
        assert c["convertito"] == pytest.approx(1250.0 / 10.55)
        assert c["unita_base"] == "EUR/MWh"

    def test_prezzo_hand_usd_mmbtu(self):
        c = _c(categoria="PREZZO", valore=11.50, da="USD_MMBTU",
               a="EUR_MWH", cambio_eurusd=1.10)
        assert c["convertito"] == pytest.approx(
            11.50 * 3.412141633127945 / 1.10)

    def test_prezzo_unita_varie(self):
        assert _c(categoria="PREZZO", valore=22.0, da="CEUR_KWH",
                  a="EUR_MWH")["convertito"] == pytest.approx(220.0)
        assert _c(categoria="PREZZO", valore=36.0, da="EUR_GJ",
                  a="EUR_MWH")["convertito"] == pytest.approx(129.6)
        assert _c(categoria="PREZZO", valore=100.0, da="P_THERM",
                  a="EUR_MWH",
                  cambio_gbpeur=1.17)["convertito"] == pytest.approx(
            100.0 * 1.17 * 0.3412141633127945)
        c = _c(categoria="PREZZO", valore=118.48341232227488,
               da="EUR_MWH", a="EUR_SM3")
        assert c["convertito"] == pytest.approx(1.25)

    def test_anomalia_valore_nullo(self):
        c = _c(valore=0.0, da="MWH", a="KWH")
        assert not c["completa"] and c["convertito"] is None
        assert any("nullo" in a for a in c["anomalie"])

    def test_anomalia_unita_identica(self):
        c = _c(valore=5.0, da="MWH", a="MWH")
        assert not c["completa"] and c["fattore"] is None
        assert len(c["anomalie"]) == 1

    def test_unita_categoria_sbagliata_ko(self):
        with pytest.raises(ValueError):
            _c(categoria="ENERGIA", da="EUR_MWH", a="MWH")
        with pytest.raises(ValueError):
            _c(categoria="PREZZO", da="MWH", a="EUR_MWH")

    def test_pcs_fx_ko(self):
        with pytest.raises(ValueError):
            _c(da="SM3", a="MWH", valore=1.0, pcs=0.0)
        with pytest.raises(ValueError):
            _c(categoria="PREZZO", da="USD_MMBTU", a="EUR_MWH",
               valore=1.0, cambio_eurusd=0.0)
        with pytest.raises(ValueError):
            _c(categoria="PREZZO", da="P_THERM", a="EUR_MWH",
               valore=1.0, cambio_gbpeur=-2.0)

    def test_demo(self):
        d = _F["mh584_demo"]()
        assert len(d) == 3
        assert all(c["completa"] for c in d)
        assert d[0]["convertito"] == pytest.approx(1250.0 / 10.55)
        assert d[1]["convertito"] == pytest.approx(
            11.50 * 3.412141633127945 / 1.10)
        assert d[2]["convertito"] == pytest.approx(
            2500.0 * 0.2930710701722222)


class TestW584Riepilogo:
    def test_vuoto(self):
        r = _F["mh584_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_CONVERSIONE"
        assert r["n_conversioni"] == 0

    def test_ok(self):
        r = _F["mh584_riepilogo"](_F["mh584_demo"]())
        assert r["verdetto"] == "CONVERSIONI_OK"
        assert (r["n_conversioni"], r["n_completi"],
                r["n_anomalie"]) == (3, 3, 0)

    def test_duplicati(self):
        r = _F["mh584_riepilogo"]([_c("DUP"), _c("DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert r["n_completi"] == 0

    def test_precedenza_anomalie(self):
        r = _F["mh584_riepilogo"](
            [_c("A", valore=1.0), _c("B", valore=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert (r["n_completi"], r["n_anomalie"]) == (1, 1)


class TestW584Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE584}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 808
        assert TITLE584 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808 = st.tabs([" in src
        assert "with tab584:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st584_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
