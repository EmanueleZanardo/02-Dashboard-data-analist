"""Test tab574 "Inefficacia a P&L per tipo di copertura (IFRS 7.24G)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh574_num", "mh574_str", "mh574_tipo", "mh574_rischio",
           "mh574_relazione", "mh574_demo", "mh574_riepilogo")

TITLE574 = "💶📊 Inefficacia a P&L per tipo di copertura (IFRS 7.24G)"


def _r(rid="HED-1", descrizione="relazione", tipo="FAIR_VALUE",
       rischio="COMMODITY", pl=-450_000.0, gs=100_000.0, gc=-550_000.0):
    return _F["mh574_relazione"](rid, descrizione, tipo, rischio, pl,
                                 gain_strumento=gs, gain_coperto=gc)


class TestW574Validatori:
    def test_num_ok(self):
        assert _F["mh574_num"](2, "x") == 2.0
        assert _F["mh574_num"](-3.5, "x") == -3.5
        assert _F["mh574_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh574_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh574_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh574_str"](bad, "x")

    def test_tipo_ok(self):
        assert _F["mh574_tipo"]("fair_value") == "FAIR_VALUE"
        assert _F["mh574_tipo"]("Cash Flow") == "CASH_FLOW"
        assert _F["mh574_tipo"]("NET_INVESTMENT") == "NET_INVESTMENT"

    def test_tipo_ko(self):
        for bad in ("FV", "", None, "cashflow"):
            with pytest.raises(ValueError):
                _F["mh574_tipo"](bad)

    def test_rischio_ok(self):
        assert _F["mh574_rischio"]("fx") == "FX"
        assert _F["mh574_rischio"]("Commodity") == "COMMODITY"
        assert _F["mh574_rischio"]("TASSO") == "TASSO"

    def test_rischio_ko(self):
        for bad in ("equity", "", None):
            with pytest.raises(ValueError):
                _F["mh574_rischio"](bad)


class TestW574Relazione:
    def test_fv_hand_computed(self):
        r = _r()
        assert r["id"] == "HED-1"
        assert r["tipo"] == "FAIR_VALUE"
        assert r["tipo_label"] == "Fair value hedges"
        assert r["rischio_label"] == "Commodity"
        assert r["inefficacia_pl"] == pytest.approx(-450_000.0)
        assert r["completa"] is True
        assert r["anomalie"] == []

    def test_fv_somma_tolleranza_ok(self):
        # scarto 0.005 EUR entro la tolleranza 0.01 -> nessuna anomalia
        r = _r(pl=-450_000.005)
        assert r["completa"] is True

    def test_fv_componenti_mancanti_anomalia(self):
        r = _r(gs=None, gc=None)
        assert r["completa"] is False
        assert any("non dichiarate" in a for a in r["anomalie"])

    def test_fv_incoerenza_anomalia(self):
        r = _r(pl=-450_000.0, gs=100_000.0, gc=-400_000.0)
        assert r["completa"] is False
        assert any("incoerente" in a for a in r["anomalie"])

    def test_cfh_ok(self):
        r = _F["mh574_relazione"]("HED-CF", "forward", "CASH_FLOW", "FX",
                                  -80_000.0)
        assert r["completa"] is True
        assert r["gain_strumento"] is None
        assert r["tipo_label"] == "Cash flow hedges"

    def test_cfh_componenti_fv_anomalia(self):
        r = _F["mh574_relazione"]("HED-CF", "forward", "CASH_FLOW", "FX",
                                  -80_000.0, gain_strumento=10.0,
                                  gain_coperto=-5.0)
        assert r["completa"] is False
        assert any("non attese" in a for a in r["anomalie"])

    def test_ni_ok(self):
        r = _F["mh574_relazione"]("HED-NI", "nib", "NET_INVESTMENT",
                                  "FX", 12_000.0)
        assert r["completa"] is True
        assert r["tipo_label"] == "Net investment hedges"

    def test_str_strip(self):
        r = _r(rid="  HED-X ", descrizione=" rel ")
        assert r["id"] == "HED-X"
        assert r["descrizione"] == "rel"

    def test_pl_non_numero_ko(self):
        with pytest.raises(ValueError):
            _F["mh574_relazione"]("HED-1", "r", "FAIR_VALUE", "COMMODITY",
                                  "x", gain_strumento=0.0,
                                  gain_coperto=0.0)


class TestW574Riepilogo:
    def test_demo_inefficacia_significativa(self):
        r = _F["mh574_riepilogo"](_F["mh574_demo"]())
        # tot = +5k - 1450k - 18k = -1_463_000
        assert r["inefficacia_totale"] == pytest.approx(-1_463_000.0)
        assert r["inefficacia_assoluta_totale"] == pytest.approx(
            1_463_000.0)
        assert r["n_relazioni"] == 3
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "INEFFICACIA_SIGNIFICATIVA"
        assert r["peggiore_id"] == "HED-002"
        assert r["totale_per_tipo"]["Fair value hedges"] == \
            pytest.approx(-13_000.0)
        assert r["totale_per_tipo"]["Cash flow hedges"] == \
            pytest.approx(-1_450_000.0)
        assert r["totale_per_tipo"]["Net investment hedges"] == \
            pytest.approx(0.0)

    def test_inefficacia_gestibile(self):
        r = _F["mh574_riepilogo"]([_r()], soglia_eur=1_000_000.0)
        assert r["verdetto"] == "INEFFICACIA_GESTIBILE"

    def test_nessuna_relazione(self):
        r = _F["mh574_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_RELAZIONE"
        assert r["n_relazioni"] == 0
        assert r["totale_per_tipo"]["Fair value hedges"] == 0.0

    def test_duplicati_anomalia(self):
        r = _F["mh574_riepilogo"]([_r(rid="DUP"), _r(rid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"] for x in r["analizzate"])

    def test_anomalie_hanno_priorita(self):
        # sopra soglia MA con anomalia -> ANOMALIE_DA_VERIFICARE
        r = _F["mh574_riepilogo"](
            [_r(pl=-2_000_000.0, gs=100_000.0, gc=-550_000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh574_riepilogo"]([_r()], soglia_eur=0.0)

    def test_peggiore_none_se_tutto_zero(self):
        r = _F["mh574_riepilogo"](
            [_F["mh574_relazione"]("HED-0", "zero", "CASH_FLOW",
                                   "TASSO", 0.0)])
        assert r["peggiore_id"] is None
        assert r["verdetto"] == "INEFFICACIA_GESTIBILE"


class TestW574Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE574}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 806
        assert TITLE574 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806 = st.tabs([" in src
        assert "with tab574:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st574_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
