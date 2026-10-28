"""Test tab579 "Rendita da congestione (congestion rent)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh579_num", "mh579_str", "mh579_direzione",
           "mh579_frontiera", "mh579_demo", "mh579_riepilogo")

TITLE579 = "🔌💰 Rendita da congestione (congestion rent)"


def _f(fid="CR-1", descrizione="frontiera", frontiera="CH-IT",
       direzione="ESPORTAZIONE", mw=200.0, ore=1000.0, fc=0.8,
       spread=17.0, costo=500_000.0):
    return _F["mh579_frontiera"](fid, descrizione, frontiera,
                                 direzione, mw, ore, fc, spread,
                                 costo)


class TestW579Validatori:
    def test_num_ok(self):
        assert _F["mh579_num"](2, "x") == 2.0
        assert _F["mh579_num"](-3.5, "x") == -3.5
        assert _F["mh579_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh579_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh579_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh579_str"](bad, "x")

    def test_direzione_ok(self):
        assert _F["mh579_direzione"]("esportazione") == "ESPORTAZIONE"
        assert _F["mh579_direzione"]("IMPORTAZIONE") == "IMPORTAZIONE"

    def test_direzione_ko(self):
        for bad in ("MKT", "", None, "export"):
            with pytest.raises(ValueError):
                _F["mh579_direzione"](bad)


class TestW579Frontiera:
    def test_hand_computed(self):
        c = _f()
        # 200 * 1000 * 0.8 = 160000 MWh; 17 * 160000 = 2720000
        assert c["energia_mwh"] == pytest.approx(160_000.0)
        assert c["ricavo_lordo_eur"] == pytest.approx(2_720_000.0)
        # 2720000 - 500000 = 2220000; 2220000 / 160000 = 13.875
        assert c["rendita_netta_eur"] == pytest.approx(2_220_000.0)
        assert c["rendita_eur_mwh"] == pytest.approx(13.875)
        assert c["roi"] == pytest.approx(4.44)
        assert c["completa"] is True
        assert c["anomalie"] == []

    def test_hand_computed_rendita_negativa(self):
        c = _f(fid="CR-2", mw=150.0, ore=800.0, fc=0.9, spread=1.5,
               costo=300_000.0)
        # 150 * 800 * 0.9 = 108000; 1.5 * 108000 = 162000
        assert c["energia_mwh"] == pytest.approx(108_000.0)
        assert c["ricavo_lordo_eur"] == pytest.approx(162_000.0)
        # 162000 - 300000 = -138000; -138000 / 108000
        assert c["rendita_netta_eur"] == pytest.approx(-138_000.0)
        assert c["rendita_eur_mwh"] == pytest.approx(-138_000.0
                                                    / 108_000.0)
        assert c["roi"] == pytest.approx(-0.46)
        assert c["completa"] is True

    def test_spread_negativo_anomalia(self):
        c = _f(spread=-2.0)
        assert c["completa"] is False
        assert any("Spread" in a for a in c["anomalie"])
        assert c["ricavo_lordo_eur"] == pytest.approx(0.0)
        assert c["rendita_netta_eur"] == pytest.approx(-500_000.0)

    def test_anomalia_capacita(self):
        c = _f(mw=0.0)
        assert c["completa"] is False
        assert any("Capacita'" in a for a in c["anomalie"])
        assert c["energia_mwh"] == pytest.approx(0.0)

    def test_anomalia_ore(self):
        c = _f(ore=0.0)
        assert c["completa"] is False
        assert any("Ore" in a for a in c["anomalie"])

    def test_anomalia_fattore(self):
        for bad in (0.0, -0.1, 1.5):
            c = _f(fc=bad)
            assert c["completa"] is False
            assert any("Fattore" in a for a in c["anomalie"])

    def test_anomalia_costo_negativo(self):
        c = _f(costo=-100.0)
        assert c["completa"] is False
        assert any("Costo" in a for a in c["anomalie"])

    def test_fattore_uno_ok(self):
        c = _f(mw=100.0, ore=500.0, fc=1.0, spread=12.0,
               costo=180_000.0)
        assert c["energia_mwh"] == pytest.approx(50_000.0)
        assert c["rendita_netta_eur"] == pytest.approx(420_000.0)
        assert c["roi"] == pytest.approx(420_000.0 / 180_000.0)
        assert c["completa"] is True

    def test_roi_costo_zero(self):
        c = _f(costo=0.0)
        assert c["roi"] == pytest.approx(0.0)
        assert c["completa"] is True

    def test_ko_direzione_e_tipo(self):
        with pytest.raises(ValueError):
            _F["mh579_frontiera"]("X", "d", "CH-IT", "LONG", 100.0,
                                  100.0, 0.8, 10.0, 1000.0)
        with pytest.raises(ValueError):
            _F["mh579_frontiera"]("X", "d", "CH-IT", "ESPORTAZIONE",
                                  math.nan, 100.0, 0.8, 10.0,
                                  1000.0)

    def test_demo(self):
        d = _F["mh579_demo"]()
        assert len(d) == 3
        assert [x["id"] for x in d] == ["CR-001", "CR-002", "CR-003"]
        assert all(x["completa"] for x in d)


class TestW579Riepilogo:
    def test_vuoto(self):
        r = _F["mh579_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_FRONTIERA"
        assert r["n_frontiere"] == 0

    def test_demo_positiva(self):
        r = _F["mh579_riepilogo"](_F["mh579_demo"]())
        assert r["verdetto"] == "RENDITA_POSITIVA"
        assert r["n_frontiere"] == 3
        assert r["n_anomalie"] == 0
        # 2220000 - 138000 + 420000 = 2502000
        assert r["rendita_netta_totale"] == pytest.approx(
            2_502_000.0)
        assert r["costo_totale"] == pytest.approx(980_000.0)
        assert r["ricavo_lordo_totale"] == pytest.approx(
            3_482_000.0)
        assert r["energia_totale"] == pytest.approx(318_000.0)
        # 2502000 / 980000 ; 2502000 / 318000
        assert r["roi_medio"] == pytest.approx(2_502_000.0
                                               / 980_000.0)
        assert r["rendita_media_mwh"] == pytest.approx(
            2_502_000.0 / 318_000.0)
        assert r["n_esportazioni"] == 2
        assert r["n_importazioni"] == 1

    def test_rendita_negativa(self):
        r = _F["mh579_riepilogo"]([_f(spread=1.0, costo=1_000_000.0)])
        # 1.0 * 160000 = 160000 - 1000000 = -840000
        assert r["rendita_netta_totale"] == pytest.approx(-840_000.0)
        assert r["verdetto"] == "RENDITA_NEGATIVA"

    def test_anomalie_hanno_priorita(self):
        bad = _f(spread=-5.0)
        r = _F["mh579_riepilogo"]([bad])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_id_duplicato(self):
        r = _F["mh579_riepilogo"]([_f(), _f()])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2


class TestW579Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE579}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 770
        assert TITLE579 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770 = st.tabs([" in src
        assert "with tab579:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st579_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
