"""Test tab638 "💛 Idrogeno giallo: l'elettrolisi alimentata dal fotovoltaico".

Demo calcolata a mano: FV 5 MWp a 1300 ore equivalenti/anno (6500 MWh),
elettrolizzatore 4 MW (4000 kW) -> assorbibile 4 x 1300 = 5200 MWh;
energia H2 = min(6500, 5200) = 5200 MWh; surplus 1300 MWh.
t H2 = 5200 / 55 = 94,54545454545455 t/anno; utilizzazione 100,0 %.
CAPEX FV 5 x 1000 x 700 = 3,5 M€; elettrolizzatore 4000 x 900 = 3,6 M€
(totale 7,1 M€); CRF(6 %, 25 a) = 0,07822671821227395;
capitale annuo 7,1e6 x 0,07822671821227395 = 555.409,6993071451 €/anno;
OPEX 3,5e6 x 0,03 + 3,6e6 x 0,04 = 249.000 €/anno;
ricavo surplus 1300 x 60 = 78.000 €/anno;
LCOH (555409,6993071451 + 249000 - 78000) / 94,54545454545455
= 7.683,179511902496 €/t (7,683179511902496 €/kg);
margine (6000 - 7683,179511902496) x 94,54545454545455
= -159.136,97203441785 €/anno; payback None;
verdetto 7683,18 > 6000 x 1,20 -> NON_CONVIENTE.
Sensibilita': (1100 h, 50 kWh/kg) -> 88,0 t, LCOH 8.391,019310308468,
NON_CONVIENTE; (1500 h, 50) -> 120,0 t, LCOH 5.953,414160892876,
CONVIENTE; (1500 h, 55) -> 109,090909 t, LCOH 6.548,755576982163,
MARGINALE.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh638_num", "mh638_nneg", "mh638_pos", "mh638_frac01",
           "mh638_energia_pv_mwh", "mh638_energia_h2_mwh",
           "mh638_surplus_mwh", "mh638_h2_t_anno",
           "mh638_utilizzazione_ely_pct", "mh638_capex_totale",
           "mh638_crf", "mh638_capitale_annuo", "mh638_opex_annuo",
           "mh638_ricavo_surplus_eur", "mh638_lcoh_eur_t",
           "mh638_margine_annuo_eur", "mh638_payback_anni",
           "mh638_verdetto", "mh638_sensibilita", "mh638_demo")

TITLE638 = "💛 Idrogeno giallo: l'elettrolisi alimentata dal fotovoltaico"

EPV_DEMO = 6500.0
EH2_DEMO = 5200.0
SUR_DEMO = 1300.0
T_DEMO = 94.54545454545455
UT_DEMO = 100.0
CAPEX_DEMO = 7100000.0
CRF_DEMO = 0.07822671821227395
CAP_ANN_DEMO = 555409.6993071451
OPEX_DEMO = 249000.0
RS_DEMO = 78000.0
LCOH_DEMO = 7683.179511902496
LCOHKG_DEMO = 7.683179511902496
MARGINE_DEMO = -159136.97203441785
LCOH_1100_50 = 8391.019310308468
LCOH_1500_50 = 5953.414160892876
LCOH_1500_55 = 6548.755576982163


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh638_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh638_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh638_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh638_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh638_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh638_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh638_frac01"](1.0, "x") == 1.0
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh638_frac01"](bad, "x")


class TestCalcoli:
    def test_energia_pv(self):
        assert _F["mh638_energia_pv_mwh"](5.0, 1300.0) == EPV_DEMO

    def test_energia_h2_limitata_da_elettrolizzatore(self):
        # FV 6500 MWh ma l'unita' puo' assorbire solo 4 x 1300 = 5200
        assert _F["mh638_energia_h2_mwh"](5.0, 1300.0, 4000.0) == EH2_DEMO

    def test_energia_h2_limitata_da_fv(self):
        # FV piccola, elettrolizzatore sovradimensionato: min = energia FV
        assert _F["mh638_energia_h2_mwh"](1.0, 1000.0, 10000.0) == 1000.0

    def test_surplus(self):
        assert _F["mh638_surplus_mwh"](5.0, 1300.0, 4000.0) == SUR_DEMO
        assert _F["mh638_surplus_mwh"](1.0, 1000.0, 10000.0) == 0.0

    def test_h2_t(self):
        assert _F["mh638_h2_t_anno"](5200.0, 55.0) == pytest.approx(T_DEMO)
        with pytest.raises(ValueError):
            _F["mh638_h2_t_anno"](5200.0, 0.0)

    def test_utilizzazione(self):
        assert _F["mh638_utilizzazione_ely_pct"](5200.0, 4000.0,
                                                1300.0) == UT_DEMO
        assert _F["mh638_utilizzazione_ely_pct"](0.0, 0.0, 1300.0) is None
        assert _F["mh638_utilizzazione_ely_pct"](100.0, 4000.0, 0.0) is None

    def test_capex(self):
        assert _F["mh638_capex_totale"](5.0, 700.0, 4000.0,
                                        900.0) == CAPEX_DEMO

    def test_crf(self):
        assert _F["mh638_crf"](6.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh638_crf"](0.0, 10.0) == 0.1

    def test_capitale(self):
        assert _F["mh638_capitale_annuo"](CAPEX_DEMO, 6.0,
                                          25.0) == pytest.approx(
                                              CAP_ANN_DEMO)

    def test_opex(self):
        assert _F["mh638_opex_annuo"](3500000.0, 3.0, 3600000.0,
                                      4.0) == OPEX_DEMO

    def test_ricavo_surplus(self):
        assert _F["mh638_ricavo_surplus_eur"](1300.0, 60.0) == RS_DEMO

    def test_lcoh(self):
        assert _F["mh638_lcoh_eur_t"](CAP_ANN_DEMO, OPEX_DEMO, RS_DEMO,
                                     T_DEMO) == pytest.approx(LCOH_DEMO)
        assert _F["mh638_lcoh_eur_t"](1.0, 1.0, 0.0, 0.0) is None

    def test_margine_e_payback(self):
        assert _F["mh638_margine_annuo_eur"](LCOH_DEMO, 6000.0,
                                             T_DEMO) == pytest.approx(
                                                 MARGINE_DEMO)
        assert _F["mh638_payback_anni"](CAPEX_DEMO,
                                        MARGINE_DEMO) is None
        assert _F["mh638_payback_anni"](1000.0, 500.0) == 2.0

    def test_verdetto(self):
        v = _F["mh638_verdetto"]
        assert v(None, 6000.0, 20.0) == "NON_CALCOLABILE"
        assert v(6000.0, 6000.0, 20.0) == "CONVIENTE"
        assert v(6000.01, 6000.0, 20.0) == "MARGINALE"
        assert v(7200.0, 6000.0, 20.0) == "MARGINALE"
        assert v(7200.01, 6000.0, 20.0) == "NON_CONVIENTE"
        assert v(LCOH_DEMO, 6000.0, 20.0) == "NON_CONVIENTE"


class TestSensibilita:
    def _df(self):
        d = _F["mh638_demo"]()
        return _F["mh638_sensibilita"]([1100.0, 1500.0], [50.0, 55.0],
                                       d["p_pv_mwp"], d["p_ely_kw"],
                                       d["capex_pv_eur_kwp"],
                                       d["capex_ely_eur_kw"],
                                       d["opex_pv_pct"], d["opex_ely_pct"],
                                       d["tasso_pct"], d["anni"],
                                       d["prezzo_surplus_eur_mwh"],
                                       d["prezzo_h2_grigio_eur_t"],
                                       d["premium_toll_pct"])

    def test_forma(self):
        df = self._df()
        assert len(df) == 4
        assert set(df.columns) == {"ore_equivalenti", "consumo_kwh_per_kg",
                                   "h2_t_anno", "lcoh_eur_t", "verdetto"}

    def test_valori(self):
        df = self._df()
        r = df.set_index(["ore_equivalenti", "consumo_kwh_per_kg"])
        assert r.loc[(1100.0, 50.0), "h2_t_anno"] == 88.0
        assert r.loc[(1100.0, 50.0), "lcoh_eur_t"] == pytest.approx(
            LCOH_1100_50)
        assert r.loc[(1100.0, 50.0), "verdetto"] == "NON_CONVIENTE"
        assert r.loc[(1500.0, 50.0), "h2_t_anno"] == 120.0
        assert r.loc[(1500.0, 50.0), "lcoh_eur_t"] == pytest.approx(
            LCOH_1500_50)
        assert r.loc[(1500.0, 50.0), "verdetto"] == "CONVIENTE"
        assert r.loc[(1500.0, 55.0), "h2_t_anno"] == pytest.approx(
            109.09090909090909)
        assert r.loc[(1500.0, 55.0), "lcoh_eur_t"] == pytest.approx(
            LCOH_1500_55)
        assert r.loc[(1500.0, 55.0), "verdetto"] == "MARGINALE"

    def test_liste_vuote(self):
        d = _F["mh638_demo"]()
        args = (d["p_pv_mwp"], d["p_ely_kw"], d["capex_pv_eur_kwp"],
                d["capex_ely_eur_kw"], d["opex_pv_pct"], d["opex_ely_pct"],
                d["tasso_pct"], d["anni"], d["prezzo_surplus_eur_mwh"],
                d["prezzo_h2_grigio_eur_t"], d["premium_toll_pct"])
        # ore equivalenti nulle -> produzione nulla -> LCOH None
        df = _F["mh638_sensibilita"]([0.0], [55.0], *args)
        assert df.iloc[0]["lcoh_eur_t"] is None
        assert df.iloc[0]["verdetto"] == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_valori(self):
        d = _F["mh638_demo"]()
        assert d["p_pv_mwp"] == 5.0
        assert d["ore_eq_pv"] == 1300.0
        assert d["p_ely_kw"] == 4000.0
        assert d["kwh_per_kg"] == 55.0
        epv = _F["mh638_energia_pv_mwh"](d["p_pv_mwp"], d["ore_eq_pv"])
        assert epv == EPV_DEMO
        t = _F["mh638_h2_t_anno"](
            _F["mh638_energia_h2_mwh"](d["p_pv_mwp"], d["ore_eq_pv"],
                                       d["p_ely_kw"]),
            d["kwh_per_kg"])
        assert t == pytest.approx(T_DEMO)
        cx = _F["mh638_capex_totale"](d["p_pv_mwp"], d["capex_pv_eur_kwp"],
                                      d["p_ely_kw"],
                                      d["capex_ely_eur_kw"])
        assert cx == CAPEX_DEMO
        cap = _F["mh638_capitale_annuo"](cx, d["tasso_pct"], d["anni"])
        op = _F["mh638_opex_annuo"](d["p_pv_mwp"] * 1000.0
                                    * d["capex_pv_eur_kwp"],
                                    d["opex_pv_pct"],
                                    d["p_ely_kw"] * d["capex_ely_eur_kw"],
                                    d["opex_ely_pct"])
        rs = _F["mh638_ricavo_surplus_eur"](
            _F["mh638_surplus_mwh"](d["p_pv_mwp"], d["ore_eq_pv"],
                                    d["p_ely_kw"]),
            d["prezzo_surplus_eur_mwh"])
        lcoh = _F["mh638_lcoh_eur_t"](cap, op, rs, t)
        assert lcoh == pytest.approx(LCOH_DEMO)
        assert _F["mh638_verdetto"](lcoh, d["prezzo_h2_grigio_eur_t"],
                                    d["premium_toll_pct"]) == \
            "NON_CONVIENTE"


class TestStruttura:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W638 (22/10/2026)")[1].split(
            "# W637 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab638:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 746
        assert TITLE638 in titles

    def test_registrazione(self):
        assert f'"{TITLE638}"' in self._src()
        assert ", tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746 = st.tabs([" in self._src()
        assert "with tab638:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st638_[a-z0-9_]+", self._ui()))
        attese = {"st638_mwp", "st638_ore", "st638_kw", "st638_kwh",
                  "st638_cpv", "st638_cel", "st638_opv", "st638_oel",
                  "st638_tasso", "st638_anni", "st638_sur", "st638_grigio",
                  "st638_tol", "st638_sens", "st638_go", "st638_fig",
                  "st638_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st638_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
