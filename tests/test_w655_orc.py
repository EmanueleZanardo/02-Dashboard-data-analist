"""Test tab655 "♨️⚡ ORC: il calore di scarto diventa elettricità".

Demo calcolata a mano: fumi di forno, 500 kW termici a 280 C,
condensazione a 30 C, 7.000 h/anno, k_carnot 0,45, ausiliari 8 %,
quota autoconsumo 70 % (0,22 €/kWh) / cessione 30 % (0,14 €/kWh),
smaltimento calore 5.000 €/anno, O&M 25.000 €/anno, CAPEX 900.000 €,
CO2 elettricità 0,30 kg/kWh, 6 %, 15 anni, escalation 2 %/anno,
tolleranza 10 %.

- eta = 0,45 x (1 - 303,15/553,15) = 0,20338063816324686
- P_el = 500 x 0,20338063816324686 = 101,69031908162343 kW
- E_lorda = 101,69031908162343 x 7.000 = 711.832,233571364 kWh/anno
- E_netta = 711.832,233571364 x 0,92 = 654.885,6548856549 kWh/anno
- Q_scar = 500 x 7.000 - 711.832,233571364 = 2.788.167,766428636 kWh/anno
- p_medio = 0,70 x 0,22 + 0,30 x 0,14 = 0,196 €/kWh
- risparmio anno 1 = 654.885,6548856549 x 0,196 - 25.000 - 5.000
  = 98.357,58835758836 €/anno
- CO2 evitata = 654.885,6548856549 x 0,30 / 1.000 = 196,46569646569648 t/anno
- flussi [-900.000, 98.357,59 x 1,02^i per i=1..15]; VAN(6 %) =
  199.599,69817926973 €; TIR 0,09065139642180237 (9,0651 %); payback anno 9;
  VAN > 0 -> CONVIENTE
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh655_num", "mh655_nneg", "mh655_pos", "mh655_int_pos",
           "mh655_frazione", "mh655_k_carnot", "mh655_aux_pct",
           "mh655_eta_orc", "mh655_potenza_elettrica",
           "mh655_energia_lorda", "mh655_energia_netta",
           "mh655_calore_scaricato", "mh655_prezzo_medio",
           "mh655_capex_da_specifico", "mh655_risparmio", "mh655_co2_t",
           "mh655_flussi", "mh655_flussi_esc", "mh655_van", "mh655_tir",
           "mh655_payback", "mh655_verdetto", "mh655_demo",
           "mh655_demo_calcoli")

TITLE655 = "♨️⚡ ORC: il calore di scarto diventa elettricità"

ETA_DEMO = 0.20338063816324686
P_EL_DEMO = 101.69031908162343
E_LORDA_DEMO = 711832.233571364
E_NETTA_DEMO = 654885.6548856549
Q_SCAR_DEMO = 2788167.766428636
P_MEDIO_DEMO = 0.196
RISP_DEMO = 98357.58835758836
CO2_DEMO = 196.46569646569648
CAPEX_DEMO = 900000.0
VAN_DEMO = 199599.69817926973
TIR_DEMO = 0.09065139642180237


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh655_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh655_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh655_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh655_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh655_pos"](0, "x")
        assert _F["mh655_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh655_int_pos"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh655_int_pos"](15.5, "x")

    def test_frazione_bordi(self):
        assert _F["mh655_frazione"](0, "x") == 0.0
        assert _F["mh655_frazione"](1, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh655_frazione"](1.1, "x")

    def test_k_carnot_bordi_aperti(self):
        with pytest.raises(ValueError):
            _F["mh655_k_carnot"](0, "x")
        with pytest.raises(ValueError):
            _F["mh655_k_carnot"](1, "x")
        assert _F["mh655_k_carnot"](0.45, "x") == 0.45

    def test_aux_bordi(self):
        assert _F["mh655_aux_pct"](0, "x") == 0.0
        assert _F["mh655_aux_pct"](99.9, "x") == 99.9
        with pytest.raises(ValueError):
            _F["mh655_aux_pct"](100.0, "x")
        with pytest.raises(ValueError):
            _F["mh655_aux_pct"](-1.0, "x")


class TestEta:
    def test_eta_demo(self):
        assert _F["mh655_eta_orc"](280.0, 30.0, 0.45) == \
            pytest.approx(ETA_DEMO)

    def test_eta_clamp_trenta(self):
        # Th enorme -> eta grezza oltre 0,30 -> clampata a 0,30
        assert _F["mh655_eta_orc"](10000.0, 30.0, 0.45) == \
            pytest.approx(0.30)

    def test_eta_rifiuta_th_minore_uguale_tc(self):
        with pytest.raises(ValueError):
            _F["mh655_eta_orc"](30.0, 30.0, 0.45)
        with pytest.raises(ValueError):
            _F["mh655_eta_orc"](20.0, 30.0, 0.45)

    def test_eta_rifiuta_k_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh655_eta_orc"](280.0, 30.0, 1.5)


class TestEnergia:
    def test_potenza_demo(self):
        assert _F["mh655_potenza_elettrica"](500.0, ETA_DEMO) == \
            pytest.approx(P_EL_DEMO)

    def test_energia_lorda_demo(self):
        assert _F["mh655_energia_lorda"](P_EL_DEMO, 7000.0) == \
            pytest.approx(E_LORDA_DEMO)

    def test_energia_netta_demo(self):
        assert _F["mh655_energia_netta"](E_LORDA_DEMO, 8.0) == \
            pytest.approx(E_NETTA_DEMO)

    def test_calore_scaricato_demo(self):
        assert _F["mh655_calore_scaricato"](500.0, 7000.0,
                                            E_LORDA_DEMO) == \
            pytest.approx(Q_SCAR_DEMO)

    def test_calore_scaricato_non_negativo(self):
        # E_lorda impossibile > calore in -> 0, mai negativa
        assert _F["mh655_calore_scaricato"](500.0, 7000.0,
                                            1e12) == 0.0

    def test_prezzo_medio_demo(self):
        assert _F["mh655_prezzo_medio"](70.0, 0.22, 0.14) == \
            pytest.approx(P_MEDIO_DEMO)

    def test_prezzo_medio_bordi(self):
        assert _F["mh655_prezzo_medio"](0.0, 0.22, 0.14) == \
            pytest.approx(0.14)
        assert _F["mh655_prezzo_medio"](100.0, 0.22, 0.14) == \
            pytest.approx(0.22)

    def test_prezzo_medio_rifiuta_quota(self):
        with pytest.raises(ValueError):
            _F["mh655_prezzo_medio"](101.0, 0.22, 0.14)
        with pytest.raises(ValueError):
            _F["mh655_prezzo_medio"](-1.0, 0.22, 0.14)

    def test_capex_da_specifico(self):
        assert _F["mh655_capex_da_specifico"](100.0, 8000.0) == \
            pytest.approx(800000.0)
        with pytest.raises(ValueError):
            _F["mh655_capex_da_specifico"](100.0, -1.0)


class TestRisparmio:
    def test_risparmio_demo(self):
        assert _F["mh655_risparmio"](E_NETTA_DEMO, P_MEDIO_DEMO, 25000.0,
                                     5000.0) == pytest.approx(RISP_DEMO)

    def test_risparmio_senza_scarico(self):
        assert _F["mh655_risparmio"](1000.0, 0.20, 50.0) == \
            pytest.approx(150.0)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh655_risparmio"](100.0, 0.10, 300.0,
                                     5000.0) == pytest.approx(-5290.0)


class TestCo2:
    def test_co2_demo(self):
        assert _F["mh655_co2_t"](E_NETTA_DEMO, 0.30) == \
            pytest.approx(CO2_DEMO)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh655_flussi_esc"](CAPEX_DEMO, RISP_DEMO, 15, 2.0)

    def test_flussi_struttura(self):
        fl = _F["mh655_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_esc_struttura(self):
        # escalation 10 % su 3 anni: mano -> [-1000, 110, 121, 133.1]
        fl = _F["mh655_flussi_esc"](1000.0, 100.0, 3, 10.0)
        assert fl[0] == -1000.0
        assert fl[1:] == pytest.approx([110.0, 121.0, 133.1])

    def test_flussi_esc_zero_come_flussi(self):
        a = _F["mh655_flussi_esc"](CAPEX_DEMO, RISP_DEMO, 15, 0.0)
        b = _F["mh655_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        assert a == pytest.approx(b)

    def test_flussi_esc_rifiuta(self):
        with pytest.raises(ValueError):
            _F["mh655_flussi_esc"](1000.0, 100.0, 3, 31.0)
        with pytest.raises(ValueError):
            _F["mh655_flussi_esc"](1000.0, 100.0, 3, -1.0)

    def test_van_demo(self):
        assert _F["mh655_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh655_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh655_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh655_payback"](self._flussi_demo()) == 9

    def test_payback_none_mai(self):
        assert _F["mh655_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh655_verdetto"](RISP_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        assert _F["mh655_verdetto"](1000.0, -1500.0, 24000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh655_verdetto"](100.0, -5000.0, 24000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh655_verdetto"](0.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh655_verdetto"](-50.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        r = _F["mh655_demo_calcoli"]()
        assert r["eta_orc"] == pytest.approx(ETA_DEMO)
        assert r["p_el_kw"] == pytest.approx(P_EL_DEMO)
        assert r["e_lorda"] == pytest.approx(E_LORDA_DEMO)
        assert r["e_netta"] == pytest.approx(E_NETTA_DEMO)
        assert r["q_scaricato"] == pytest.approx(Q_SCAR_DEMO)
        assert r["p_medio"] == pytest.approx(P_MEDIO_DEMO)
        assert r["risparmio"] == pytest.approx(RISP_DEMO)
        assert r["co2_t"] == pytest.approx(CO2_DEMO)
        assert r["van"] == pytest.approx(VAN_DEMO)
        assert r["tir"] == pytest.approx(TIR_DEMO)
        assert r["payback"] == 9
        assert r["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE655 in self._app()

    def test_helpers_presenti(self):
        assert "# W655 (23/10/2026) - tab655" in self._app()

    def test_chain_bumpata(self):
        assert ", tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748 = st.tabs([" in self._app()

    def test_tab_count_655(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 748
        assert TITLE655 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab655" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab655" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st655_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st654_") for k in keys)

    def test_csv_filename(self):
        assert "orc.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W655 (23/10/2026)")[1].split("# W654 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
