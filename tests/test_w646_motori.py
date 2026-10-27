"""Test tab646 "🔧⚙️ Motori elettrici: l'inverter paga?".

Demo calcolata a mano: pompa 110 kW, profilo (100 %, 2.000 h),
(80 %, 3.000 h), (60 %, 2.760 h) -> 7.760 h/anno; strozzamento 95 %;
prezzo 0,22 €/kWh; inverter 120 €/kW; tasso 6 %; vita 12 anni.
-> E_base = 110 x 0,95 x 7.760 = 810.920 kWh/anno
-> E_vsd = 110 x (2.000 + 3.000 x 0,512 + 2.760 x 0,216) = 454.537,6
-> risparmio 356.382,4 kWh/anno (43,95 %), 78.404,128 €/anno
-> CAPEX 13.200 €; VAN(6 %) +644.128,0 €; TIR 593,97 %; payback anno 1
-> verdetto CONVIENTE; potenza media risparmiata 45,93 kW.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh646_num", "mh646_nneg", "mh646_pos", "mh646_pct100",
           "mh646_fraz01", "mh646_int_pos", "mh646_potenza_affinita",
           "mh646_ore_totali", "mh646_energia_vsd", "mh646_energia_base",
           "mh646_risparmio_kwh", "mh646_risparmio_eur", "mh646_capex",
           "mh646_quota_risparmio_pct", "mh646_potenza_media_risparmiata_kw",
           "mh646_crf", "mh646_flussi", "mh646_van", "mh646_tir",
           "mh646_payback", "mh646_verdetto", "mh646_demo",
           "mh646_demo_calcoli")

TITLE646 = "🔧⚙️ Motori elettrici: l'inverter paga?"

ORE_DEMO = 7760.0
E_BASE_DEMO = 810920.0
E_VSD_DEMO = 454537.6
RISP_KWH_DEMO = 356382.4
QUOTA_DEMO = 43.95
RISP_EUR_DEMO = 78404.128
CAPEX_DEMO = 13200.0
VAN_DEMO = 644128.0
TIR_DEMO = 5.9397
P_MEDIA_DEMO = 45.93
PROFILO_DEMO = [(100.0, 2000.0), (80.0, 3000.0), (60.0, 2760.0)]


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh646_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh646_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh646_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh646_nneg"](-0.1, "x")
        assert _F["mh646_pos"](0.1, "x") == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh646_pos"](0.0, "x")

    def test_pct100_e_fraz01(self):
        assert _F["mh646_pct100"](100, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh646_pct100"](100.1, "x")
        assert _F["mh646_fraz01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh646_fraz01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh646_fraz01"](1.5, "x")

    def test_int_pos(self):
        assert _F["mh646_int_pos"](12.0, "x") == 12
        with pytest.raises(ValueError):
            _F["mh646_int_pos"](12.5, "x")
        with pytest.raises(ValueError):
            _F["mh646_int_pos"](0, "x")


class TestAffinita:
    def test_potenza_piena_portata(self):
        assert _F["mh646_potenza_affinita"](110.0, 100.0) == pytest.approx(110.0)

    def test_potenza_legge_cubo(self):
        # 50 % di portata -> 12,5 % della potenza
        assert _F["mh646_potenza_affinita"](110.0, 50.0) == pytest.approx(13.75)
        assert _F["mh646_potenza_affinita"](110.0, 80.0) == pytest.approx(56.32)

    def test_potenza_zero_a_portata_zero(self):
        assert _F["mh646_potenza_affinita"](110.0, 0.0) == 0.0

    def test_portata_fuori_range_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh646_potenza_affinita"](110.0, 101.0)
        with pytest.raises(ValueError):
            _F["mh646_potenza_affinita"](-5.0, 80.0)


class TestEnergia:
    def test_ore_totali(self):
        assert _F["mh646_ore_totali"](PROFILO_DEMO) == pytest.approx(ORE_DEMO)

    def test_ore_totali_vuoto(self):
        assert _F["mh646_ore_totali"]([]) == 0.0

    def test_energia_base(self):
        assert _F["mh646_energia_base"](110.0, ORE_DEMO, 0.95) == pytest.approx(
            E_BASE_DEMO)

    def test_energia_vsd(self):
        assert _F["mh646_energia_vsd"](110.0, PROFILO_DEMO) == pytest.approx(
            E_VSD_DEMO)

    def test_risparmio_kwh(self):
        assert _F["mh646_risparmio_kwh"](E_BASE_DEMO, E_VSD_DEMO) == pytest.approx(
            RISP_KWH_DEMO)

    def test_risparmio_negativo_se_profilo_pieno(self):
        # profilo tutto al 100 % con strozzamento 95 %: VSD non risparmia
        e_vsd = _F["mh646_energia_vsd"](110.0, [(100.0, 7760.0)])
        e_base = _F["mh646_energia_base"](110.0, 7760.0, 0.95)
        assert _F["mh646_risparmio_kwh"](e_base, e_vsd) < 0.0

    def test_quota_risparmio(self):
        assert _F["mh646_quota_risparmio_pct"](
            RISP_KWH_DEMO, E_BASE_DEMO) == pytest.approx(QUOTA_DEMO, abs=0.01)

    def test_quota_none_se_base_nulla(self):
        assert _F["mh646_quota_risparmio_pct"](100.0, 0.0) is None

    def test_potenza_media_risparmiata(self):
        assert _F["mh646_potenza_media_risparmiata_kw"](
            RISP_KWH_DEMO, ORE_DEMO) == pytest.approx(P_MEDIA_DEMO, abs=0.01)

    def test_potenza_media_none_se_ore_nulle(self):
        assert _F["mh646_potenza_media_risparmiata_kw"](100.0, 0.0) is None


class TestBusinessCase:
    def test_risparmio_eur(self):
        assert _F["mh646_risparmio_eur"](
            RISP_KWH_DEMO, 0.22) == pytest.approx(RISP_EUR_DEMO)

    def test_capex(self):
        assert _F["mh646_capex"](110.0, 120.0) == pytest.approx(CAPEX_DEMO)

    def test_crf(self):
        assert _F["mh646_crf"](6.0, 12) == pytest.approx(0.119277, abs=1e-4)
        assert _F["mh646_crf"](0.0, 12) == pytest.approx(1.0 / 12)

    def test_flussi(self):
        f = _F["mh646_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 12)
        assert f[0] == pytest.approx(-CAPEX_DEMO)
        assert len(f) == 13 and all(
            v == pytest.approx(RISP_EUR_DEMO) for v in f[1:])

    def test_van(self):
        f = _F["mh646_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 12)
        assert _F["mh646_van"](f, 6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_tir(self):
        f = _F["mh646_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 12)
        assert _F["mh646_tir"](f) == pytest.approx(TIR_DEMO, abs=0.01)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh646_tir"]([100.0, 50.0, 50.0]) is None
        assert _F["mh646_tir"]([-100.0, -50.0]) is None

    def test_payback(self):
        f = _F["mh646_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 12)
        assert _F["mh646_payback"](f) == 1

    def test_payback_none_se_mai(self):
        assert _F["mh646_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviente(self):
        assert _F["mh646_verdetto"](RISP_EUR_DEMO, VAN_DEMO, CAPEX_DEMO,
                                   10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh646_verdetto"](1000.0, -500.0, 13200.0,
                                   10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh646_verdetto"](1000.0, -5000.0, 13200.0,
                                   10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh646_verdetto"](0.0, 100.0, CAPEX_DEMO,
                                   10.0) == "NON_CALCOLABILE"
        assert _F["mh646_verdetto"](-5.0, 100.0, CAPEX_DEMO,
                                   10.0) == "NON_CALCOLABILE"
        assert _F["mh646_verdetto"](1000.0, None, CAPEX_DEMO,
                                   10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh646_demo_calcoli"]()
        assert c["ore_tot"] == pytest.approx(ORE_DEMO)
        assert c["energia_base_kwh"] == pytest.approx(E_BASE_DEMO)
        assert c["energia_vsd_kwh"] == pytest.approx(E_VSD_DEMO)
        assert c["risparmio_kwh"] == pytest.approx(RISP_KWH_DEMO)
        assert c["quota_risp_pct"] == pytest.approx(QUOTA_DEMO, abs=0.01)
        assert c["risparmio_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=0.01)
        assert c["payback"] == 1
        assert c["verdetto"] == "CONVIENTE"
        assert c["p_media_risp_kw"] == pytest.approx(P_MEDIA_DEMO, abs=0.01)

    def test_demo_input(self):
        d = _F["mh646_demo"]()
        assert d["p_nom_kw"] == 110.0 and len(d["profilo"]) == 3


class TestIntegrazioneUI:
    @staticmethod
    def _src():
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        s = self._src()
        return s.split("with tab646:")[1].split("# Footer")[0]

    def _helpers(self):
        s = self._src()
        return s.split("# W646 (22/10/2026)")[1].split(
            "# W645 (22/10/2026)")[0]

    def test_chain_registry_e_label(self):
        assert ", tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761 = st.tabs([" in self._src()
        assert "with tab646:" in self._src()
        assert TITLE646 in self._src()

    def test_registry_646(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 761
        assert TITLE646 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab646" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab646" in withs
        assert len(withs) == len(dvars) == 761

    def test_ui_chiavi_e_guard(self):
        ui = self._ui()
        assert "st646_calcola" in ui and "st646_csv" in ui
        assert "Profilo di carico nullo" in ui
        assert "mh646_demo_calcoli" in ui or "mh646_ore_totali" in ui

    def test_nessun_segreto_negli_helper(self):
        h = self._helpers().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in h

    def test_chiavi_st_univoche(self):
        ui = self._ui()
        chiavi = re.findall(r'key="(st646_[^"]+)"', ui)
        attese = {"st646_pnom", "st646_prezzo", "st646_eurkw",
                  "st646_fstrozz", "st646_tasso", "st646_vita",
                  "st646_toll", "st646_calcola", "st646_csv"}
        assert attese.issubset(set(chiavi))
        assert len(chiavi) == len(set(chiavi))
        fstr = re.findall(r'key=f"st646_[qh]\{', ui)
        # 2 template f-string nel loop (3 scaglioni) -> 6 chiavi runtime
        assert sorted(fstr) == ['key=f"st646_h{', 'key=f"st646_q{']
