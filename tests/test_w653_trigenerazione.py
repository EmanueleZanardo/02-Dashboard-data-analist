"""Test tab653 "❄️ Trigenerazione (CCHP): un solo combustibile, elettricita' + calore + freddo".

Demo calcolata a mano: CHP 500 kWe, 5.000 h/anno, eta_el 0,38, eta_th 0,45,
share freddo 50 %, COP assorbitore 0,7, eta caldaia 0,9, EER 3,0,
prezzo gas 0,08 €/kWh, prezzo el 0,22 €/kWh, O&M 0,012 €/kWh_el,
fattori CO2 gas 0,20 / el 0,35, CAPEX 800.000 €, 6 %, 15 anni.

- e_el = 500 x 5.000 = 2.500.000 kWh
- f = 2.500.000 / 0,38 = 6.578.947,368421053 kWh PCI
- q_th = 6.578.947,368421053 x 0,45 = 2.960.526,3157894737 kWh
- q_freddo = 2.960.526,3157894737 x 0,5 x 0,7 = 1.036.184,2105263157 kWh
- q_calore = 2.960.526,3157894737 x 0,5 = 1.480.263,1578947369 kWh
- C_base = 2.500.000 x 0,22 + 1.480.263,1578947369/0,9 x 0,08
         + 1.036.184,2105263157/3 x 0,22 = 757.565,7894736843 €
  (voci: 550.000 + 131.578,94736842107 + 75.986,84210526315)
- C_tri = 6.578.947,368421053 x 0,08 + 2.500.000 x 0,012
        = 556.315,7894736843 €
- risparmio = 201.250,0 €/anno
- CO2 base = (2.500.000x0,35 + 1.644.736,8421052632x0,20
            + 345.394,7368421053x0,35)/1000 = 1.324,8355263157894 t
  CO2 tri = 6.578.947,368421053 x 0,20/1000 = 1.315,7894736842106 t
  evitata = 9,046052631578732 t/anno
- flussi [-800.000, 201.250 x 15]; VAN(6 %) = 1.154.590,1087828726 €;
  TIR 0,24179209570395777; payback anno 4 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh653_num", "mh653_nneg", "mh653_pos", "mh653_int_pos",
           "mh653_frazione", "mh653_rendimento", "mh653_rendimenti",
           "mh653_cop_assorbitore", "mh653_bilancio", "mh653_costo_baseline",
           "mh653_costo_trigen", "mh653_risparmio", "mh653_co2_t",
           "mh653_flussi", "mh653_van", "mh653_tir", "mh653_payback",
           "mh653_verdetto", "mh653_demo", "mh653_demo_calcoli")

TITLE653 = ("❄️ Trigenerazione (CCHP): un solo combustibile, elettricita' "
            "+ calore + freddo")

E_EL_DEMO = 2500000.0
F_DEMO = 6578947.368421053
Q_TH_DEMO = 2960526.3157894737
Q_FREDDO_DEMO = 1036184.2105263157
Q_CALORE_DEMO = 1480263.1578947369
C_BASE_EL = 550000.0
C_BASE_CAL = 131578.94736842107
C_BASE_FRE = 75986.84210526315
C_BASE_TOT = 757565.7894736843
C_TRI_DEMO = 556315.7894736843
RISP_DEMO = 201250.0
CAPEX_DEMO = 800000.0
CO2_BASE = 1324.8355263157894
CO2_TRI = 1315.7894736842106
CO2_EVITATA = 9.046052631578732
VAN_DEMO = 1154590.1087828726
TIR_DEMO = 0.24179209570395777


def _bil_demo():
    return _F["mh653_bilancio"](500.0, 5000.0, 0.38, 0.45, 0.5, 0.7)


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh653_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh653_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh653_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh653_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh653_pos"](0, "x")
        assert _F["mh653_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh653_int_pos"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh653_int_pos"](15.5, "x")
        with pytest.raises(ValueError):
            _F["mh653_int_pos"](0, "x")

    def test_frazione_ok_e_limiti(self):
        assert _F["mh653_frazione"](0.5, "x") == 0.5
        assert _F["mh653_frazione"](0.0, "x") == 0.0
        assert _F["mh653_frazione"](1.0, "x") == 1.0
        for bad in (-0.01, 1.01, 2.0):
            with pytest.raises(ValueError):
                _F["mh653_frazione"](bad, "x")

    def test_rendimento_ok_e_limiti(self):
        assert _F["mh653_rendimento"](0.38, "x") == 0.38
        for bad in (0.0, 1.0, -0.1, 1.2):
            with pytest.raises(ValueError):
                _F["mh653_rendimento"](bad, "x")

    def test_rendimenti_somma_non_supera_uno(self):
        ee, et = _F["mh653_rendimenti"](0.38, 0.45)
        assert (ee, et) == (0.38, 0.45)
        with pytest.raises(ValueError):
            _F["mh653_rendimenti"](0.6, 0.5)  # somma 1,1 > 1

    def test_cop_assorbitore_ok_e_limiti(self):
        assert _F["mh653_cop_assorbitore"](0.7, "x") == 0.7
        assert _F["mh653_cop_assorbitore"](1.2, "x") == 1.2
        for bad in (0.29, 1.51, 0.0):
            with pytest.raises(ValueError):
                _F["mh653_cop_assorbitore"](bad, "x")


class TestBilancio:
    def test_bilancio_demo(self):
        b = _bil_demo()
        assert b["e_el"] == pytest.approx(E_EL_DEMO)
        assert b["f"] == pytest.approx(F_DEMO)
        assert b["q_th"] == pytest.approx(Q_TH_DEMO)
        assert b["q_freddo"] == pytest.approx(Q_FREDDO_DEMO)
        assert b["q_calore"] == pytest.approx(Q_CALORE_DEMO)

    def test_energia_conservata(self):
        # E_el + Q_th deve eguagliare F x (eta_el + eta_th)
        b = _F["mh653_bilancio"](100.0, 4000.0, 0.35, 0.45, 0.3, 0.7)
        assert b["e_el"] + b["q_th"] == pytest.approx(b["f"] * 0.80)

    def test_share_zero_nessun_freddo(self):
        b = _F["mh653_bilancio"](100.0, 4000.0, 0.35, 0.45, 0.0, 0.7)
        assert b["q_freddo"] == 0.0
        assert b["q_calore"] == pytest.approx(b["q_th"])

    def test_share_uno_tutto_freddo(self):
        b = _F["mh653_bilancio"](100.0, 4000.0, 0.35, 0.45, 1.0, 0.7)
        assert b["q_calore"] == 0.0
        assert b["q_freddo"] == pytest.approx(b["q_th"] * 0.7)

    def test_formula_q_freddo(self):
        b = _F["mh653_bilancio"](200.0, 3000.0, 0.40, 0.40, 0.6, 1.2)
        f = 200.0 * 3000.0 / 0.40
        assert b["q_freddo"] == pytest.approx(f * 0.40 * 0.6 * 1.2)


class TestCosti:
    def test_costo_baseline_demo(self):
        c = _F["mh653_costo_baseline"](_bil_demo(), 0.9, 3.0, 0.08, 0.22)
        assert c["elettricita_rete"] == pytest.approx(C_BASE_EL)
        assert c["calore_caldaia"] == pytest.approx(C_BASE_CAL)
        assert c["freddo_chiller"] == pytest.approx(C_BASE_FRE)
        assert c["totale"] == pytest.approx(C_BASE_TOT)

    def test_costo_trigen_demo(self):
        assert _F["mh653_costo_trigen"](_bil_demo(), 0.08,
                                        0.012) == pytest.approx(C_TRI_DEMO)

    def test_risparmio_demo(self):
        assert _F["mh653_risparmio"](C_BASE_TOT,
                                     C_TRI_DEMO) == pytest.approx(RISP_DEMO)

    def test_risparmio_negativo_gas_caro(self):
        # gas a 0,30 €/kWh: il trigeneratore costa piu' del baseline
        c_base = _F["mh653_costo_baseline"](_bil_demo(), 0.9, 3.0, 0.30, 0.22)
        c_tri = _F["mh653_costo_trigen"](_bil_demo(), 0.30, 0.012)
        assert _F["mh653_risparmio"](c_base["totale"], c_tri) < 0.0


class TestCo2:
    def test_co2_demo(self):
        co2 = _F["mh653_co2_t"](_bil_demo(), 0.9, 3.0, 0.20, 0.35)
        assert co2["base_t"] == pytest.approx(CO2_BASE)
        assert co2["trigen_t"] == pytest.approx(CO2_TRI)
        assert co2["evitata_t"] == pytest.approx(CO2_EVITATA)

    def test_co2_base_coerente_con_voci_costo(self):
        # stessa struttura del costo baseline, con fattori al posto dei prezzi
        co2 = _F["mh653_co2_t"](_bil_demo(), 0.9, 3.0, 0.20, 0.35)
        atteso = (E_EL_DEMO * 0.35 + Q_CALORE_DEMO / 0.9 * 0.20
                  + Q_FREDDO_DEMO / 3.0 * 0.35) / 1000.0
        assert co2["base_t"] == pytest.approx(atteso)


class TestFinanza:
    def test_flussi_forma(self):
        fl = _F["mh653_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        assert fl[0] == pytest.approx(-CAPEX_DEMO)
        assert len(fl) == 16
        assert all(f == pytest.approx(RISP_DEMO) for f in fl[1:])

    def test_van_demo(self):
        fl = _F["mh653_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        assert _F["mh653_van"](fl, 6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_tir_demo(self):
        fl = _F["mh653_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        tir = _F["mh653_tir"](fl)
        assert tir == pytest.approx(TIR_DEMO, abs=1e-4)
        npv = sum(f / (1.0 + tir) ** t for t, f in enumerate(fl))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh653_tir"]([1000.0, 100.0, 100.0]) is None
        assert _F["mh653_tir"]([-1000.0, -100.0, -100.0]) is None

    def test_payback_demo(self):
        fl = _F["mh653_flussi"](CAPEX_DEMO, RISP_DEMO, 15)
        assert _F["mh653_payback"](fl) == 4

    def test_payback_none_mai(self):
        assert _F["mh653_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviente(self):
        assert _F["mh653_verdetto"](RISP_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh653_verdetto"](1000.0, -70000.0, 800000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh653_verdetto"](1000.0, -90000.0, 800000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh653_verdetto"](0.0, 100.0, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh653_verdetto"](-50.0, None, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh653_demo_calcoli"]()
        assert c["bilancio_kwh"]["e_el"] == pytest.approx(E_EL_DEMO)
        assert c["bilancio_kwh"]["f"] == pytest.approx(F_DEMO)
        assert c["bilancio_kwh"]["q_freddo"] == pytest.approx(Q_FREDDO_DEMO)
        assert c["bilancio_kwh"]["q_calore"] == pytest.approx(Q_CALORE_DEMO)
        assert c["costo_base_eur"]["totale"] == pytest.approx(C_BASE_TOT)
        assert c["costo_trigen_eur"] == pytest.approx(C_TRI_DEMO)
        assert c["risparmio_eur"] == pytest.approx(RISP_DEMO)
        assert c["co2_t"]["evitata_t"] == pytest.approx(CO2_EVITATA)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 4
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE653 in self._app()

    def test_helpers_presenti(self):
        assert "# W653 (23/10/2026) - tab653" in self._app()

    def test_chain_bumpata(self):
        assert ", tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761 = st.tabs([" in self._app()

    def test_tab_count_653(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 761
        assert TITLE653 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab653" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab653" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st653_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 19
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st652_") for k in keys)

    def test_csv_filename(self):
        assert "trigenerazione.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W653 (23/10/2026)")[1].split("# W652 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
