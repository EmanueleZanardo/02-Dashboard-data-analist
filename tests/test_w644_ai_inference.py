"""Test tab644 "🤖⚡ Inferenza AI: dal MW delle GPU al costo per milione di token".

Demo calcolata a mano: 1.000 GPU da 700 W, PUE 1,35, utilizzo 60 %,
2.000 token/s/GPU, 8.760 h/anno.
-> potenza IT 1.000 x 700 / 1e6 = 0,7 MW; potenza totale 0,7 x 1,35 = 0,945 MW;
energia annua 0,945 x 8.760 = 8.278,2 MWh/anno.
Token annui 1.000 x 2.000 x 3.600 x 8.760 x 0,6 = 3,78432e13
= 37.843.200 Mtoken/anno; energia per Mtoken 8.278.200 / 37.843.200
= 0,21875 kWh/Mtoken.
Costo energia 8.278,2 x 90 = 745.038,0 €/anno; CAPEX 1.000 x 28.000
= 28.000.000 €; CRF(8 %, 5 a) = 0,2504564545668364; capex annuo
= 7.012.780,727871419 €; OPEX 28.000.000 x 0,08 = 2.240.000 €;
TCO = 9.997.818,727871418 €/anno; costo/Mtoken = 9.997.818,73 / 37.843.200
= 0,2641906267934905 €/Mtoken.
Margine = (1,20 - 0,2641906267934905) x 37.843.200 = 35.414.021,27212858 €/anno.
Quota energia = 745.038 / 9.997.818,73 = 7,452005485186687 %.
Emissioni = 8.278,2 x 250 / 1.000 = 2.069,55 tCO2/anno.
Flussi [-28.000.000, 35.414.021,27 x 5]: VAN(8 %) = 113.397.918,1865246 €;
TIR = 1,2424830593834195 (124,25 %); payback anno 1 -> CONVIENTE
(tolleranza 10 %).
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh644_num", "mh644_nneg", "mh644_pos", "mh644_pct100",
           "mh644_int_pos", "mh644_pue", "mh644_potenza_it_mw",
           "mh644_potenza_tot_mw", "mh644_energia_annua_mwh",
           "mh644_token_annui", "mh644_energia_per_mtoken_kwh",
           "mh644_costo_energia_annuo", "mh644_capex_tot", "mh644_crf",
           "mh644_capex_annuo", "mh644_opex_annuo", "mh644_tco_annuo",
           "mh644_costo_per_mtoken_eur", "mh644_margine_annuo",
           "mh644_quota_energia_pct", "mh644_emissioni_tco2", "mh644_flussi",
           "mh644_van", "mh644_tir", "mh644_payback", "mh644_verdetto",
           "mh644_sensibilita", "mh644_demo_calcoli", "mh644_demo")

TITLE644 = ("🤖⚡ Inferenza AI: dal MW delle GPU al costo per milione "
            "di token")

PIT_DEMO = 0.7
PTOT_DEMO = 0.945
EN_DEMO = 8278.2
TOK_DEMO = 3.78432e13
MTOK_DEMO = 37843200.0
KWHMT_DEMO = 0.21875
CE_DEMO = 745038.0
CX_DEMO = 28000000.0
CRF_DEMO = 0.2504564545668364
CXA_DEMO = 7012780.727871419
OPX_DEMO = 2240000.0
TCO_DEMO = 9997818.727871418
CMT_DEMO = 0.2641906267934905
MA_DEMO = 35414021.27212858
QE_DEMO = 7.452005485186687
EMI_DEMO = 2069.55
VAN_DEMO = 113397918.1865246
TIR_DEMO = 1.2424830593834195
PB_DEMO = 1


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh644_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh644_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh644_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh644_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh644_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh644_pos"](0.0, "x")

    def test_pct100(self):
        assert _F["mh644_pct100"](100, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh644_pct100"](100.1, "x")

    def test_int_pos(self):
        assert _F["mh644_int_pos"](1000, "x") == 1000
        assert _F["mh644_int_pos"](1000.0, "x") == 1000
        for bad in (0, -5, 3.5, "1000"):
            with pytest.raises(ValueError):
                _F["mh644_int_pos"](bad, "x")

    def test_pue(self):
        assert _F["mh644_pue"](1.0, "pue") == 1.0
        assert _F["mh644_pue"](1.35, "pue") == 1.35
        with pytest.raises(ValueError):
            _F["mh644_pue"](0.99, "pue")


class TestCalcoli:
    def test_potenza(self):
        assert _F["mh644_potenza_it_mw"](1000, 700.0) == pytest.approx(PIT_DEMO)
        assert _F["mh644_potenza_tot_mw"](PIT_DEMO, 1.35) \
            == pytest.approx(PTOT_DEMO)
        assert _F["mh644_potenza_tot_mw"](PIT_DEMO, 1.0) == PIT_DEMO
        with pytest.raises(ValueError):
            _F["mh644_potenza_tot_mw"](PIT_DEMO, 0.99)

    def test_energia_e_token(self):
        assert _F["mh644_energia_annua_mwh"](PTOT_DEMO, 8760.0) \
            == pytest.approx(EN_DEMO)
        assert _F["mh644_token_annui"](1000, 2000.0, 8760.0, 60.0) \
            == pytest.approx(TOK_DEMO)
        assert _F["mh644_token_annui"](1000, 2000.0, 8760.0, 0.0) == 0.0

    def test_energia_per_mtoken(self):
        assert _F["mh644_energia_per_mtoken_kwh"](EN_DEMO, TOK_DEMO) \
            == pytest.approx(KWHMT_DEMO)
        assert _F["mh644_energia_per_mtoken_kwh"](EN_DEMO, 0.0) is None

    def test_costi(self):
        assert _F["mh644_costo_energia_annuo"](EN_DEMO, 90.0) \
            == pytest.approx(CE_DEMO)
        assert _F["mh644_capex_tot"](1000, 28000.0) == pytest.approx(CX_DEMO)
        assert _F["mh644_crf"](8.0, 5) == pytest.approx(CRF_DEMO)
        assert _F["mh644_crf"](0.0, 5) == pytest.approx(1.0 / 5)
        assert _F["mh644_capex_annuo"](CX_DEMO, 8.0, 5) \
            == pytest.approx(CXA_DEMO)
        assert _F["mh644_opex_annuo"](CX_DEMO, 8.0) == pytest.approx(OPX_DEMO)
        assert _F["mh644_tco_annuo"](CXA_DEMO, OPX_DEMO, CE_DEMO) \
            == pytest.approx(TCO_DEMO)
        assert _F["mh644_costo_per_mtoken_eur"](TCO_DEMO, TOK_DEMO) \
            == pytest.approx(CMT_DEMO)
        assert _F["mh644_costo_per_mtoken_eur"](TCO_DEMO, 0.0) is None

    def test_margine_quota_emissioni(self):
        assert _F["mh644_margine_annuo"](1.20, CMT_DEMO, TOK_DEMO) \
            == pytest.approx(MA_DEMO)
        assert _F["mh644_margine_annuo"](1.20, None, TOK_DEMO) is None
        assert _F["mh644_quota_energia_pct"](CE_DEMO, TCO_DEMO) \
            == pytest.approx(QE_DEMO)
        assert _F["mh644_quota_energia_pct"](0.0, 0.0) == 0.0
        assert _F["mh644_emissioni_tco2"](EN_DEMO, 250.0) \
            == pytest.approx(EMI_DEMO)

    def test_flussi_van_tir_payback(self):
        fl = _F["mh644_flussi"](CX_DEMO, MA_DEMO, 5)
        assert fl[0] == -CX_DEMO and len(fl) == 6
        assert _F["mh644_van"](fl, 8.0) == pytest.approx(VAN_DEMO)
        assert _F["mh644_tir"](fl) == pytest.approx(TIR_DEMO)
        assert _F["mh644_payback"](fl) == PB_DEMO

    def test_tir_payback_degeneri(self):
        assert _F["mh644_tir"]([-100.0, -50.0, -10.0]) is None
        assert _F["mh644_tir"]([100.0, 50.0, 10.0]) is None
        assert _F["mh644_payback"]([-100.0, 10.0, 10.0]) is None

    def test_verdetto(self):
        assert _F["mh644_verdetto"](100.0, CX_DEMO, 10.0) == "CONVIENTE"
        assert _F["mh644_verdetto"](-100000.0, CX_DEMO, 10.0) == "MARGINALE"
        assert _F["mh644_verdetto"](-10000000.0, CX_DEMO, 10.0) == "NON_CONVIENTE"
        assert _F["mh644_verdetto"](None, CX_DEMO, 10.0) == "NON_CALCOLABILE"

    def test_sensibilita(self):
        p = _F["mh644_demo"]()
        righe = _F["mh644_sensibilita"](p, [90.0, 100.0], [60.0, 70.0])
        assert len(righe) == 4
        r = righe[1]
        assert r["prezzo_energia_eur_mwh"] == 90.0
        assert r["utilizzo_pct"] == 70.0
        assert set(r.keys()) == {"prezzo_energia_eur_mwh", "utilizzo_pct",
                                 "margine_annuo_eur", "verdetto"}
        assert righe[0]["margine_annuo_eur"] == pytest.approx(MA_DEMO)

    def test_demo_calcoli_completi(self):
        d = _F["mh644_demo_calcoli"](_F["mh644_demo"]())
        assert d["potenza_it_mw"] == pytest.approx(PIT_DEMO)
        assert d["potenza_tot_mw"] == pytest.approx(PTOT_DEMO)
        assert d["energia_annua_mwh"] == pytest.approx(EN_DEMO)
        assert d["token_annui"] == pytest.approx(TOK_DEMO)
        assert d["mtoken_annui"] == pytest.approx(MTOK_DEMO)
        assert d["kwh_per_mtoken"] == pytest.approx(KWHMT_DEMO)
        assert d["costo_energia_eur"] == pytest.approx(CE_DEMO)
        assert d["capex_tot_eur"] == pytest.approx(CX_DEMO)
        assert d["capex_annuo_eur"] == pytest.approx(CXA_DEMO)
        assert d["opex_annuo_eur"] == pytest.approx(OPX_DEMO)
        assert d["tco_annuo_eur"] == pytest.approx(TCO_DEMO)
        assert d["costo_per_mtoken_eur"] == pytest.approx(CMT_DEMO)
        assert d["margine_annuo_eur"] == pytest.approx(MA_DEMO)
        assert d["van_eur"] == pytest.approx(VAN_DEMO)
        assert d["tir"] == pytest.approx(TIR_DEMO)
        assert d["payback_anni"] == PB_DEMO
        assert d["verdetto"] == "CONVIENTE"
        assert d["quota_energia_pct"] == pytest.approx(QE_DEMO)
        assert d["emissioni_tco2"] == pytest.approx(EMI_DEMO)

    def test_demo_degenere(self):
        p = _F["mh644_demo"]()
        p["utilizzo_pct"] = 0.0
        d = _F["mh644_demo_calcoli"](p)
        assert d["token_annui"] == 0.0
        assert d["kwh_per_mtoken"] is None
        assert d["costo_per_mtoken_eur"] is None
        assert d["margine_annuo_eur"] is None
        assert d["flussi"] is None
        assert d["van_eur"] is None
        assert d["verdetto"] == "NON_CALCOLABILE"


class TestRegistrazione:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W644 (22/10/2026)")[1].split(
            "# W643 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab644:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 659
        assert TITLE644 in titles

    def test_registrazione(self):
        assert f'"{TITLE644}"' in self._src()
        assert ", tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659 = st.tabs([" in self._src()
        assert "with tab644:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st644_[a-z0-9_]+", self._ui()))
        attese = {"st644_ngpu", "st644_wgpu", "st644_pue", "st644_util",
                  "st644_tps", "st644_ore", "st644_pene", "st644_capex",
                  "st644_opex", "st644_anni", "st644_tasso", "st644_pmk",
                  "st644_ef", "st644_toll", "st644_sens", "st644_go",
                  "st644_fig1", "st644_fig2", "st644_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st644_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        # "token" NON e' nei pattern: e' l'unita' di misura standard di
        # questa tab (token/s, Mtoken), non un segreto
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
