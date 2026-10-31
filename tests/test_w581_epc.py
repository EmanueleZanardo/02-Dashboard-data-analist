"""Test tab581 "EPC: rendimento energetico garantito (ESCO)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh581_num", "mh581_str", "mh581_van", "mh581_irr",
           "mh581_proposta", "mh581_demo", "mh581_riepilogo")

TITLE581 = "🏭🤝 EPC: rendimento energetico garantito (ESCO)"


def _p(pid="EPC-1", descrizione="proposta", baseline=2_000_000.0,
       prezzo=0.22, investimento=400_000.0, risparmio=30.0,
       canone=30_000.0, durata=10, tasso=5.0):
    return _F["mh581_proposta"](pid, descrizione, baseline, prezzo,
                                investimento, risparmio, canone,
                                durata, tasso)


class TestW581Validatori:
    def test_num_ok(self):
        assert _F["mh581_num"](2, "x") == 2.0
        assert _F["mh581_num"](-3.5, "x") == -3.5
        assert _F["mh581_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh581_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh581_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh581_str"](bad, "x")

    def test_van_tasso_zero(self):
        assert _F["mh581_van"](400_000.0, 102_000.0, 10, 0.0) == \
            pytest.approx(-400_000.0 + 102_000.0 * 10)

    def test_van_hand(self):
        assert _F["mh581_van"](400_000.0, 102_000.0, 10, 0.05) == \
            pytest.approx(387_616.96, rel=1e-4)

    def test_irr_none_flusso_non_positivo(self):
        assert _F["mh581_irr"](400_000.0, 0.0, 10) is None
        assert _F["mh581_irr"](400_000.0, -5.0, 10) is None

    def test_durata_non_intera_ko(self):
        with pytest.raises(ValueError):
            _p(durata=10.5)
        with pytest.raises(ValueError):
            _p(durata=True)

    def test_canone_negativo_ko(self):
        with pytest.raises(ValueError):
            _p(canone=-1.0)

    def test_tasso_negativo_ko(self):
        with pytest.raises(ValueError):
            _p(tasso=-0.5)


class TestW581Proposta:
    def test_hand_computed_conviene(self):
        r = _p("EPC-01", "Efficientamento HVAC stabilimento")
        assert r["completa"] is True
        assert r["anomalie"] == []
        assert r["costo_baseline_annuo"] == pytest.approx(440_000.0)
        assert r["risparmio_annuo_garantito"] == pytest.approx(132_000.0)
        assert r["flusso_netto_annuo"] == pytest.approx(102_000.0)
        assert r["payback_anni"] == pytest.approx(3.9215686, rel=1e-6)
        assert r["van_eur"] == pytest.approx(387_616.96, rel=1e-4)
        assert r["irr"] == pytest.approx(0.2201, rel=1e-2)

    def test_hand_computed_non_conviene(self):
        r = _p("EPC-02", "Relamping magazzino", baseline=1_000_000.0,
              prezzo=0.20, investimento=500_000.0, risparmio=15.0,
              canone=12_000.0)
        assert r["completa"] is True
        assert r["van_eur"] == pytest.approx(-361_008.77, rel=1e-4)
        assert r["payback_anni"] == pytest.approx(27.7778, rel=1e-4)
        assert r["irr"] is not None and r["irr"] < 0.0

    def test_anomalia_baseline_non_positiva(self):
        r = _p(baseline=0.0)
        assert r["completa"] is False
        assert "Baseline nulla o negativa" in r["anomalie"]
        assert r["van_eur"] is None

    def test_anomalia_prezzo_non_positivo(self):
        r = _p(prezzo=-0.1)
        assert "Prezzo energia nullo o negativo" in r["anomalie"]

    def test_anomalia_investimento_non_positivo(self):
        r = _p(investimento=0.0)
        assert "Investimento nullo o negativo" in r["anomalie"]

    def test_anomalia_risparmio_fuori_range(self):
        for bad in (0.0, 100.0, 120.0, -5.0):
            r = _p(risparmio=bad)
            assert "Risparmio garantito fuori (0, 100)%" in r["anomalie"], bad

    def test_anomalia_canone_oltre_risparmio(self):
        # risparmio garantito = 440.000 * 30% = 132.000 < canone 150.000
        r = _p(canone=150_000.0)
        assert "Canone supera il risparmio garantito" in r["anomalie"]
        assert r["completa"] is False

    def test_anomalia_durata_fuori_range(self):
        r = _p(durata=20)
        assert "Durata fuori [1, 15] anni" in r["anomalie"]

    def test_canone_uguale_risparmio(self):
        # flusso netto zero: completa, payback None, VAN negativo
        r = _p(canone=132_000.0)
        assert r["completa"] is True
        assert r["flusso_netto_annuo"] == pytest.approx(0.0)
        assert r["payback_anni"] is None
        assert r["van_eur"] == pytest.approx(-400_000.0)
        assert r["irr"] is None


class TestW581Demo:
    def test_demo_due_proposte(self):
        d = _F["mh581_demo"]()
        assert len(d) == 2
        assert d[0]["id"] == "EPC-01"
        assert d[1]["id"] == "EPC-02"
        assert all(p["completa"] for p in d)

    def test_demo_riepilogo_conviene(self):
        ri = _F["mh581_riepilogo"](_F["mh581_demo"]())
        assert ri["verdetto"] == "CONVIENE"
        assert ri["n_proposte"] == 2
        assert ri["n_anomalie"] == 0
        assert ri["miglior_id"] == "EPC-01"
        assert ri["miglior_van"] == pytest.approx(387_616.96, rel=1e-4)


class TestW581Riepilogo:
    def test_vuoto(self):
        ri = _F["mh581_riepilogo"]([])
        assert ri["verdetto"] == "NESSUNA_PROPOSTA"
        assert ri["n_proposte"] == 0

    def test_anomalie_precedenza(self):
        bad = _p("EPC-X", "x", baseline=0.0)
        good = _p("EPC-01", "Efficientamento HVAC stabilimento")
        ri = _F["mh581_riepilogo"]([good, bad])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert ri["n_anomalie"] == 1
        assert ri["miglior_id"] is None

    def test_duplicati(self):
        a = _p("EPC-01", "a")
        b = _p("EPC-01", "b")
        ri = _F["mh581_riepilogo"]([a, b])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert ri["n_anomalie"] == 2
        assert all("ID duplicato" in o["anomalie"]
                   for o in ri["analizzati"])

    def test_non_conviene(self):
        solo = _p("EPC-02", "Relamping magazzino", baseline=1_000_000.0,
                 prezzo=0.20, investimento=500_000.0, risparmio=15.0,
                 canone=12_000.0)
        ri = _F["mh581_riepilogo"]([solo])
        assert ri["verdetto"] == "NON_CONVIENE"
        assert ri["miglior_id"] == "EPC-02"
        assert ri["miglior_payback_anni"] == pytest.approx(27.7778,
                                                          rel=1e-4)

    def test_migliore_e_il_max_van(self):
        a = _p("EPC-A", "a")  # VAN +387k
        b = _p("EPC-B", "b", investimento=100_000.0)  # VAN piu' alto
        ri = _F["mh581_riepilogo"]([a, b])
        assert ri["verdetto"] == "CONVIENE"
        assert ri["miglior_id"] == "EPC-B"
        assert ri["miglior_van"] > 387_616.96


class TestW581Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE581}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 827
        assert TITLE581 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827 = st.tabs([" in src
        assert "with tab581:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st581_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
