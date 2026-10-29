"""Test tab639 "🧪🛢️ LOHC: l'idrogeno nei liquidi organici".

Demo calcolata a mano: 1000 t H2/anno su 8000 h -> 125 kg/h;
potenza PCI 125 x 33,33 = 4166,25 kW.
CAPEX idrogenazione 4166,25 x 250 = 1.041.562,50 €;
CAPEX deidrogenazione 4166,25 x 400 = 1.666.500,00 €.
Carrier: 1000/365 x 30 = 82,1918 t H2 di scorta / 0,062
= 1.325,6738842244806 t -> x 1000 x 4 = 5.302.695,536897923 €.
CRF(6 %, 20 a) = 0,0871845569768514.
Capitale annuo (1041562,5 + 1666500 + 5302695,536897923)
x 0,0871845569768514 = 698.413,68...; opex 3 % = 240.322,74...;
top-up carrier 2 % = 106.053,91...; calore 1000x1000x10/1000x40
= 400.000 €/anno; trasporto 1000/0,062 x 2 x 0,08 x 500
= 1.290.322,5806451614 €/anno.
Totale 2.735.113,622985755 €/anno -> adder 2,735113622985755 €/kg;
delivered 5,00 + 2,735113622985755 = 7,7351136229857556 €/kg;
target 6,50 toll 15 % (soglia 7,475) -> NON_CONVIENTE;
quota calore 400000/2735113,622985755 = 14,624620953163351 %.
Sensibilita': (250 km, 20 €/MWh) -> 6,889952332663174 MARGINALE;
(250 km, 40 €/MWh) -> 7,089952332663174 MARGINALE;
(500 km, 40 €/MWh) -> 7,7351136229857556 NON_CONVIENTE.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh639_num", "mh639_nneg", "mh639_pos", "mh639_frac01",
           "mh639_kg_h2_ora", "mh639_potenza_kw_lhv",
           "mh639_capex_idrogenazione", "mh639_capex_deidrogenazione",
           "mh639_carrier_t", "mh639_capex_carrier", "mh639_crf",
           "mh639_costo_calore_annuo", "mh639_costo_trasporto_annuo",
           "mh639_costo_annuo_totale", "mh639_adder_eur_kg",
           "mh639_delivered_eur_kg", "mh639_verdetto",
           "mh639_quota_calore_pct", "mh639_sensibilita", "mh639_demo")

TITLE639 = "🧪🛢️ LOHC: l'idrogeno nei liquidi organici"

KGH_DEMO = 125.0
PKW_DEMO = 4166.25
CXH_DEMO = 1041562.5
CXD_DEMO = 1666500.0
CAR_DEMO = 1325.6738842244806
CXC_DEMO = 5302695.536897923
CRF_DEMO = 0.0871845569768514
CC_DEMO = 400000.0
CT_DEMO = 1290322.5806451614
TOT_DEMO = 2735113.622985755
ADDER_DEMO = 2.735113622985755
DL_DEMO = 7.7351136229857556
QC_DEMO = 14.624620953163351
DL_250_20 = 6.889952332663174
DL_250_40 = 7.089952332663174


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh639_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh639_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh639_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh639_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh639_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh639_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh639_frac01"](1.0, "x") == 1.0
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh639_frac01"](bad, "x")


class TestCalcoli:
    def test_kg_h2_ora(self):
        assert _F["mh639_kg_h2_ora"](1000.0, 8000.0) == KGH_DEMO
        with pytest.raises(ValueError):
            _F["mh639_kg_h2_ora"](1000.0, 0.0)

    def test_potenza_kw_lhv(self):
        assert _F["mh639_potenza_kw_lhv"](KGH_DEMO) == PKW_DEMO

    def test_capex_idro_deidro(self):
        assert _F["mh639_capex_idrogenazione"](PKW_DEMO, 250.0) == CXH_DEMO
        assert _F["mh639_capex_deidrogenazione"](PKW_DEMO, 400.0) == CXD_DEMO

    def test_carrier(self):
        assert _F["mh639_carrier_t"](1000.0, 30.0, 6.2) == pytest.approx(
            CAR_DEMO)
        # capacita' doppia -> meta' carrier
        assert _F["mh639_carrier_t"](1000.0, 30.0, 12.4) == pytest.approx(
            CAR_DEMO / 2.0)
        with pytest.raises(ValueError):
            _F["mh639_carrier_t"](1000.0, 30.0, 0.0)

    def test_capex_carrier(self):
        assert _F["mh639_capex_carrier"](CAR_DEMO, 4.0) == pytest.approx(
            CXC_DEMO)

    def test_crf(self):
        assert _F["mh639_crf"](6.0, 20.0) == pytest.approx(CRF_DEMO)
        assert _F["mh639_crf"](0.0, 10.0) == 0.1

    def test_costo_calore(self):
        assert _F["mh639_costo_calore_annuo"](1000.0, 10.0, 40.0) == CC_DEMO
        # calore gratis -> costo nullo
        assert _F["mh639_costo_calore_annuo"](1000.0, 10.0, 0.0) == 0.0

    def test_costo_trasporto(self):
        assert _F["mh639_costo_trasporto_annuo"](1000.0, 6.2, 0.08,
                                               500.0) == pytest.approx(
                                                   CT_DEMO)
        # distanza nulla -> costo nullo
        assert _F["mh639_costo_trasporto_annuo"](1000.0, 6.2, 0.08,
                                               0.0) == 0.0

    def test_costo_totale(self):
        tot = _F["mh639_costo_annuo_totale"](CXH_DEMO, CXD_DEMO, CXC_DEMO,
                                            CRF_DEMO, 3.0, 2.0, CC_DEMO,
                                            CT_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        with pytest.raises(ValueError):
            _F["mh639_costo_annuo_totale"](CXH_DEMO, CXD_DEMO, CXC_DEMO,
                                           CRF_DEMO, 101.0, 2.0, CC_DEMO,
                                           CT_DEMO)

    def test_adder(self):
        assert _F["mh639_adder_eur_kg"](TOT_DEMO, 1000.0) == pytest.approx(
            ADDER_DEMO)
        assert _F["mh639_adder_eur_kg"](TOT_DEMO, 0.0) is None

    def test_delivered(self):
        assert _F["mh639_delivered_eur_kg"](5.0, ADDER_DEMO) == pytest.approx(
            DL_DEMO)
        assert _F["mh639_delivered_eur_kg"](5.0, None) is None

    def test_verdetto(self):
        v = _F["mh639_verdetto"]
        assert v(None, 6.5, 15.0) == "NON_CALCOLABILE"
        assert v(6.5, 6.5, 15.0) == "CONVIENTE"
        assert v(6.51, 6.5, 15.0) == "MARGINALE"
        assert v(7.475, 6.5, 15.0) == "MARGINALE"
        assert v(7.4751, 6.5, 15.0) == "NON_CONVIENTE"
        assert v(DL_DEMO, 6.5, 15.0) == "NON_CONVIENTE"

    def test_quota_calore(self):
        assert _F["mh639_quota_calore_pct"](CC_DEMO, TOT_DEMO) == pytest.approx(
            QC_DEMO)
        assert _F["mh639_quota_calore_pct"](100.0, 0.0) is None


class TestSensibilita:
    def _df(self):
        d = _F["mh639_demo"]()
        return _F["mh639_sensibilita"]([250.0, 500.0], [20.0, 40.0],
                                       d["t_h2_anno"], d["ore_anno"],
                                       d["lcoh_eur_kg"], d["tasso_pct"],
                                       d["anni"], d["capex_h_eur_kw"],
                                       d["capex_d_eur_kw"], d["opex_pct"],
                                       d["capacita_wt_pct"],
                                       d["carrier_eur_kg"],
                                       d["giorni_scorta"],
                                       d["perdite_carrier_pct"],
                                       d["calore_kwh_kg"],
                                       d["tariffa_eur_t_km"],
                                       d["target_eur_kg"], d["toll_pct"])

    def test_forma(self):
        df = self._df()
        assert len(df) == 4
        assert set(df.columns) == {"distanza_km", "prezzo_calore_eur_mwh",
                                   "adder_eur_kg", "delivered_eur_kg",
                                   "verdetto"}

    def test_valori(self):
        df = self._df()
        r = df.set_index(["distanza_km", "prezzo_calore_eur_mwh"])
        assert r.loc[(250.0, 20.0), "delivered_eur_kg"] == pytest.approx(
            DL_250_20)
        assert r.loc[(250.0, 20.0), "verdetto"] == "MARGINALE"
        assert r.loc[(250.0, 40.0), "delivered_eur_kg"] == pytest.approx(
            DL_250_40)
        assert r.loc[(250.0, 40.0), "verdetto"] == "MARGINALE"
        assert r.loc[(500.0, 40.0), "delivered_eur_kg"] == pytest.approx(
            DL_DEMO)
        assert r.loc[(500.0, 40.0), "verdetto"] == "NON_CONVIENTE"


class TestDemo:
    def test_demo_valori(self):
        d = _F["mh639_demo"]()
        assert d["t_h2_anno"] == 1000.0
        assert d["capacita_wt_pct"] == 6.2
        assert d["distanza_km"] == 500.0
        kgh = _F["mh639_kg_h2_ora"](d["t_h2_anno"], d["ore_anno"])
        assert kgh == KGH_DEMO
        pkw = _F["mh639_potenza_kw_lhv"](kgh)
        cxh = _F["mh639_capex_idrogenazione"](pkw, d["capex_h_eur_kw"])
        cxd = _F["mh639_capex_deidrogenazione"](pkw, d["capex_d_eur_kw"])
        car = _F["mh639_carrier_t"](d["t_h2_anno"], d["giorni_scorta"],
                                   d["capacita_wt_pct"])
        cxc = _F["mh639_capex_carrier"](car, d["carrier_eur_kg"])
        assert cxc == pytest.approx(CXC_DEMO)
        crf = _F["mh639_crf"](d["tasso_pct"], d["anni"])
        cc = _F["mh639_costo_calore_annuo"](d["t_h2_anno"],
                                            d["calore_kwh_kg"],
                                            d["prezzo_calore_eur_mwh"])
        ct = _F["mh639_costo_trasporto_annuo"](d["t_h2_anno"],
                                              d["capacita_wt_pct"],
                                              d["tariffa_eur_t_km"],
                                              d["distanza_km"])
        tot = _F["mh639_costo_annuo_totale"](cxh, cxd, cxc, crf,
                                             d["opex_pct"],
                                             d["perdite_carrier_pct"],
                                             cc, ct)
        assert tot == pytest.approx(TOT_DEMO)
        ad = _F["mh639_adder_eur_kg"](tot, d["t_h2_anno"])
        assert ad == pytest.approx(ADDER_DEMO)
        dl = _F["mh639_delivered_eur_kg"](d["lcoh_eur_kg"], ad)
        assert dl == pytest.approx(DL_DEMO)
        assert _F["mh639_verdetto"](dl, d["target_eur_kg"],
                                    d["toll_pct"]) == "NON_CONVIENTE"


class TestStruttura:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W639 (22/10/2026)")[1].split(
            "# W638 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab639:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 797
        assert TITLE639 in titles

    def test_registrazione(self):
        assert f'"{TITLE639}"' in self._src()
        assert ", tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797 = st.tabs([" in self._src()
        assert "with tab639:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st639_[a-z0-9_]+", self._ui()))
        attese = {"st639_t", "st639_ore", "st639_lcoh", "st639_cxh",
                  "st639_cxd", "st639_opex", "st639_tasso", "st639_anni",
                  "st639_wt", "st639_ckg", "st639_gs", "st639_pc",
                  "st639_kh", "st639_pq", "st639_tf", "st639_km",
                  "st639_tg", "st639_tol", "st639_sens", "st639_go",
                  "st639_fig", "st639_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st639_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
