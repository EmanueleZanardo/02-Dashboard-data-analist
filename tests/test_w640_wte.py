"""Test tab640 "♻️🔥 Termovalorizzatore: il business case waste-to-energy".

Demo calcolata a mano: capacita' 200.000 t/anno, disponibilita' 90 %
-> 180.000 t/anno trattate.
PCI 2,8 MWh/t, rendimento elettrico 25 % -> 126.000 MWh/anno;
rendimento termico 35 %, quota venduta 60 % -> 105.840 MWh/anno.
Tipping fee 150 €/t -> 27.000.000 €/anno; energia a 110 €/MWh ->
13.860.000 €/anno; calore a 45 €/MWh -> 4.762.800 €/anno;
ricavi totali 45.622.800 €/anno.
OPEX: fisso 18 M€ + 25 €/t x 180.000 = 22.500.000 €/anno;
margine 23.122.800 €/anno.
CRF(6 %, 25 a) = 0,07822671821227395; CAPEX annuo 300 M€ x CRF
= 23.468.015,46 €/anno.
Costo netto = (23.468.015,46 + 22.500.000 - 13.860.000 - 4.762.800)
/ 180.000 = 151,9178636871233 €/t; fee 150, toll 10 % (soglia 165)
-> MARGINALE; quota ricavi da energia 30,37954706857097 %.
Flussi [-300 M€, 23.122.800 x 25]: VAN(6 %) = -4.413.012,22 €;
TIR = 0,05844686844162206 (5,8447 %); payback anno 13.
Sensibilita': (fee 150, prezzo 110) -> 151,9178636871233 MARGINALE;
(fee 150, prezzo 140) -> 130,9178636871233 CONVIENTE;
(fee 170, prezzo 110) -> 151,9178636871233 CONVIENTE.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh640_num", "mh640_nneg", "mh640_pos", "mh640_pct100",
           "mh640_rifiuti_t", "mh640_energia_elettrica_mwh",
           "mh640_energia_termica_mwh", "mh640_ricavo_tipping",
           "mh640_ricavo_energia", "mh640_ricavi_totali",
           "mh640_opex_totale", "mh640_margine_annuo", "mh640_crf",
           "mh640_capex_annuo", "mh640_net_cost_eur_t", "mh640_flussi",
           "mh640_van", "mh640_tir", "mh640_payback", "mh640_verdetto",
           "mh640_quota_energia_pct", "mh640_sensibilita", "mh640_demo")

TITLE640 = "♻️🔥 Termovalorizzatore: il business case waste-to-energy"

RIF_DEMO = 180000.0
MWE_DEMO = 126000.0
MWT_DEMO = 105840.0
RT_DEMO = 27000000.0
RE_DEMO = 13860000.0
RC_DEMO = 4762800.0
RIC_DEMO = 45622800.0
OPX_DEMO = 22500000.0
MG_DEMO = 23122800.0
CRF_DEMO = 0.07822671821227395
CXA_DEMO = 23468015.463682186
NC_DEMO = 151.9178636871233
VAN_DEMO = -4413012.22359143
TIR_DEMO = 0.05844686844162206
PB_DEMO = 13
QE_DEMO = 30.37954706857097
NC_150_140 = 130.9178636871233


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh640_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh640_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh640_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh640_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh640_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh640_pos"](0.0, "x")

    def test_pct100(self):
        assert _F["mh640_pct100"](100.0, "x") == 100.0
        assert _F["mh640_pct100"](0.0, "x") == 0.0
        for bad in (-0.01, 100.01):
            with pytest.raises(ValueError):
                _F["mh640_pct100"](bad, "x")


class TestCalcoli:
    def test_rifiuti(self):
        assert _F["mh640_rifiuti_t"](200000.0, 90.0) == RIF_DEMO
        assert _F["mh640_rifiuti_t"](200000.0, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh640_rifiuti_t"](-1.0, 90.0)
        with pytest.raises(ValueError):
            _F["mh640_rifiuti_t"](200000.0, 101.0)

    def test_energie(self):
        assert _F["mh640_energia_elettrica_mwh"](
            RIF_DEMO, 2.8, 25.0) == pytest.approx(MWE_DEMO)
        assert _F["mh640_energia_termica_mwh"](
            RIF_DEMO, 2.8, 35.0, 60.0) == pytest.approx(MWT_DEMO)
        # solo elettrico -> calore nullo
        assert _F["mh640_energia_termica_mwh"](
            RIF_DEMO, 2.8, 0.0, 60.0) == 0.0

    def test_ricavi(self):
        assert _F["mh640_ricavo_tipping"](RIF_DEMO, 150.0) == RT_DEMO
        assert _F["mh640_ricavo_energia"](
            MWE_DEMO, 110.0) == pytest.approx(RE_DEMO)
        assert _F["mh640_ricavo_energia"](
            MWT_DEMO, 45.0) == pytest.approx(RC_DEMO)
        assert _F["mh640_ricavi_totali"](
            RT_DEMO, RE_DEMO, RC_DEMO) == pytest.approx(RIC_DEMO)

    def test_opex_margine(self):
        assert _F["mh640_opex_totale"](
            18000000.0, 25.0, RIF_DEMO) == OPX_DEMO
        assert _F["mh640_margine_annuo"](RIC_DEMO, OPX_DEMO) == pytest.approx(
            MG_DEMO)

    def test_crf(self):
        assert _F["mh640_crf"](6.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh640_crf"](0.0, 10.0) == 0.1

    def test_capex_annuo_net_cost(self):
        assert _F["mh640_capex_annuo"](
            300000000.0, CRF_DEMO) == pytest.approx(CXA_DEMO)
        assert _F["mh640_net_cost_eur_t"](
            CXA_DEMO, OPX_DEMO, RE_DEMO, RC_DEMO,
            RIF_DEMO) == pytest.approx(NC_DEMO)
        assert _F["mh640_net_cost_eur_t"](
            CXA_DEMO, OPX_DEMO, RE_DEMO, RC_DEMO, 0.0) is None

    def test_flussi_van(self):
        fl = _F["mh640_flussi"](300000000.0, MG_DEMO, 25.0)
        assert len(fl) == 26 and fl[0] == -300000000.0
        assert all(c == pytest.approx(MG_DEMO) for c in fl[1:])
        assert _F["mh640_van"](fl, 6.0) == pytest.approx(VAN_DEMO)

    def test_tir(self):
        assert _F["mh640_tir"]([-100.0, 60.0, 60.0]) == pytest.approx(
            0.13066238629180738)
        assert _F["mh640_tir"]([-100.0, -10.0, -10.0]) is None
        assert _F["mh640_tir"]([100.0, 10.0]) is None

    def test_payback(self):
        assert _F["mh640_payback"]([-100.0, 40.0, 40.0, 40.0]) == 3
        assert _F["mh640_payback"]([-100.0, 40.0, 40.0]) is None

    def test_verdetto(self):
        v = _F["mh640_verdetto"]
        assert v(None, 150.0, 10.0) == "NON_CALCOLABILE"
        assert v(150.0, 150.0, 10.0) == "CONVIENTE"
        assert v(150.01, 150.0, 10.0) == "MARGINALE"
        assert v(165.0, 150.0, 10.0) == "MARGINALE"
        assert v(165.01, 150.0, 10.0) == "NON_CONVIENTE"
        assert v(NC_DEMO, 150.0, 10.0) == "MARGINALE"

    def test_quota_energia(self):
        assert _F["mh640_quota_energia_pct"](
            RE_DEMO, RIC_DEMO) == pytest.approx(QE_DEMO)
        assert _F["mh640_quota_energia_pct"](100.0, 0.0) is None


class TestSensibilita:
    def _df(self):
        d = _F["mh640_demo"]()
        return _F["mh640_sensibilita"](
            [150.0, 170.0], [110.0, 140.0], d["capacita_t_anno"],
            d["disponibilita_pct"], d["pci_mwh_t"], d["eta_elettrica_pct"],
            d["eta_termica_pct"], d["quota_calore_venduta_pct"],
            d["prezzo_calore_eur_mwh"], d["capex_eur"],
            d["opex_fisso_eur_anno"], d["opex_variabile_eur_t"],
            d["tasso_pct"], d["anni"], d["toll_pct"])

    def test_forma(self):
        df = self._df()
        assert len(df) == 4
        assert set(df.columns) == {"tipping_fee_eur_t",
                                   "prezzo_energia_eur_mwh",
                                   "net_cost_eur_t", "verdetto"}

    def test_valori(self):
        df = self._df()
        r = df.set_index(["tipping_fee_eur_t", "prezzo_energia_eur_mwh"])
        assert r.loc[(150.0, 110.0), "net_cost_eur_t"] == pytest.approx(
            NC_DEMO)
        assert r.loc[(150.0, 110.0), "verdetto"] == "MARGINALE"
        assert r.loc[(150.0, 140.0), "net_cost_eur_t"] == pytest.approx(
            NC_150_140)
        assert r.loc[(150.0, 140.0), "verdetto"] == "CONVIENTE"
        assert r.loc[(170.0, 110.0), "net_cost_eur_t"] == pytest.approx(
            NC_DEMO)
        assert r.loc[(170.0, 110.0), "verdetto"] == "CONVIENTE"


class TestDemo:
    def test_demo_valori(self):
        d = _F["mh640_demo"]()
        assert d["capacita_t_anno"] == 200000.0
        assert d["tipping_fee_eur_t"] == 150.0
        assert d["anni"] == 25.0
        rif = _F["mh640_rifiuti_t"](d["capacita_t_anno"],
                                    d["disponibilita_pct"])
        assert rif == RIF_DEMO
        mwe = _F["mh640_energia_elettrica_mwh"](
            rif, d["pci_mwh_t"], d["eta_elettrica_pct"])
        mwt = _F["mh640_energia_termica_mwh"](
            rif, d["pci_mwh_t"], d["eta_termica_pct"],
            d["quota_calore_venduta_pct"])
        assert mwe == pytest.approx(MWE_DEMO)
        assert mwt == pytest.approx(MWT_DEMO)
        rt = _F["mh640_ricavo_tipping"](rif, d["tipping_fee_eur_t"])
        re_ = _F["mh640_ricavo_energia"](mwe, d["prezzo_energia_eur_mwh"])
        rc = _F["mh640_ricavo_energia"](mwt, d["prezzo_calore_eur_mwh"])
        ric = _F["mh640_ricavi_totali"](rt, re_, rc)
        assert ric == pytest.approx(RIC_DEMO)
        opx = _F["mh640_opex_totale"](d["opex_fisso_eur_anno"],
                                      d["opex_variabile_eur_t"], rif)
        assert opx == OPX_DEMO
        mg = _F["mh640_margine_annuo"](ric, opx)
        assert mg == pytest.approx(MG_DEMO)
        crf = _F["mh640_crf"](d["tasso_pct"], d["anni"])
        cxa = _F["mh640_capex_annuo"](d["capex_eur"], crf)
        assert cxa == pytest.approx(CXA_DEMO)
        nc = _F["mh640_net_cost_eur_t"](cxa, opx, re_, rc, rif)
        assert nc == pytest.approx(NC_DEMO)
        fl = _F["mh640_flussi"](d["capex_eur"], mg, d["anni"])
        assert _F["mh640_van"](fl, d["tasso_pct"]) == pytest.approx(VAN_DEMO)
        assert _F["mh640_tir"](fl) == pytest.approx(TIR_DEMO)
        assert _F["mh640_payback"](fl) == PB_DEMO
        assert _F["mh640_verdetto"](nc, d["tipping_fee_eur_t"],
                                    d["toll_pct"]) == "MARGINALE"


class TestStruttura:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W640 (22/10/2026)")[1].split(
            "# W639 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab640:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 694
        assert TITLE640 in titles

    def test_registrazione(self):
        assert f'"{TITLE640}"' in self._src()
        assert ", tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694 = st.tabs([" in self._src()
        assert "with tab640:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st640_[a-z0-9_]+", self._ui()))
        attese = {"st640_cap", "st640_disp", "st640_pci", "st640_etae",
                  "st640_etat", "st640_qcal", "st640_fee", "st640_pene",
                  "st640_pcal", "st640_capex", "st640_opexf", "st640_opexv",
                  "st640_tasso", "st640_anni", "st640_disc", "st640_toll",
                  "st640_sens", "st640_go", "st640_fig1", "st640_fig2",
                  "st640_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st640_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
