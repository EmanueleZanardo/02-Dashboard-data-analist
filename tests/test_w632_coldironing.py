"""Test tab632 "⚓ Cold ironing: elettrificare le navi in banchina".

Demo calcolata a mano: 5 MW x 2500 h x 0,7 -> 8.750 MWh/anno;
bunker 8750 x 0,21 = 1.837,5 t; CO2 1837,5 x 3,114 = 5.721,975 t;
CRF(7 %, 25 a) = 0,0858105172206656; capex 1,2M x 5 = 6.000.000;
capitale annuo = 6M x CRF + 6M x 3 % = 694.863,1033239936;
energia 8750 x 90 = 787.500; bunker eff. (ETS) 550 + 3,114 x 95 =
845,83; risparmio 1837,5 x 845,83 = 1.554.212,625; costo netto =
(694.863,1033239936 + 787.500 - 1.554.212,625)/5.721,975 =
-12,556769590221215 €/tCO2 -> CONVIENE (gap -107,56); margine =
71.849,52167600614; opex cash 180.000; payback 6M/(1.554.212,625 -
787.500 - 180.000) = 10,22647160524286 anni; quota energia =
787.500/(787.500 + 694.863,1033239936) = 0,5312463580846962.
Senza ETS: bunker 550 -> risparmio 1.010.625 -> costo netto 82,44
-> CONVIENE (82,44 <= 95).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh632_num", "mh632_nneg", "mh632_pos", "mh632_frac01",
           "mh632_energia_annua", "mh632_bunker_risparmiato_t",
           "mh632_co2_evitata_t", "mh632_crf", "mh632_capex_totale",
           "mh632_capitale_annuo", "mh632_costo_energia_annuo",
           "mh632_prezzo_bunker_eff", "mh632_risparmio_bunker",
           "mh632_costo_netto_co2", "mh632_margine", "mh632_verdetto",
           "mh632_gap_pareggio", "mh632_opex_cash_annuo",
           "mh632_payback_anni", "mh632_quota_energia_su_costi",
           "mh632_sensibilita", "mh632_demo")

TITLE632 = "⚓ Cold ironing: elettrificare le navi in banchina"

DEMO = _F["mh632_demo"]()
EN_DEMO = 8750.0
BUN_DEMO = 1837.5
CO2_DEMO = 5721.975
CRF_DEMO = 0.0858105172206656
CX_DEMO = 6000000.0
CAP_DEMO = 694863.1033239936
CE_DEMO = 787500.0
PEFF_DEMO = 845.83
RIS_DEMO = 1554212.625
CN_DEMO = -12.556769590221215
MG_DEMO = 71849.52167600614
GAP_DEMO = -107.55676959022122
OX_DEMO = 180000.0
PB_DEMO = 10.22647160524286
Q_DEMO = 0.5312463580846962
RIS_NOETS = 1010625.0
CN_NOETS = 82.44323040977875


class TestW632Validatori:
    def test_num(self):
        assert _F["mh632_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh632_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh632_nneg"](0, "x") == 0.0
        assert _F["mh632_pos"](0.001, "x") == 0.001
        assert _F["mh632_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh632_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh632_pos"](bad, "x")
        for bad in (-0.1, 1.5):
            with pytest.raises(ValueError):
                _F["mh632_frac01"](bad, "x")


class TestW632Catena:
    def test_energia_bunker_co2(self):
        assert _F["mh632_energia_annua"](5.0, 2500.0, 0.7) == EN_DEMO
        assert _F["mh632_bunker_risparmiato_t"](
            EN_DEMO, 0.21) == BUN_DEMO
        assert _F["mh632_co2_evitata_t"](
            BUN_DEMO, 3.114) == pytest.approx(CO2_DEMO)
        with pytest.raises(ValueError):
            _F["mh632_energia_annua"](5.0, 2500.0, 1.5)
        with pytest.raises(ValueError):
            _F["mh632_bunker_risparmiato_t"](-1.0, 0.21)

    def test_crf(self):
        assert _F["mh632_crf"](7.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh632_crf"](0.0, 25.0) == pytest.approx(1.0 / 25.0)
        with pytest.raises(ValueError):
            _F["mh632_crf"](7.0, 0.0)

    def test_capex_e_capitale(self):
        assert _F["mh632_capex_totale"](1200000.0, 5.0) == CX_DEMO
        ca = _F["mh632_capitale_annuo"](CX_DEMO, CRF_DEMO, 3.0)
        assert ca == pytest.approx(CAP_DEMO)
        with pytest.raises(ValueError):
            _F["mh632_capex_totale"](-5.0, 5.0)

    def test_costo_energia(self):
        assert _F["mh632_costo_energia_annuo"](
            EN_DEMO, 90.0) == CE_DEMO
        assert _F["mh632_costo_energia_annuo"](
            EN_DEMO, 0.0) == 0.0

    def test_prezzo_bunker_eff(self):
        assert _F["mh632_prezzo_bunker_eff"](
            550.0, 3.114, 95.0, True) == pytest.approx(PEFF_DEMO)
        assert _F["mh632_prezzo_bunker_eff"](
            550.0, 3.114, 95.0, False) == 550.0
        with pytest.raises(ValueError):
            _F["mh632_prezzo_bunker_eff"](550.0, 3.114, 95.0, "si")

    def test_risparmio_costo_netto(self):
        assert _F["mh632_risparmio_bunker"](
            BUN_DEMO, PEFF_DEMO) == pytest.approx(RIS_DEMO)
        assert _F["mh632_costo_netto_co2"](
            CAP_DEMO, CE_DEMO, RIS_DEMO,
            CO2_DEMO) == pytest.approx(CN_DEMO)
        assert _F["mh632_costo_netto_co2"](
            CAP_DEMO, CE_DEMO, RIS_DEMO, 0.0) is None
        with pytest.raises(ValueError):
            _F["mh632_costo_netto_co2"](
                -1.0, CE_DEMO, RIS_DEMO, CO2_DEMO)

    def test_margine(self):
        assert _F["mh632_margine"](RIS_DEMO, CAP_DEMO,
                                   CE_DEMO) == pytest.approx(MG_DEMO)
        assert _F["mh632_margine"](500000.0, CAP_DEMO,
                                   CE_DEMO) < 0

    def test_verdetto(self):
        assert _F["mh632_verdetto"](CN_DEMO, 95.0) == "CONVIENE"
        assert _F["mh632_verdetto"](CN_NOETS, 95.0) == "CONVIENE"
        assert _F["mh632_verdetto"](100.0, 95.0) == "MARGINALE"
        assert _F["mh632_verdetto"](95.0 * 1.15, 95.0) == "MARGINALE"
        assert _F["mh632_verdetto"](120.0, 95.0) == "NON_CONVIENTE"
        assert _F["mh632_verdetto"](None, 95.0) == "NON_CALCOLABILE"
        with pytest.raises(ValueError):
            _F["mh632_verdetto"](CN_DEMO, -1.0)

    def test_gap(self):
        assert _F["mh632_gap_pareggio"](
            CN_DEMO, 95.0) == pytest.approx(GAP_DEMO)
        assert _F["mh632_gap_pareggio"](None, 95.0) is None

    def test_opex_payback(self):
        assert _F["mh632_opex_cash_annuo"](
            CX_DEMO, 3.0) == OX_DEMO
        assert _F["mh632_payback_anni"](
            CX_DEMO, RIS_DEMO, CE_DEMO,
            OX_DEMO) == pytest.approx(PB_DEMO)
        assert _F["mh632_payback_anni"](
            CX_DEMO, 500000.0, CE_DEMO, OX_DEMO) is None

    def test_quota_energia(self):
        assert _F["mh632_quota_energia_su_costi"](
            CE_DEMO, CAP_DEMO) == pytest.approx(Q_DEMO)
        assert _F["mh632_quota_energia_su_costi"](0.0, 0.0) is None

    def test_sensibilita(self):
        rows = _F["mh632_sensibilita"](
            5.0, 2500.0, 0.7, 0.21, 3.114, 1200000.0, 0.0, 7.0,
            25.0, 3.0, 90.0, 95.0, [550.0, 700.0], [70.0, 90.0],
            True)
        assert len(rows) == 4
        r00 = rows[0]
        assert r00["p_bunker_eur_t"] == 550.0
        assert r00["p_el_eur_mwh"] == 70.0
        # riga hand-computed: energia 8750 x 70 = 612.500
        u00 = (CAP_DEMO + 612500.0 - RIS_DEMO) / CO2_DEMO
        assert r00["costo_netto_eur_t"] == pytest.approx(u00)
        assert r00["costo_netto_eur_t"] == \
            pytest.approx(-43.14061520296856)
        assert r00["verdetto"] == "CONVIENE"
        r13 = rows[3]
        assert r13["p_bunker_eur_t"] == 700.0
        assert r13["p_el_eur_mwh"] == 90.0
        assert r13["costo_netto_eur_t"] == \
            pytest.approx(-60.72632643029829)
        assert r13["verdetto"] == "CONVIENE"

    def test_demo(self):
        d = DEMO
        assert d["potenza_media_mw"] == 5.0
        assert d["fattore_connessione"] == 0.7
        assert d["prezzo_co2_eur_t"] == 95.0
        assert d["includi_ets"] is True

    def test_catena_completa(self):
        d = dict(DEMO)
        en = _F["mh632_energia_annua"](d["potenza_media_mw"],
                                       d["ore_banchina_annue"],
                                       d["fattore_connessione"])
        bun = _F["mh632_bunker_risparmiato_t"](en, d["sfc_t_mwh"])
        co2 = _F["mh632_co2_evitata_t"](bun, d["ef_tco2_t"])
        crf = _F["mh632_crf"](d["tasso_pct"], d["anni"])
        cx = _F["mh632_capex_totale"](d["capex_eur_mw"],
                                      d["potenza_media_mw"])
        cxn = cx * (1.0 - d["contributo_capex_pct"] / 100.0)
        cap = _F["mh632_capitale_annuo"](cxn, crf, d["opex_pct"])
        ce = _F["mh632_costo_energia_annuo"](
            en, d["prezzo_elettricita_eur_mwh"]
            + d["oneri_rete_eur_mwh"])
        peff = _F["mh632_prezzo_bunker_eff"](
            d["prezzo_bunker_eur_t"], d["ef_tco2_t"],
            d["prezzo_co2_eur_t"], d["includi_ets"])
        ris = _F["mh632_risparmio_bunker"](bun, peff)
        cn = _F["mh632_costo_netto_co2"](cap, ce, ris, co2)
        mg = _F["mh632_margine"](ris, cap, ce)
        ver = _F["mh632_verdetto"](cn, d["prezzo_co2_eur_t"])
        gap = _F["mh632_gap_pareggio"](cn, d["prezzo_co2_eur_t"])
        ox = _F["mh632_opex_cash_annuo"](cxn, d["opex_pct"])
        pb = _F["mh632_payback_anni"](cxn, ris, ce, ox)
        assert en == pytest.approx(EN_DEMO)
        assert bun == pytest.approx(BUN_DEMO)
        assert co2 == pytest.approx(CO2_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert cx == pytest.approx(CX_DEMO)
        assert cap == pytest.approx(CAP_DEMO)
        assert ce == pytest.approx(CE_DEMO)
        assert peff == pytest.approx(PEFF_DEMO)
        assert ris == pytest.approx(RIS_DEMO)
        assert cn == pytest.approx(CN_DEMO)
        assert mg == pytest.approx(MG_DEMO)
        assert ver == "CONVIENE"
        assert gap == pytest.approx(GAP_DEMO)
        assert ox == pytest.approx(OX_DEMO)
        assert pb == pytest.approx(PB_DEMO)


class TestW632Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab632:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 664
        assert TITLE632 in titles

    def test_chain(self):
        assert ", tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664 = st.tabs([" in self._src()
        assert "with tab632:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st632_[a-z0-9_]+", self._ui()))
        attese = {"st632_pot", "st632_ore", "st632_conn",
                  "st632_sfc", "st632_ef", "st632_cx", "st632_sub",
                  "st632_tasso", "st632_anni", "st632_ox",
                  "st632_pel", "st632_oneri", "st632_pbun",
                  "st632_pco2", "st632_ets", "st632_sens",
                  "st632_go", "st632_fig", "st632_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st632_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W632 (22/10/2026)')[1]
        sec = sec.split('# W631 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
