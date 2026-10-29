"""Test tab641 "🧊❄️ Telerifreddamento (district cooling): centrale frigorifera vs chiller".

Demo calcolata a mano: domanda 30.000 MWh/anno, perdite 6 %
-> 31.914,8936 MWh da produrre in centrale.
COP chiller 2,8 -> 10.714,2857 MWh/anno; COP centrale 5,5
-> 5.802,7079 MWh/anno.
CAPEX DC: centrale 5 M€ + rete 2.000 m x 800 €/m = 6,6 M€;
CAPEX chiller evitato: 12.000 kW_f x 250 €/kW = 3 M€.
CRF(6 %, 25 a) = 0,07822671821227395; capex annuo DC 516.296,34 €;
costo annuo DC = 516.296,34 + 350.000 + 5.802,7079 x 140
= 1.678.675,450452459 €; costo netto = 55,9558483484153 €/MWh_f.
Costo annuo chiller = 234.680,15 + 120.000 + 1.500.000
= 1.854.680,1546368222 €; benchmark = 61,82267182122741 €/MWh_f
-> CONVIENTE (tolleranza 10 %).
Investimento incrementale = 3.600.000 €; risparmio annuo
= 1.620.000 - 1.162.379,1102514506 = 457.620,88974854944 €.
Flussi [-3.600.000, 457.620,89 x 25]: VAN(6 %) = 2.249.930,8191193845 €;
TIR = 0,11956680920443252 (11,9567 %); payback anno 8.
Quota elettricita' = 812.379,11 / 1.678.675,45 = 48,3940543737914 %.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh641_num", "mh641_nneg", "mh641_pos", "mh641_pct100",
           "mh641_domanda_rete_mwh", "mh641_energia_elettrica_mwh",
           "mh641_capex_totale_dc", "mh641_capex_chiller_evitato",
           "mh641_crf", "mh641_capex_annuo", "mh641_costo_annuo_dc",
           "mh641_costo_annuo_chiller", "mh641_costo_netto_eur_mwh",
           "mh641_costo_benchmark_eur_mwh", "mh641_investimento_netto",
           "mh641_risparmio_annuo", "mh641_flussi", "mh641_van",
           "mh641_tir", "mh641_payback", "mh641_verdetto",
           "mh641_quota_elettricita_pct", "mh641_sensibilita",
           "mh641_demo_calcoli", "mh641_demo")

TITLE641 = ("🧊❄️ Telerifreddamento (district cooling): centrale frigorifera "
            "vs chiller")

RETE_DEMO = 31914.89361702128
EIND_DEMO = 10714.285714285716
ECENT_DEMO = 5802.7079303675055
CXTOT_DEMO = 6600000.0
CXCH_DEMO = 3000000.0
CRF_DEMO = 0.07822671821227395
CDC_DEMO = 1678675.450452459
CCH_DEMO = 1854680.1546368222
NC_DEMO = 55.9558483484153
BENCH_DEMO = 61.82267182122741
INV_DEMO = 3600000.0
RIS_DEMO = 457620.88974854944
VAN_DEMO = 2249930.8191193845
TIR_DEMO = 0.11956680920443252
PB_DEMO = 8
QE_DEMO = 48.3940543737914


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh641_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh641_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh641_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh641_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh641_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh641_pos"](0, "x")

    def test_pct100(self):
        assert _F["mh641_pct100"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh641_pct100"](bad, "x")


class TestCalcoli:
    def test_domanda_rete(self):
        assert _F["mh641_domanda_rete_mwh"](30000.0, 6.0) == pytest.approx(
            RETE_DEMO)
        assert _F["mh641_domanda_rete_mwh"](30000.0, 0.0) == 30000.0
        with pytest.raises(ValueError):
            _F["mh641_domanda_rete_mwh"](30000.0, 100.0)

    def test_energia_elettrica(self):
        assert _F["mh641_energia_elettrica_mwh"](30000.0, 2.8) == pytest.approx(
            EIND_DEMO)
        with pytest.raises(ValueError):
            _F["mh641_energia_elettrica_mwh"](30000.0, 0.0)

    def test_capex(self):
        assert _F["mh641_capex_totale_dc"](5e6, 2000.0, 800.0) == CXTOT_DEMO
        assert _F["mh641_capex_chiller_evitato"](12000.0, 250.0) == CXCH_DEMO

    def test_crf(self):
        assert _F["mh641_crf"](6.0, 25) == pytest.approx(CRF_DEMO)
        assert _F["mh641_crf"](0.0, 25) == pytest.approx(0.04)

    def test_capex_annuo(self):
        assert _F["mh641_capex_annuo"](6600000.0, 6.0, 25) == pytest.approx(
            516296.340200613)

    def test_costi_annui(self):
        assert _F["mh641_costo_annuo_dc"](516296.340200613, 350000.0,
                                          ECENT_DEMO, 140.0) == pytest.approx(
            CDC_DEMO)
        assert _F["mh641_costo_annuo_chiller"](234680.154636822, 120000.0,
                                               EIND_DEMO, 140.0) == pytest.approx(
            CCH_DEMO)

    def test_costo_netto_e_benchmark(self):
        assert _F["mh641_costo_netto_eur_mwh"](CDC_DEMO, 30000.0) == pytest.approx(
            NC_DEMO)
        assert _F["mh641_costo_netto_eur_mwh"](CDC_DEMO, 0.0) is None
        assert _F["mh641_costo_benchmark_eur_mwh"](
            CCH_DEMO, 30000.0) == pytest.approx(BENCH_DEMO)

    def test_investimento_e_risparmio(self):
        assert _F["mh641_investimento_netto"](6600000.0, 3000000.0) == INV_DEMO
        assert _F["mh641_risparmio_annuo"](EIND_DEMO, ECENT_DEMO, 140.0,
                                           120000.0, 350000.0) == pytest.approx(
            RIS_DEMO)

    def test_flussi_van_tir_payback(self):
        fl = _F["mh641_flussi"](INV_DEMO, RIS_DEMO, 25)
        assert len(fl) == 26 and fl[0] == -INV_DEMO and fl[1] == pytest.approx(
            RIS_DEMO)
        assert _F["mh641_van"](fl, 6.0) == pytest.approx(VAN_DEMO)
        assert _F["mh641_tir"](fl) == pytest.approx(TIR_DEMO)
        assert _F["mh641_payback"](fl) == PB_DEMO

    def test_tir_payback_degeneri(self):
        assert _F["mh641_tir"]([-100.0, -10.0, -10.0]) is None
        assert _F["mh641_payback"]([-100.0, -10.0, -10.0]) is None

    def test_verdetto(self):
        v = _F["mh641_verdetto"]
        assert v(NC_DEMO, BENCH_DEMO, 10.0) == "CONVIENTE"
        assert v(64.0, BENCH_DEMO, 10.0) == "MARGINALE"
        assert v(70.0, BENCH_DEMO, 10.0) == "NON_CONVIENTE"
        assert v(None, BENCH_DEMO, 10.0) == "NON_CALCOLABILE"
        assert v(NC_DEMO, None, 10.0) == "NON_CALCOLABILE"

    def test_quota_elettricita(self):
        assert _F["mh641_quota_elettricita_pct"](ECENT_DEMO * 140.0,
                                                 CDC_DEMO) == pytest.approx(
            QE_DEMO)
        assert _F["mh641_quota_elettricita_pct"](0.0, 0.0) == 0.0

    def test_sensibilita(self):
        p = _F["mh641_demo"]()
        righe = _F["mh641_sensibilita"](p, [120.0, 140.0], [5.0, 5.5])
        assert len(righe) == 4
        r0 = righe[0]
        assert r0["prezzo_eur_mwh"] == 120.0 and r0["cop_centrale"] == 5.0
        assert r0["costo_netto_eur_mwh"] > 0.0
        assert r0["verdetto"] in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                                  "NON_CALCOLABILE")

    def test_demo_calcoli_completi(self):
        d = _F["mh641_demo_calcoli"](_F["mh641_demo"]())
        assert d["costo_netto_eur_mwh"] == pytest.approx(NC_DEMO)
        assert d["costo_benchmark_eur_mwh"] == pytest.approx(BENCH_DEMO)
        assert d["van_eur"] == pytest.approx(VAN_DEMO)
        assert d["tir"] == pytest.approx(TIR_DEMO)
        assert d["payback_anni"] == PB_DEMO
        assert d["verdetto"] == "CONVIENTE"
        assert d["quota_elettricita_pct"] == pytest.approx(QE_DEMO)


class TestRegistrazione:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W641 (22/10/2026)")[1].split(
            "# W640 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab641:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 791
        assert TITLE641 in titles

    def test_registrazione(self):
        assert f'"{TITLE641}"' in self._src()
        assert ", tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791 = st.tabs([" in self._src()
        assert "with tab641:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st641_[a-z0-9_]+", self._ui()))
        attese = {"st641_dom", "st641_perd", "st641_copi", "st641_copc",
                  "st641_pene", "st641_cxc", "st641_rete", "st641_eurm",
                  "st641_oxc", "st641_oxh", "st641_picco", "st641_eurkw",
                  "st641_tasso", "st641_anni", "st641_toll", "st641_sens",
                  "st641_go", "st641_fig1", "st641_fig2", "st641_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st641_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
