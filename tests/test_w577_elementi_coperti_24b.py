"""Test tab577 "Elementi coperti per categoria di rischio (IFRS 7.24B)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh577_num", "mh577_str", "mh577_rischio", "mh577_tipo",
           "mh577_unita", "mh577_item", "mh577_demo",
           "mh577_riepilogo")

TITLE577 = "📊📦 Elementi coperti per categoria di rischio (IFRS 7.24B)"


def _i(sid="HI-1", descrizione="elemento", rischio="COMMODITY",
       tipo="CASH_FLOW", att=800_000.0, pas=0.0,
       voce="Crediti commerciali", vv=-150_000.0,
       not_=30_000.0, un="MWH", adj=None):
    return _F["mh577_item"](sid, descrizione, rischio, tipo, att, pas,
                            voce, vv, nozionale_importo=not_,
                            nozionale_unita=un, adeguamento_fv=adj)


class TestW577Validatori:
    def test_num_ok(self):
        assert _F["mh577_num"](2, "x") == 2.0
        assert _F["mh577_num"](-3.5, "x") == -3.5
        assert _F["mh577_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh577_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh577_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh577_str"](bad, "x")

    def test_rischio_ok(self):
        assert _F["mh577_rischio"]("tasso") == "TASSO"
        assert _F["mh577_rischio"]("Commodity") == "COMMODITY"
        assert _F["mh577_rischio"]("FX") == "FX"
        assert _F["mh577_rischio"]("credito") == "CREDITO"
        assert _F["mh577_rischio"]("altro") == "ALTRO"

    def test_rischio_ko(self):
        for bad in ("MKT", "", None, "tassi"):
            with pytest.raises(ValueError):
                _F["mh577_rischio"](bad)

    def test_tipo_unita_ok(self):
        assert _F["mh577_tipo"]("cash flow") == "CASH_FLOW"
        assert _F["mh577_tipo"]("NET_INVESTMENT") == "NET_INVESTMENT"
        assert _F["mh577_unita"]("eur") == "EUR"
        assert _F["mh577_unita"]("M3") == "M3"
        assert _F["mh577_unita"]("mwh") == "MWH"

    def test_tipo_ko(self):
        for bad in ("FV", "", None, "cashflow"):
            with pytest.raises(ValueError):
                _F["mh577_tipo"](bad)

    def test_unita_ko(self):
        for bad in ("JPY", "", None, "ton"):
            with pytest.raises(ValueError):
                _F["mh577_unita"](bad)


class TestW577Item:
    def test_hand_computed(self):
        r = _i()
        assert r["valore_att"] == pytest.approx(800_000.0)
        assert r["valore_pass"] == pytest.approx(0.0)
        assert r["variazione_valore"] == pytest.approx(-150_000.0)
        assert r["nozionale_importo"] == pytest.approx(30_000.0)
        assert r["nozionale_unita"] == "MWH"
        assert r["fisico"] is True
        assert r["rischio_label"] == "Commodity"
        assert r["tipo_label"] == "Cash flow hedges"
        assert r["adeguamento_fv"] is None
        assert r["completa"] and r["anomalie"] == []

    def test_voce_vuota_anomalia(self):
        r = _i(voce="   ")
        assert not r["completa"]
        assert any("Voce di stato patrimoniale non indicata" in a
                   for a in r["anomalie"])

    def test_nozionale_zero_anomalia(self):
        r = _i(not_=0.0)
        assert not r["completa"]
        assert any("Nozionale nullo o negativo" in a
                   for a in r["anomalie"])

    def test_nozionale_negativo_anomalia(self):
        r = _i(not_=-5.0)
        assert any("Nozionale nullo o negativo" in a
                   for a in r["anomalie"])

    def test_nozionale_none_anomalia(self):
        r = _F["mh577_item"]("HI-1", "s", "FX", "CASH_FLOW",
                             10.0, 0.0, "voce", 0.0,
                             nozionale_importo=None)
        assert any("Nozionale non dichiarato" in a
                   for a in r["anomalie"])

    def test_variazione_none_anomalia(self):
        r = _i(vv=None)
        assert r["variazione_valore"] == 0.0
        assert any("Variazione di valore non dichiarata" in a
                   for a in r["anomalie"])

    def test_variazione_non_numerico_ko(self):
        with pytest.raises(ValueError):
            _i(vv="x")

    def test_valori_contabili_zero_anomalia(self):
        r = _i(att=0.0, pas=0.0)
        assert any("Nessun valore contabile rilevato" in a
                   for a in r["anomalie"])

    def test_fisico_flag(self):
        assert _i(un="EUR")["fisico"] is False
        assert _i(un="M3")["fisico"] is True
        assert _i(un="MWH")["fisico"] is True

    def test_adeguamento_fv_solo_fair_value(self):
        r = _F["mh577_item"]("HI-9", "d", "TASSO", "FAIR_VALUE",
                             100.0, 0.0, "voce", 10.0,
                             nozionale_importo=1_000.0,
                             nozionale_unita="EUR")
        assert r["adeguamento_fv"] == 0.0
        assert any("Adeguamento FV cumulato non dichiarato" in a
                   for a in r["anomalie"])
        r2 = _F["mh577_item"]("HI-9", "d", "TASSO", "FAIR_VALUE",
                              100.0, 0.0, "voce", 10.0,
                              nozionale_importo=1_000.0,
                              nozionale_unita="EUR",
                              adeguamento_fv=-40.0)
        assert r2["adeguamento_fv"] == pytest.approx(-40.0)
        assert r2["completa"]
        r3 = _i(adj=999.0)
        assert r3["adeguamento_fv"] is None
        assert r3["completa"]

    def test_strip(self):
        r = _i(sid="  HI-X  ", descrizione="  d  ", rischio="fx",
               voce="  voce x  ")
        assert r["id"] == "HI-X"
        assert r["rischio"] == "FX"
        assert r["voce_bilancio"] == "voce x"


class TestW577Riepilogo:
    def test_demo_disclosure_completa(self):
        r = _F["mh577_riepilogo"](_F["mh577_demo"]())
        # att = 2.4M; pass = 1.5M + 5M = 6.5M; netto = -4.1M
        assert r["totale_att"] == pytest.approx(2_400_000.0)
        assert r["totale_pass"] == pytest.approx(6_500_000.0)
        assert r["valore_netto"] == pytest.approx(-4_100_000.0)
        # adeguamenti FV: +310k (HI-301) - 150k (HI-303) = 160k
        assert r["adeguamento_fv_totale"] == pytest.approx(160_000.0)
        assert r["n_items"] == 3
        assert r["n_anomalie"] == 0
        assert r["n_nozionali_fisici"] == 2
        assert r["verdetto"] == "DISCLOSURE_COMPLETA"
        vt = r["valore_per_tipo"]
        assert vt["Fair value hedges"] == {"att": pytest.approx(
            2_400_000.0), "pass": pytest.approx(5_000_000.0)}
        assert vt["Cash flow hedges"] == {"att": pytest.approx(
            0.0), "pass": pytest.approx(1_500_000.0)}
        assert vt["Net investment hedges"] == {"att": pytest.approx(
            0.0), "pass": pytest.approx(0.0)}
        apt = r["adeguamento_per_tipo"]
        assert apt["Fair value hedges"] == pytest.approx(160_000.0)
        assert apt["Cash flow hedges"] == pytest.approx(0.0)
        assert apt["Net investment hedges"] == pytest.approx(0.0)
        npr = r["nozionale_per_rischio"]
        assert npr["Commodity"] == {"MWH": pytest.approx(120_000.0),
                                    "T": pytest.approx(45_000.0)}
        assert npr["Tasso di interesse"] == {
            "EUR": pytest.approx(5_000_000.0)}

    def test_nessun_elemento(self):
        r = _F["mh577_riepilogo"]([])
        assert r["verdetto"] == "NESSUN_ELEMENTO"
        assert r["n_items"] == 0
        assert r["adeguamento_fv_totale"] == 0.0
        assert r["valore_per_tipo"]["Fair value hedges"]["att"] == 0.0

    def test_duplicati_anomalia(self):
        r = _F["mh577_riepilogo"]([_i(sid="DUP"), _i(sid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"]
                   for x in r["analizzati"])

    def test_anomalie_hanno_priorita(self):
        bad = _i(voce="")
        r = _F["mh577_riepilogo"]([bad])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_nozionale_e_valori_per_rischio_tipo(self):
        r = _F["mh577_riepilogo"]([_i(sid="A", rischio="TASSO",
                                      tipo="FAIR_VALUE", att=100.0,
                                      pas=0.0, not_=1_000.0, un="EUR",
                                      adj=20.0),
                                   _i(sid="B", rischio="TASSO",
                                      tipo="FAIR_VALUE", att=0.0,
                                      pas=50.0, not_=500.0, un="EUR",
                                      adj=-10.0)])
        assert r["nozionale_per_rischio"]["Tasso di interesse"] == \
            {"EUR": pytest.approx(1_500.0)}
        assert r["valore_per_tipo"]["Fair value hedges"] == \
            {"att": pytest.approx(100.0), "pass": pytest.approx(50.0)}
        assert r["adeguamento_per_tipo"]["Fair value hedges"] == \
            pytest.approx(10.0)


class TestW577Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE577}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 767
        assert TITLE577 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767 = st.tabs([" in src
        assert "with tab577:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st577_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
