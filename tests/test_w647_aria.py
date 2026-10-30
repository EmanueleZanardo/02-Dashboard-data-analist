"""Test tab647 "🌬️🔧 Aria compressa: quanto costano le perdite?".

Demo calcolata a mano: compressore 75 kW, consumo specifico
6,5 kW/(m3/min), 6.000 h/anno, prezzo 0,22 €/kWh, perdite 25 %,
riduzione pressione 1 bar, CAPEX 8.000 €, tasso 6 %, vita 10 anni.
-> portata = 75 / 6,5 = 11,5384615 m3/min
-> E_base = 75 x 6.000 = 450.000 kWh/anno
-> E_perdite = 450.000 x 25 % = 112.500 kWh/anno -> 24.750 €/anno
-> E_press = (450.000 - 112.500) x 0,07 x 1,0 = 23.625 kWh/anno
-> risparmio 136.125 kWh/anno (30,25 %), 29.947,5 €/anno
-> ore sprecate = 112.500 / 75 = 1.500 h/anno
-> flussi [-8.000, 29.947,5 x 10]; VAN(6 %) = 212.416,21 €
-> TIR 374,34 %; payback anno 1 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh647_num", "mh647_nneg", "mh647_pos", "mh647_pct100",
           "mh647_fraz01", "mh647_int_pos", "mh647_portata_nominale_m3min",
           "mh647_energia_base_kwh", "mh647_energia_perdite_kwh",
           "mh647_risparmio_pressione_kwh", "mh647_risparmio_totale_kwh",
           "mh647_risparmio_eur", "mh647_costo_perdite_eur",
           "mh647_quota_risparmio_pct", "mh647_ore_sprecate",
           "mh647_crf", "mh647_flussi", "mh647_van", "mh647_tir",
           "mh647_payback", "mh647_verdetto", "mh647_demo",
           "mh647_demo_calcoli")

TITLE647 = "🌬️🔧 Aria compressa: quanto costano le perdite?"

PORTATA_DEMO = 11.538461538461538
E_BASE_DEMO = 450000.0
E_PERDITE_DEMO = 112500.0
E_PRESS_DEMO = 23625.0
E_RISP_DEMO = 136125.0
RISP_EUR_DEMO = 29947.5
COSTO_PERDITE_DEMO = 24750.0
QUOTA_DEMO = 30.25
ORE_SPRECATE_DEMO = 1500.0
VAN_DEMO = 212416.21
TIR_DEMO = 3.7434


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh647_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh647_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh647_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh647_nneg"](-0.1, "x")
        assert _F["mh647_pos"](0.1, "x") == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh647_pos"](0.0, "x")

    def test_pct100_e_fraz01(self):
        assert _F["mh647_pct100"](100, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh647_pct100"](100.1, "x")
        assert _F["mh647_fraz01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh647_fraz01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh647_fraz01"](1.5, "x")

    def test_int_pos(self):
        assert _F["mh647_int_pos"](10.0, "x") == 10
        with pytest.raises(ValueError):
            _F["mh647_int_pos"](10.5, "x")
        with pytest.raises(ValueError):
            _F["mh647_int_pos"](0, "x")


class TestPortataEdEnergia:
    def test_portata_nominale(self):
        assert _F["mh647_portata_nominale_m3min"](
            75.0, 6.5) == pytest.approx(PORTATA_DEMO)

    def test_portata_rifiuta_consumo_nullo(self):
        with pytest.raises(ValueError):
            _F["mh647_portata_nominale_m3min"](75.0, 0.0)

    def test_energia_base(self):
        assert _F["mh647_energia_base_kwh"](
            75.0, 6000.0) == pytest.approx(E_BASE_DEMO)

    def test_energia_base_nulla_se_fermo(self):
        assert _F["mh647_energia_base_kwh"](75.0, 0.0) == 0.0
        assert _F["mh647_energia_base_kwh"](0.0, 6000.0) == 0.0

    def test_energia_perdite(self):
        assert _F["mh647_energia_perdite_kwh"](
            E_BASE_DEMO, 25.0) == pytest.approx(E_PERDITE_DEMO)

    def test_energia_perdite_zero_se_quota_zero(self):
        assert _F["mh647_energia_perdite_kwh"](E_BASE_DEMO, 0.0) == 0.0

    def test_energia_perdite_quota_oltre_100_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh647_energia_perdite_kwh"](E_BASE_DEMO, 101.0)


class TestRisparmio:
    def test_risparmio_pressione(self):
        assert _F["mh647_risparmio_pressione_kwh"](
            E_BASE_DEMO, E_PERDITE_DEMO,
            1.0) == pytest.approx(E_PRESS_DEMO)

    def test_risparmio_pressione_due_bar(self):
        # 2 bar -> doppio del risparmio a 1 bar
        assert _F["mh647_risparmio_pressione_kwh"](
            E_BASE_DEMO, E_PERDITE_DEMO,
            2.0) == pytest.approx(2.0 * E_PRESS_DEMO)

    def test_risparmio_pressione_zero_se_delta_zero(self):
        assert _F["mh647_risparmio_pressione_kwh"](
            E_BASE_DEMO, E_PERDITE_DEMO, 0.0) == 0.0

    def test_risparmio_pressione_su_residuo(self):
        # la regola del 7 % si applica all'energia residua (base - perdite),
        # non all'intera base: con perdite al 100 % non resta nulla
        assert _F["mh647_risparmio_pressione_kwh"](
            E_BASE_DEMO, E_BASE_DEMO, 1.0) == 0.0

    def test_risparmio_pressione_rifiuta_perdite_oltre_base(self):
        with pytest.raises(ValueError):
            _F["mh647_risparmio_pressione_kwh"](
                E_BASE_DEMO, E_BASE_DEMO + 1.0, 1.0)

    def test_risparmio_totale(self):
        assert _F["mh647_risparmio_totale_kwh"](
            E_PERDITE_DEMO, E_PRESS_DEMO) == pytest.approx(E_RISP_DEMO)

    def test_risparmio_eur(self):
        assert _F["mh647_risparmio_eur"](
            E_RISP_DEMO, 0.22) == pytest.approx(RISP_EUR_DEMO)

    def test_costo_perdite_eur(self):
        assert _F["mh647_costo_perdite_eur"](
            E_PERDITE_DEMO, 0.22) == pytest.approx(COSTO_PERDITE_DEMO)

    def test_quota_risparmio(self):
        assert _F["mh647_quota_risparmio_pct"](
            E_RISP_DEMO, E_BASE_DEMO) == pytest.approx(QUOTA_DEMO, abs=0.01)

    def test_quota_none_se_base_nulla(self):
        assert _F["mh647_quota_risparmio_pct"](100.0, 0.0) is None

    def test_ore_sprecate(self):
        assert _F["mh647_ore_sprecate"](
            E_PERDITE_DEMO, 75.0) == pytest.approx(ORE_SPRECATE_DEMO)

    def test_ore_sprecate_none_se_potenza_nulla(self):
        assert _F["mh647_ore_sprecate"](E_PERDITE_DEMO, 0.0) is None


class TestBusinessCase:
    def _flussi_demo(self):
        return _F["mh647_flussi"](8000.0, RISP_EUR_DEMO, 10)

    def test_flussi(self):
        f = self._flussi_demo()
        assert f[0] == -8000.0
        assert len(f) == 11
        assert all(v == pytest.approx(RISP_EUR_DEMO) for v in f[1:])

    def test_crf(self):
        assert _F["mh647_crf"](6.0, 10) == pytest.approx(0.13586796,
                                                        abs=1e-6)
        assert _F["mh647_crf"](0.0, 10) == pytest.approx(0.1)

    def test_van_demo(self):
        assert _F["mh647_van"](self._flussi_demo(),
                               6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_van_tasso_zero(self):
        assert _F["mh647_van"](self._flussi_demo(),
                               0.0) == pytest.approx(-8000.0 +
                                                     RISP_EUR_DEMO * 10)

    def test_tir_demo(self):
        assert _F["mh647_tir"](
            self._flussi_demo()) == pytest.approx(TIR_DEMO, abs=0.01)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh647_tir"]([100.0, 50.0]) is None
        assert _F["mh647_tir"]([-100.0, -50.0]) is None

    def test_payback_demo(self):
        assert _F["mh647_payback"](self._flussi_demo()) == 1

    def test_payback_none_se_mai(self):
        assert _F["mh647_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviene(self):
        assert _F["mh647_verdetto"](
            RISP_EUR_DEMO, VAN_DEMO, 8000.0, 10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh647_verdetto"](
            100.0, -500.0, 8000.0, 10.0) == "MARGINALE"

    def test_verdetto_non_conviene(self):
        assert _F["mh647_verdetto"](
            100.0, -5000.0, 8000.0, 10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh647_verdetto"](
            0.0, 100.0, 8000.0, 10.0) == "NON_CALCOLABILE"
        assert _F["mh647_verdetto"](
            -5.0, 100.0, 8000.0, 10.0) == "NON_CALCOLABILE"
        assert _F["mh647_verdetto"](
            100.0, None, 8000.0, 10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        r = _F["mh647_demo_calcoli"]()
        assert r["portata_m3min"] == pytest.approx(PORTATA_DEMO)
        assert r["e_base"] == pytest.approx(E_BASE_DEMO)
        assert r["e_perdite"] == pytest.approx(E_PERDITE_DEMO)
        assert r["e_pressione"] == pytest.approx(E_PRESS_DEMO)
        assert r["e_risp"] == pytest.approx(E_RISP_DEMO)
        assert r["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert r["costo_perdite_eur"] == pytest.approx(COSTO_PERDITE_DEMO)
        assert r["quota_pct"] == pytest.approx(QUOTA_DEMO, abs=0.01)
        assert r["ore_sprecate"] == pytest.approx(ORE_SPRECATE_DEMO)
        assert r["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert r["tir"] == pytest.approx(TIR_DEMO, abs=0.01)
        assert r["payback"] == 1
        assert r["verdetto"] == "CONVIENTE"


class TestRegistry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def _ui(self):
        s = self._src()
        return s.split("with tab647:")[1].split("# Footer")[0]

    def _helpers(self):
        s = self._src()
        return s.split("# W647 (22/10/2026)")[1].split(
            "# W646 (22/10/2026)")[0]

    def test_chain_registry_e_label(self):
        assert ", tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823 = st.tabs([" in self._src()
        assert "with tab647:" in self._src()
        assert TITLE647 in self._src()

    def test_registry_647(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 823
        assert TITLE647 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab647" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab647" in withs

    def test_helpers_presenti(self):
        h = self._helpers()
        for nome in ("mh647_portata_nominale_m3min",
                     "mh647_energia_base_kwh",
                     "mh647_energia_perdite_kwh",
                     "mh647_risparmio_pressione_kwh",
                     "mh647_risparmio_totale_kwh",
                     "mh647_verdetto",
                     "mh647_demo_calcoli"):
            assert f"def {nome}(" in h

    def test_ui_chiavi_uniche(self):
        ui = self._ui()
        chiavi = re.findall(r'key="(st647_[a-z0-9_]+)"', ui)
        assert chiavi, "nessuna chiave st647_* trovata"
        assert len(chiavi) == len(set(chiavi)), "chiavi duplicate"
        assert 'key="st647_calcola"' in ui
        assert 'key="st647_csv"' in ui

    def test_ui_guard_degenere(self):
        ui = self._ui()
        assert "_degen647" in ui
        assert "non calcolabili" in ui
