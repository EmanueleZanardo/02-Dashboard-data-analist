"""Test tab642 "⚡🏭 VPP (Virtual Power Plant): aggregare la flessibilità distribuita".

Demo calcolata a mano: 200 asset da 0,5 MW, disponibilita' 90 %
-> potenza flessibile 90,0 MW.
120 chiamate/anno da 2 h, fattore erogazione 80 %
-> energia attivata 17.280,0 MWh/anno.
Ricavi capacita': 90 x 25.000 = 2.250.000 €/anno;
ricavi energia: 17.280 x 180 = 3.110.400 €/anno;
penali: 120 x 3 % x 90 x 5.000 = 1.620.000 €/anno.
Ricavi lordi = 2.250.000 + 3.110.400 - 1.620.000 = 3.740.400 €;
quota aggregatore 25 % -> 935.100 €/anno;
margine = 935.100 - 150.000 = 785.100 €/anno.
CRF(7 %, 10 a) = 0,14237750272736463; capex annuo
= 400.000 x CRF = 56.951,00109094585 €;
costo servizio = (56.951,00 + 150.000) / 90 = 2.299,455567677176 €/MW/anno
vs prezzo capacita' 25.000 €/MW/anno.
Quota penali = 1.620.000 / 5.360.400 = 30,221625251846877 %;
quota energia = 3.110.400 / 5.360.400 = 58,025520483546 %.
Flussi [-400.000, 785.100 x 10]: VAN(7 %) = 5.114.213,867786184 €;
TIR = 1,9627123322105908 (196,27 %); payback anno 1
-> CONVIENTE (tolleranza 10 %).
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh642_num", "mh642_nneg", "mh642_pos", "mh642_pct100",
           "mh642_potenza_flex_mw", "mh642_energia_attivata_mwh",
           "mh642_ricavi_capacita", "mh642_ricavi_energia", "mh642_penali",
           "mh642_ricavi_lordi", "mh642_ricavi_aggregatore",
           "mh642_margine_annuo", "mh642_crf", "mh642_capex_annuo",
           "mh642_costo_servizio_eur_mw_anno", "mh642_flussi", "mh642_van",
           "mh642_tir", "mh642_payback", "mh642_verdetto",
           "mh642_quota_penali_pct", "mh642_quota_energia_pct",
           "mh642_sensibilita", "mh642_demo_calcoli", "mh642_demo")

TITLE642 = ("⚡🏭 VPP (Virtual Power Plant): aggregare la flessibilità "
            "distribuita")

POT_DEMO = 90.0
EA_DEMO = 17280.0
RC_DEMO = 2250000.0
RE_DEMO = 3110400.0
PEN_DEMO = 1620000.0
RL_DEMO = 3740400.0
RA_DEMO = 935100.0
MA_DEMO = 785100.0
CRF_DEMO = 0.14237750272736463
CA_DEMO = 56951.00109094585
CS_DEMO = 2299.455567677176
QP_DEMO = 30.221625251846877
QE_DEMO = 58.025520483546
VAN_DEMO = 5114213.867786184
TIR_DEMO = 1.9627123322105908
PB_DEMO = 1


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh642_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh642_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh642_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh642_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh642_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh642_pos"](0, "x")

    def test_pct100(self):
        assert _F["mh642_pct100"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh642_pct100"](bad, "x")


class TestCalcoli:
    def test_potenza_flex(self):
        assert _F["mh642_potenza_flex_mw"](200.0, 0.5, 90.0) == POT_DEMO
        assert _F["mh642_potenza_flex_mw"](0.0, 0.5, 90.0) == 0.0

    def test_energia_attivata(self):
        assert _F["mh642_energia_attivata_mwh"](
            120.0, 2.0, POT_DEMO, 80.0) == EA_DEMO
        assert _F["mh642_energia_attivata_mwh"](
            120.0, 2.0, 0.0, 80.0) == 0.0

    def test_ricavi(self):
        assert _F["mh642_ricavi_capacita"](POT_DEMO, 25000.0) == RC_DEMO
        assert _F["mh642_ricavi_energia"](EA_DEMO, 180.0) == RE_DEMO

    def test_penali_e_lordi(self):
        assert _F["mh642_penali"](120.0, 3.0, POT_DEMO,
                                 5000.0) == PEN_DEMO
        assert _F["mh642_ricavi_lordi"](RC_DEMO, RE_DEMO,
                                        PEN_DEMO) == RL_DEMO

    def test_ricavi_aggregatore_e_margine(self):
        assert _F["mh642_ricavi_aggregatore"](RL_DEMO, 25.0) == RA_DEMO
        assert _F["mh642_margine_annuo"](RA_DEMO, 150000.0) == MA_DEMO
        assert _F["mh642_margine_annuo"](100000.0, 150000.0) == -50000.0

    def test_crf_e_capex_annuo(self):
        assert _F["mh642_crf"](7.0, 10) == pytest.approx(CRF_DEMO)
        assert _F["mh642_crf"](0.0, 10) == pytest.approx(0.1)
        assert _F["mh642_capex_annuo"](400000.0, 7.0,
                                       10) == pytest.approx(CA_DEMO)

    def test_costo_servizio(self):
        assert _F["mh642_costo_servizio_eur_mw_anno"](
            CA_DEMO, 150000.0, POT_DEMO) == pytest.approx(CS_DEMO)
        assert _F["mh642_costo_servizio_eur_mw_anno"](
            CA_DEMO, 150000.0, 0.0) is None

    def test_flussi_van_tir_payback(self):
        fl = _F["mh642_flussi"](400000.0, MA_DEMO, 10)
        assert len(fl) == 11 and fl[0] == -400000.0 and fl[1] == MA_DEMO
        assert _F["mh642_van"](fl, 7.0) == pytest.approx(VAN_DEMO)
        assert _F["mh642_tir"](fl) == pytest.approx(TIR_DEMO)
        assert _F["mh642_payback"](fl) == PB_DEMO

    def test_tir_payback_degeneri(self):
        assert _F["mh642_tir"]([-100.0, -10.0, -10.0]) is None
        assert _F["mh642_payback"]([-100.0, -10.0, -10.0]) is None

    def test_verdetto(self):
        v = _F["mh642_verdetto"]
        assert v(VAN_DEMO, 400000.0, 10.0) == "CONVIENTE"
        assert v(-30000.0, 400000.0, 10.0) == "MARGINALE"
        assert v(-40000.0, 400000.0, 10.0) == "MARGINALE"
        assert v(-40001.0, 400000.0, 10.0) == "NON_CONVIENTE"
        assert v(None, 400000.0, 10.0) == "NON_CALCOLABILE"

    def test_quote(self):
        assert _F["mh642_quota_penali_pct"](PEN_DEMO, RC_DEMO,
                                            RE_DEMO) == pytest.approx(QP_DEMO)
        assert _F["mh642_quota_energia_pct"](RE_DEMO,
                                             RC_DEMO) == pytest.approx(QE_DEMO)
        assert _F["mh642_quota_penali_pct"](0.0, 0.0, 0.0) == 0.0
        assert _F["mh642_quota_energia_pct"](0.0, 0.0) == 0.0

    def test_sensibilita(self):
        p = _F["mh642_demo"]()
        righe = _F["mh642_sensibilita"](p, [20000.0, 25000.0],
                                        [150.0, 180.0])
        assert len(righe) == 4
        r0 = righe[0]
        assert r0["prezzo_capacita_eur_mw_anno"] == 20000.0
        assert r0["prezzo_energia_eur_mwh"] == 150.0
        assert r0["verdetto"] in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                                  "NON_CALCOLABILE")

    def test_demo_calcoli_completi(self):
        d = _F["mh642_demo_calcoli"](_F["mh642_demo"]())
        assert d["potenza_flex_mw"] == POT_DEMO
        assert d["energia_attivata_mwh"] == EA_DEMO
        assert d["ricavi_lordi_eur"] == RL_DEMO
        assert d["margine_annuo_eur"] == MA_DEMO
        assert d["costo_servizio_eur_mw_anno"] == pytest.approx(CS_DEMO)
        assert d["van_eur"] == pytest.approx(VAN_DEMO)
        assert d["tir"] == pytest.approx(TIR_DEMO)
        assert d["payback_anni"] == PB_DEMO
        assert d["verdetto"] == "CONVIENTE"
        assert d["quota_penali_pct"] == pytest.approx(QP_DEMO)

    def test_demo_degenere(self):
        p = _F["mh642_demo"]()
        p["n_asset"] = 0.0
        d = _F["mh642_demo_calcoli"](p)
        assert d["potenza_flex_mw"] == 0.0
        assert d["costo_servizio_eur_mw_anno"] is None
        assert d["verdetto"] == "NON_CALCOLABILE"


class TestRegistrazione:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W642 (22/10/2026)")[1].split(
            "# W641 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab642:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 750
        assert TITLE642 in titles

    def test_registrazione(self):
        assert f'"{TITLE642}"' in self._src()
        assert ", tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750 = st.tabs([" in self._src()
        assert "with tab642:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st642_[a-z0-9_]+", self._ui()))
        attese = {"st642_nasset", "st642_mwasset", "st642_disp",
                  "st642_chiam", "st642_ore", "st642_fatt", "st642_pcap",
                  "st642_pene", "st642_fail", "st642_pen", "st642_capex",
                  "st642_opex", "st642_quota", "st642_tasso", "st642_anni",
                  "st642_toll", "st642_sens", "st642_go", "st642_fig1",
                  "st642_fig2", "st642_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st642_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
